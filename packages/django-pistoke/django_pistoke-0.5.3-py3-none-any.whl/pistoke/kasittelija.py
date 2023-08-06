# -*- coding: utf-8 -*-

import asyncio
import json

from asgiref.sync import sync_to_async

import django
from django.conf import settings
from django.core.handlers.asgi import ASGIHandler, ASGIRequest
from django.core import signals
from django.http import QueryDict
from django.test.utils import override_settings
from django.urls import set_script_prefix, set_urlconf

from pistoke.ohjain import WEBSOCKET_MIDDLEWARE


class WebsocketPyynto(ASGIRequest):
  '''
  Yksittäisen Websocket-pyynnön (istunnon) tiedot.

  Huomaa, että __init__ ei kutsu super-toteutusta.
  '''
  # pylint: disable=too-many-instance-attributes
  # pylint: disable=method-hidden
  # pylint: disable=invalid-name

  POST = QueryDict()
  FILES = {}

  def __init__(self, scope):
    # pylint: disable=super-init-not-called
    self.scope = scope
    self._post_parse_error = False
    self._read_started = False
    self.resolver_match = None
    self.script_name = self.scope.get('root_path', '')
    if self.script_name and scope['path'].startswith(self.script_name):
      self.path_info = scope['path'][len(self.script_name):]
    else:
      self.path_info = scope['path']
    if self.script_name:
      self.path = '%s/%s' % (
        self.script_name.rstrip('/'),
        self.path_info.replace('/', '', 1),
      )
    else:
      self.path = scope['path']

    self.method = 'Websocket'

    query_string = self.scope.get('query_string', '')
    if isinstance(query_string, bytes):
      query_string = query_string.decode()
    self.META = {
      'REQUEST_METHOD': self.method,
      'QUERY_STRING': query_string,
      'SCRIPT_NAME': self.script_name,
      'PATH_INFO': self.path_info,
      'wsgi.multithread': True,
      'wsgi.multiprocess': True,
    }
    if self.scope.get('client'):
      self.META['REMOTE_ADDR'] = self.scope['client'][0]
      self.META['REMOTE_HOST'] = self.META['REMOTE_ADDR']
      self.META['REMOTE_PORT'] = self.scope['client'][1]
    if self.scope.get('server'):
      self.META['SERVER_NAME'] = self.scope['server'][0]
      self.META['SERVER_PORT'] = str(self.scope['server'][1])
    else:
      self.META['SERVER_NAME'] = 'unknown'
      self.META['SERVER_PORT'] = '0'
    for name, value in self.scope.get('headers', []):
      name = name.decode('latin1')
      corrected_name = 'HTTP_%s' % name.upper().replace('-', '_')
      value = value.decode('latin1')
      if corrected_name in self.META:
        value = self.META[corrected_name] + ',' + value
      self.META[corrected_name] = value

    self.resolver_match = None
    # def __init__

  # class WebsocketPyynto


class WebsocketVirhe(RuntimeError):
  ''' Virheellinen konteksti Websocket-pyynnön käsittelyssä (WSGI). '''


class WebsocketKasittelija(ASGIHandler):
  '''
  Saapuvien Websocket-pyyntöjen (istuntojen) käsittelyrutiini.
  '''
  def __new__(cls, *args, **kwargs):
    '''
    Alusta Django ennen käsittelyrutiinin luontia.

    Vrt. get_asgi_application().
    '''
    django.setup(set_prefix=False)
    return super().__new__(cls, *args, **kwargs)
    # def __new__

  async def __call__(self, scope, receive, send):
    '''
    Asynkroninen, pyyntökohtainen kutsu.

    Vrt. django.core.handlers.asgi:ASGIHandler.__call__
    '''
    assert scope['type'] == 'websocket'

    set_script_prefix(self.get_script_prefix(scope))
    await sync_to_async(
      signals.request_started.send,
      thread_sensitive=True
    )(
      sender=self.__class__, scope=scope
    )

    # Suorita Websocket-kättely.
    while (await receive())['type'] != 'websocket.connect':
      pass
    await send({'type': 'websocket.accept'})

    # Muodosta pyyntö.
    request = WebsocketPyynto(scope)

    # Hae käsittelevä näkymärutiini tai mahdollinen virheviesti.
    nakyma = await self.get_response_async(request)

    # Palauta virhesanoma, mikäli `dispatch` tuotti sellaisen.
    if not asyncio.iscoroutine(nakyma):
      nakyma._handler_class = self.__class__
      return await self.send_response(nakyma, send)

    # Luodaan asynkroninen tehtävä näkymän suorituksesta.
    nakyma_tehtava = asyncio.ensure_future(nakyma)

    # Luodaan jono saapuville syötteille.
    _syote = asyncio.Queue()
    async def syote():
      '''
      Erillinen metodi saapuvan syötteen käsittelyyn.

      Poimitaan ja toteutetaan mahdollinen katkaisupyyntö
      riippumatta siitä, lukeeko näkymärutiini syötettä vai ei.
      '''
      while True:
        sanoma = await receive()
        if sanoma['type'] == 'websocket.receive':
          await _syote.put(sanoma.get('text', sanoma.get('bytes', None)))
        elif sanoma['type'] == 'websocket.disconnect':
          break
        else:
          raise ValueError(sanoma['type'])
        # while True
      # async def syote
    syote_tehtava = asyncio.ensure_future(syote())

    async def _send(data):
      '''
      Lähetetään annettu data joko tekstinä tai tavujonona.
      '''
      if isinstance(data, str):
        return await send({'type': 'websocket.send', 'text': data})
      elif isinstance(data, bytearray):
        return await send({'type': 'websocket.send', 'bytes': bytes(data)})
      elif isinstance(data, bytes):
        return await send({'type': 'websocket.send', 'bytes': data})
      else:
        raise TypeError(str(type(data)))
      # async def _send

    # pylint: disable=attribute-defined-outside-init
    # Kääri ASGI-protokollan mukaiset `receive`- ja `send`-metodit
    # Websocket-metodeiksi.
    request.receive = _syote.get
    request.send = _send
    # pylint: enable=attribute-defined-outside-init

    # Alusta tehtävät.
    tehtavat = {syote_tehtava, nakyma_tehtava}

    # Odota siksi kunnes joko syöte katkaistaan
    # tai näkymärutiini on valmis.
    try:
      _, tehtavat = await asyncio.wait(
        tehtavat, return_when=asyncio.FIRST_COMPLETED
      )

    # Peruuta kesken jääneet tehtävät ja odota ne loppuun.
    finally:
      for kesken in tehtavat:
        kesken.cancel()
      await asyncio.gather(*tehtavat, return_exceptions=True)
      # Lähetä sanoma päättyneestä pyynnöstä.
      # Huomaa, että normaalisti tämä tehdään paluusanoman
      # `close`-metodissa;
      # ks. `django.http.response.HttpResponseBase.close`.
      await sync_to_async(
        signals.request_finished.send,
        thread_sensitive=True
      )(
        sender=self.__class__
      )
      # finally
    # async def __call__

  def load_middleware(self, is_async=False):
    '''
    Ajetaan vain muunnostaulun mukaiset Websocket-pyynnölle käyttöön
    otettavat ohjaimet.
    '''
    with override_settings(MIDDLEWARE=list(filter(None, (
      ws_ohjain if isinstance(ws_ohjain, str)
      else ohjain if ws_ohjain else None
      for ohjain, ws_ohjain in (
        (ohjain, WEBSOCKET_MIDDLEWARE.get(ohjain, False))
        for ohjain in settings.MIDDLEWARE
      )
    )))):
      super().load_middleware(is_async=is_async)
    # def load_middleware

  # Synkroniset pyynnöt nostavat poikkeuksen.
  def get_response(self, request):
    raise WebsocketVirhe
  def _get_response(self, request):
    raise WebsocketVirhe

  async def get_response_async(self, request):
    ''' Ohitetaan paluusanoman käsittelyyn liittyvät funktiokutsut. '''
    set_urlconf(settings.ROOT_URLCONF)
    return await self._middleware_chain(request)
    # async def get_response_async

  async def _get_response_async(self, request):
    ''' Ohitetaan paluusanoman käsittelyyn liittyvät funktiokutsut. '''
    # pylint: disable=not-callable
    callback, callback_args, callback_kwargs = self.resolve_request(request)
    for middleware_method in self._view_middleware:
      await middleware_method(request, callback, callback_args, callback_kwargs)
    # Kutsutaan `dispatch`-metodia synkronisesti, sillä se saattaa
    # aiheuttaa kantakyselyjä.
    # Huomaa, että paluusanomana saadaan `websocket`-metodin
    # palauttama alirutiini, joka palautetaan sellaisenaan.
    return await sync_to_async(callback, thread_sensitive=True)(
      request, *callback_args, **callback_kwargs
    )
    # async def _get_response_async

  async def send_response(self, response, send):
    '''
    Lähetä HTTP-virhesanoma soveltuvin osin
    Websocket-prokollan mukaisesti.

    Vrt. super-toteutus.
    '''
    # pylint: disable=invalid-name
    # Collect cookies into headers. Have to preserve header case as there
    # are some non-RFC compliant clients that require e.g. Content-Type.
    response_headers = []
    for header, value in response.items():
      response_headers.append((header, value))
    for c in response.cookies.values():
      response_headers.append(
        ('Set-Cookie', c.output(header='').strip())
      )
    # Initial response message.
    await send({
      'type': 'websocket.send',
      'text': json.dumps({
        'status': response.status_code,
        'headers': response_headers,
      }),
    })
    # Streaming responses need to be pinned to their iterator.
    if response.streaming:
      # Access `__iter__` and not `streaming_content` directly in case
      # it has been overridden in a subclass.
      for part in response:
        for chunk, _ in self.chunk_bytes(part):
          if chunk:
            await send({
              'type': 'websocket.send',
              'bytes': chunk,
            })
    # Other responses just need chunking.
    else:
      # Yield chunks of response.
      for chunk, _ in self.chunk_bytes(response.content):
        if chunk:
          await send({
            'type': 'websocket.send',
            'bytes': chunk,
          })
    response.close()
    # async def send_response

  # class WebsocketKasittelija

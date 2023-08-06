import threading
from typing import List
from google.protobuf.descriptor import FieldDescriptor, FileDescriptor, MethodDescriptor
from google.protobuf.json_format import MessageToDict
from grpc import Server, StatusCode
from delphai_utils.logging import logging
from grpc_requests import Client
from google.protobuf.descriptor_pb2 import MethodOptions
from google.api.http_pb2 import HttpRule
from grpc_requests.client import reset_cached_client
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.exceptions import HTTPException
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from functools import partial
import asyncio
import os
from hypercorn.config import Config
from hypercorn.asyncio import serve
from grpc import StatusCode
from urllib.parse import urlparse

supported_methods = ['get', 'put', 'post', 'delete', 'patch']

status_map = {
  StatusCode.OK: 200,
  StatusCode.CANCELLED: 499,
  StatusCode.UNKNOWN: 500,
  StatusCode.INVALID_ARGUMENT: 400,
  StatusCode.DEADLINE_EXCEEDED: 504,
  StatusCode.NOT_FOUND: 404,
  StatusCode.ALREADY_EXISTS: 409,
  StatusCode.PERMISSION_DENIED: 403,
  StatusCode.UNAUTHENTICATED: 401,
  StatusCode.RESOURCE_EXHAUSTED: 429,
  StatusCode.FAILED_PRECONDITION: 412,
  StatusCode.ABORTED: 499,
  StatusCode.OUT_OF_RANGE: 416,
  StatusCode.UNIMPLEMENTED: 404,
  StatusCode.INTERNAL: 418,
  StatusCode.UNAVAILABLE: 503,
  StatusCode.DATA_LOSS: 420
}


class AccessLogMiddleware(BaseHTTPMiddleware):
  async def dispatch(self, request, call_next):
    response = await call_next(request)
    if response.status_code < 400:
      path = urlparse(str(request.url)).path
      logging.info(f'[{response.status_code}] {request.method} {path}')
    return response


class GatewayServer(threading.Thread):
  handlers = {}
  client = None

  def get_http_status(self, grpc_code: StatusCode):
    return status_map[grpc_code]

  def __init__(self, descriptor: FileDescriptor, server: Server, port: int = 7070, daemon: bool = True) -> None:
    self.descriptor = descriptor
    self.server = server
    self.port = port
    reset_cached_client('localhost:8080')
    self.client = Client.get_by_endpoint('localhost:8080')
    super().__init__(daemon=daemon)

  async def request_handler(self, request):
    path = [route for route in request.scope['router'].routes if route.endpoint == request.scope['endpoint']][0].path
    body = {}
    if len(await request.body()) > 0:
      body = await request.json()
    input = {**request.path_params, **body}
    handler = self.handlers[path]
    try:
      raw_output = self.client.request(handler['service'], handler['method'], input, raw_output=True)
      output = MessageToDict(raw_output, preserving_proto_field_name=True)
      return JSONResponse(output)
    except Exception as ex:
      grpc_status = ex._state.code.name
      http_status_code = self.get_http_status(StatusCode[grpc_status])
      raise HTTPException(http_status_code, ex._state.details)

  async def http_exception(self, request, exc):
    if 'favicon.ico' not in str(request.url):
      path = urlparse(str(request.url)).path
      logging.error(f'[{exc.status_code}] {request.method} {path} - {exc.detail}')
    return JSONResponse({'detail': exc.detail, 'status': exc.status_code}, status_code=exc.status_code)

  def run(self) -> None:
    logging.info(f'starting gateway on port {self.port}')
    routes = []
    for service_handler in self.server._state.generic_handlers:
      if service_handler._name.startswith('grpc.'):
        logging.info(f'skipping service {service_handler._name}')
      else:
        logging.info(f'processing service {service_handler._name}')
        for key, handler in service_handler._method_handlers.items():
          method_name = key[1:].split('/')[1]
          service_name = key[1:].split('/')[0].split('.')[-1]
          logging.info(f'  processing {method_name}')
          method_descriptor: MethodDescriptor = self.descriptor.services_by_name[service_name].methods_by_name[
            method_name]
          method_options: MethodOptions = method_descriptor.GetOptions()
          fields: List(FieldDescriptor) = method_options.ListFields()
          for field in fields:
            http_rule: HttpRule = field[1]
            for supported_method in supported_methods:
              http_path = getattr(http_rule, supported_method)
              if http_path != '':
                route = Route(http_path, endpoint=self.request_handler, methods=[supported_method])
                routes.append(route)
                self.handlers[http_path] = {'service': service_handler._name, 'method': method_name}
    middleware = [Middleware(AccessLogMiddleware)]
    debug = 'DELPHAI_ENVIRONMENT' in os.environ and os.environ['DELPHAI_ENVIRONMENT'] == 'development'
    app = Starlette(debug=debug,
                    routes=routes,
                    exception_handlers={HTTPException: self.http_exception},
                    middleware=middleware)
    config = Config()
    config.bind = [f'0.0.0.0:{self.port}']
    config.loglevel = 'INFO'
    config.accesslog = '-'
    config.errorlog = '-'
    logging.getLogger('hypercorn.access').setLevel(logging.INFO)
    asyncio.run(serve(app, config))


def start_gateway(descriptor: FileDescriptor, server: Server, port: int = 7070):
  gateway_server = GatewayServer(descriptor=descriptor, server=server, port=port, daemon=True)
  gateway_server.start()

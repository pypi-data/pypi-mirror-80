import asyncio
from asyncio.base_events import BaseEventLoop
from grpc import Server
from grpc.experimental import aio
from grpc_reflection.v1alpha import reflection
from grpc_health.v1 import health, health_pb2_grpc
from grpc_health.v1.health_pb2 import _HEALTH, HealthCheckResponse
from delphai_utils.logging import logging
from google.protobuf.descriptor import FileDescriptor
from gateway import start_gateway
import signal

shutdown_event = asyncio.Event()


def create_grpc_server(descriptor: FileDescriptor):
  server = aio.server()
  server.__dict__['descriptor'] = descriptor
  server.add_insecure_port('[::]:8080')
  health_servicer = health.HealthServicer(experimental_non_blocking=True)
  health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)
  services = descriptor.services_by_name.keys()
  service_full_names = list(map(lambda service: descriptor.services_by_name[service].full_name, services))
  service_names = (
    *service_full_names,
    _HEALTH.full_name,
    reflection.SERVICE_NAME,
  )
  reflection.enable_server_reflection(service_names, server)
  return server


def _signal_handler(*_) -> None:
  shutdown_event.set()


async def start_server(server: Server, gateway: bool = True):
  logging.info('starting grpc server...')
  await server.start()
  logging.info('started grpc server on port 8080')
  if gateway:
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGTERM, _signal_handler)
    await start_gateway(server.__dict__['descriptor'], shutdown_trigger=shutdown_event.wait)
  else:
    await server.wait_for_termination()
import os, signal, threading, sys
from delphai_utils.logging import logging


# Disable
def block_print():
  sys.stdout = open(os.devnull, 'w')


# Restore
def enable_print():
  sys.stdout = sys.__stdout__


def _signal_handler(sig, frame):
  logging.info('stopping server...')
  sys.exit(0)


def wait_for_exit():
  signal.signal(signal.SIGINT, _signal_handler)
  forever = threading.Event()
  forever.wait()
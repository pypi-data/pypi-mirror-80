
# Copyright 2020 by Chromation, Inc
# All Rights Reserved by Chromation, Inc

import logging

CHROMASPEC_LOG_FORMAT="%(asctime)-15s:%(filename)s:%(funcName)s:%(lineno)d: %(message)s"
logging.basicConfig(format=CHROMASPEC_LOG_FORMAT)

CHROMASPEC_LOGGER         =logging.getLogger("microspeclib")
CHROMASPEC_LOGGER_TEST    =logging.getLogger("microspeclib.test")
CHROMASPEC_LOGGER_INTERNAL=logging.getLogger("microspeclib.internal")
CHROMASPEC_LOGGER_STREAM  =logging.getLogger("microspeclib.internal.stream")
CHROMASPEC_LOGGER_UTIL    =logging.getLogger("microspeclib.internal.util")
CHROMASPEC_LOGGER_PAYLOAD =logging.getLogger("microspeclib.internal.payload")
CHROMASPEC_LOGGER_JSON    =logging.getLogger("microspeclib.internal.json")
CHROMASPEC_LOGGER_DATA    =logging.getLogger("microspeclib.internal.data")

CHROMASPEC_LOGGER         .setLevel(logging.ERROR)
CHROMASPEC_LOGGER_TEST    .setLevel(logging.ERROR)
CHROMASPEC_LOGGER_INTERNAL.setLevel(logging.ERROR)

def verbose(includeInternals=False):
  """Turn on logging.

  Parameters
  ----------
  includeInternals: True or False
    Also activate logging for internal modules

  """
  CHROMASPEC_LOGGER           .setLevel(logging.WARNING)
  if includeInternals:
    CHROMASPEC_LOGGER_TEST    .setLevel(logging.WARNING)
    CHROMASPEC_LOGGER_INTERNAL.setLevel(logging.WARNING)
  
def quiet(includeInternals=False):
  """Turn off logging.

  Parameters
  ----------
  includeInternals: True or False
    Also deactivate logging for internal modules

  """
  CHROMASPEC_LOGGER           .setLevel(logging.ERROR)
  if includeInternals:
    CHROMASPEC_LOGGER_TEST    .setLevel(logging.ERROR)
    CHROMASPEC_LOGGER_INTERNAL.setLevel(logging.ERROR)
  
def debug(includeInternals=False):
  """Turn on verbose debugging trace.

  Parameters
  ----------
  includeInternals: True or False
    Also activate verbose debugging for internal modules

  """
  CHROMASPEC_LOGGER           .setLevel(logging.DEBUG)
  if includeInternals:
    CHROMASPEC_LOGGER_TEST    .setLevel(logging.DEBUG)
    CHROMASPEC_LOGGER_INTERNAL.setLevel(logging.DEBUG)
  
# Level uses:
# DEBUG:   Every substantial loop and branch
# INFO:    Every subroutine call and return
# WARNING: Minor errors that can usually be ignored
# ERROR:   Data format or API errors
# CRITIAL: Fatal errors like unopenable files or command line argument errors

# If you set the main logging level, everything will print, but if you set it
# just for one component, then just those and below will be produced

# One level per file isn't sufficient, as the reply and command data modules
# are spread out in multiple files


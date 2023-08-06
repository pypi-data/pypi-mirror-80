
# Copyright 2020 by Chromation, Inc
# All Rights Reserved by Chromation, Inc

from microspeclib.internal.jsonparse import enclassJsonFile
from microspeclib.logger             import CHROMASPEC_LOGGER_DATA as log
import os, sys

CHROMASPEC_COMMAND_ID, CHROMASPEC_COMMAND_NAME = enclassJsonFile("microspec.json", "command")

globals().update([[v.name,v] for k,v in CHROMASPEC_COMMAND_ID.items()])

__all__ = list(CHROMASPEC_COMMAND_NAME.keys())+["getCommandByID","getCommandByName"]

def getCommandByID(cid):
  log.info("cid=%d", cid)
  com = CHROMASPEC_COMMAND_ID.get(cid)
  log.info("return %s", com)
  return com

def getCommandByName(name):
  log.info("name=%s", name)
  com = CHROMASPEC_COMMAND_NAME.get(name)
  log.info("return %s", com)
  return com


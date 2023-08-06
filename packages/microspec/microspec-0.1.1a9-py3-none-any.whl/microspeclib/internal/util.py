
# Copyright 2020 by Chromation, Inc
# All Rights Reserved by Chromation, Inc

from microspeclib.logger import CHROMASPEC_LOGGER_UTIL as log
from struct import unpack, pack
import re
import itertools

class MicroSpecInteger(int):

  """A subclass of Python int that remembers it's byte width and name so that it can be 
  converted to bytes and str properly"""

  def __new__(self, value, size=1, byteorder="big", signed=False, name=None):
    log.info("value=%d size=%d byteorder=%s signed=%s name=%s", value, size, byteorder, signed, name)
    self = int.__new__(MicroSpecInteger, value)
    self.size      = size
    self.byteorder = byteorder
    self.signed    = signed
    self.name      = name
    log.info("return %s", self)
    return self

  def __str__(self):
    if self.name:
      return self.name
    return super().__str__()

  def __bytes__(self):
    log.info("")
    b = self.to_bytes(self.size, self.byteorder, signed=self.signed)
    log.info("return %s", b)
    return b

def isInt(i):
  log.info("int=%s", i)
  try:
    if int(i) == i:
      log.info("return True")
      return True
  except:
    log.info("return False")
    return False
  return False

def dehex(value):
  log.info("value=%s", value)
  if re.match('^0x[0-9a-fA-F]+$', str(value)):
    h = int(value, 16)
    log.info("return %d", h)
    return h
  elif re.match('^[Tt](?:rue)?$', str(value)):
    log.info("return True")
    return True
  elif re.match('^[Ff](?:alse)?$', str(value)):
    log.info("return False")
    return False
  log.info("return %s", value)
  return value

def _flatten(_list):
  for item in _list:
    if isinstance(item, list) or isinstance(item, tuple):
      yield from flatten(item)
    else:
      yield item

def flatten(_list):
  return list(_flatten(_list))

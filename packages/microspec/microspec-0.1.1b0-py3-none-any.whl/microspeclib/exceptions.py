
# Copyright 2020 by Chromation, Inc
# All Rights Reserved by Chromation, Inc

class MicroSpecException(Exception):
  pass

class MicroSpecEmulationException(MicroSpecException):
  pass

class MicroSpecConnectionException(MicroSpecException):
  pass


# Copyright 2020 by Chromation, Inc
# All Rights Reserved by Chromation, Inc

import unittest, os, pytest, time
from timeit import default_timer as timer
from tabulate import tabulate
from microspeclib.expert            import MicroSpecExpertInterface
from microspeclib.internal.emulator import MicroSpecEmulator
from microspeclib.datatypes         import *
from microspeclib.datatypes.command import CHROMASPEC_COMMAND_ID

@pytest.mark.usefixtures("class_results")
class MicroSpecTestExpertInterface(unittest.TestCase):
  __test__ = False # Abstract test class #

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  @classmethod
  def setUpClass(cls):
    cls.setup = False
    cls.emulator = MicroSpecEmulator()
    cls.min      = 0

  def setUp(self):
    if self.__class__.setup:
      return
    command = CommandGetBridgeLED(led_num=255)
    for i in range(0,100):
      t1 = timer()    
      self.software.sendCommand(command)
      r  = self.software.receiveReply()
      t2 = timer()    
      r.led_setting = 0
      assert r == BridgeGetBridgeLED(status=1, led_setting=0)
      self.__class__.min += t2 - t1
    self.__class__.min /= 100
    self.results.append(["Expert."+command.__class__.__name__ + "(Reference)", self.min*1000])
    self.__class__.setup = True

  @classmethod
  def tearDownClass(self):
    print()
    print(tabulate(self.results, headers='firstrow', tablefmt="pipe"))

def generateTest(command_class):
  def test(self):
    command = command_class()
    if command_class is CommandSetSensorConfig:
      command.binning    = True
      command.gain       = Gain1x
      command.row_bitmap = 0x1F
    elif command_class is CommandSetExposure:
      command.cycles  = 1
    else:
      for var in command:
        command[var]  = 0
    replies = self.__class__.emulator.process(command)
    if replies:
      expected_reply = replies.pop()
    else:
      expected_reply = BridgeNull()
    avg = 0
    for i in range(0,100):
      t1 = timer()    
      self.software.sendCommand(command)
      r  = self.software.receiveReply()
      t2 = timer()    
      if command_class is CommandCaptureFrame:
        # Fake it - can't possibly predict capture data
        r.num_pixels = expected_reply.num_pixels
        r.pixels     = expected_reply.pixels
      assert r == expected_reply
      avg += t2 - t1
    avg /= 100
    avg -= self.__class__.min
    self.results.append(["Expert."+command.__class__.__name__, avg*1000])
  return test

for command_id, command_class in CHROMASPEC_COMMAND_ID.items():
  if command_id < 0:
    continue
  order = "0"
  if   command_class.__name__[0:12] == "CommandReset": order = "0"
  elif command_class.__name__[0:10] == "CommandSet":   order = "1"
  else:                                                order = "2"
  setattr(MicroSpecTestExpertInterface, "test_"+order+"sending"+command_class.__name__, generateTest(command_class))


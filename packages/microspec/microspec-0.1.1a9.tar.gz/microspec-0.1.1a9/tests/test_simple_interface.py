
# Copyright 2020 by Chromation, Inc
# All Rights Reserved by Chromation, Inc

import unittest, os, pytest, time
from timeit   import default_timer as timer
from tabulate import tabulate
from microspeclib.simple            import MicroSpecSimpleInterface
from microspeclib.internal.emulator import MicroSpecEmulator
from microspeclib.datatypes         import *
from microspeclib.datatypes.command import CHROMASPEC_COMMAND_ID

@pytest.mark.usefixtures("class_results")
class MicroSpecTestSimpleInterface(unittest.TestCase):
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
      r  = self.software.getBridgeLED(led_num=255)
      t2 = timer()    
      r.led_setting = 0
      assert r == BridgeGetBridgeLED(status=1, led_setting=0)
      self.__class__.min += t2 - t1
    self.__class__.min /= 100
    self.results.append(["Simple."+command.__class__.__name__ + "(Reference)", self.min*1000])
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
    elif command_class is CommandSetAutoExposeConfig:
      command.max_tries        = 1
      command.start_pixel      = 2
      command.stop_pixel       = 3
      command.target           = 4
      command.target_tolerance = 5
      command.max_exposure     = 6
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
      kwargs = dict([ [k, command[k]] for k in command ])
      cname  = command.__class__.__name__[7:8].lower() + command.__class__.__name__[8:]
      t1 = timer()    
      r  = getattr(self.software, cname)(**kwargs)
      t2 = timer()    
      if command_class is CommandCaptureFrame:
        # Fake it - can't possibly predict capture data
        r.num_pixels = expected_reply.num_pixels
        r.pixels     = expected_reply.pixels
      assert r == expected_reply
      avg += t2 - t1
    avg /= 100
    avg -= self.__class__.min
    self.results.append(["Simple."+command.__class__.__name__, avg*1000])
  return test

for command_id, command_class in CHROMASPEC_COMMAND_ID.items():
  if command_id < 0:
    continue
  order = "0"
  if   command_class.__name__[0:12] == "CommandReset": order = "0"
  elif command_class.__name__[0:10] == "CommandSet":   order = "1"
  else:                                                order = "2"
  setattr(MicroSpecTestSimpleInterface, "test_"+order+"sending"+command_class.__name__, generateTest(command_class))


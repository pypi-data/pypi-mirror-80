
# Copyright 2020 by Chromation, Inc
# All Rights Reserved by Chromation, Inc

import unittest, os, pytest, psutil, time, sys
from io import BytesIO
from microspeclib.internal.stream   import MicroSpecEmulatedStream, \
                                            MicroSpecSerialIOStream
from microspeclib.internal.emulator import MicroSpecEmulator
from microspeclib.datatypes         import *
from microspeclib.datatypes.command import CHROMASPEC_COMMAND_ID

#from microspeclib.internal.logger import CHROMASPEC_LOGGER_INTERNAL
#import logging

from test_bytesio_stream import MicroSpecTestBytesIOStream

@pytest.mark.skipif(sys.platform not in ["darwin","linux"], reason="Emulation currently only runs on linux and MacOS")
class MicroSpecTestEmulatedStream(MicroSpecTestBytesIOStream):
  def __init__(self, *args, **kwargs):
    # Note: 0.1 second is way more than needed, but most of these are tests of proper functionality,
    # not failures and partial reads. For those cases, the timeout is set explicitly.
    #
    # Note: for testing low-level reads and writes, write to the hardware directly here and read
    # from software, as the separate running process is reading from hardware and will respond to
    # writes to the software side, thus messing up the tests. However, if you pretend to be the
    # hardware side and only write, it's not reading from that side of the socket.
    # 
    # Note: this is testing the STREAM, not the EMULATOR, so separate test files will fully end-to-end
    # send a command and check the response.
    super().__init__(*args, **kwargs)
    self.num_socats_before = self.num_running_socats()
    self.emulator = MicroSpecEmulator()
    self.hardware = MicroSpecEmulatedStream(timeout=0.1, socat=True, fork=False)
    self.software = MicroSpecSerialIOStream(device=self.hardware.software, timeout=0.1)

  def num_running_socats(self):
    num = 0
    for proc in psutil.process_iter():
      try:
        if "socat" in proc.name().lower():
          num += 1
      except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass
    return num

  def test_socatRunning(self):
    assert self.num_running_socats() > self.num_socats_before

  def test_emulatorPath(self):
    assert os.path.exists(self.hardware.hardware) == True
    assert os.path.exists(self.hardware.software) == True

  def test_partialReadBridgeNonzerostatusAndSensorReply(self):
    super().test_partialReadBridgeNonzerostatusAndSensorReply()
    # This (necessarily) leaves the buffer in a partial state, needs to be cleaned up
    self.hardware.stream.reset_input_buffer()
    self.hardware.buffer = b''
    self.hardware.current_command = []
    self.software.stream.reset_input_buffer()
    self.software.buffer = b''
    self.software.current_command = []

  # Note: until end of file, overrides of the BytesIO tests, so that we can use the same
  # tests without having to cut-and-paste:

  def generate_streams(self):
    return self.hardware, self.software

  def seek(self, stream, pos):
    return None

  def write_underlying(self, b, s, *args, **kwargs):
    return b.write(*args, **kwargs)

  def write_direct(self, b, s, *args, **kwargs):
    return b.write(*args, **kwargs)

  def sendCommand(self, b, s, *args, **kwargs):
    return b.sendCommand(*args, **kwargs)

  def sendReply(self, b, s, *args, **kwargs):
    return b.sendCommand(*args, **kwargs)

  def small_wait(self):
    time.sleep(0.1)

  def assert_getvalue(self, stream, value):
    pass

  def assert_readpos(self, stream, pos):
    pass
  
  def test_parameterStream(self):
    pass


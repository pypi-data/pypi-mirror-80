
# Copyright 2020 by Chromation, Inc
# All Rights Reserved by Chromation, Inc

import unittest, os, pytest
from io import BytesIO
from microspeclib.internal.stream   import MicroSpecBytesIOStream
from microspeclib.datatypes         import *
from microspeclib.datatypes.command import CHROMASPEC_COMMAND_ID
from microspeclib.logger            import CHROMASPEC_LOGGER_TEST as log

class MicroSpecTestBytesIOStream(unittest.TestCase):

  def generate_streams(self):
    b = BytesIO()
    s = MicroSpecBytesIOStream(stream=b)
    return b, s

  def test_defaultStream(self):
    b, s = self.generate_streams()
    s = MicroSpecBytesIOStream()
    assert b is not s.stream

  def test_parameterStream(self):
    b, s = self.generate_streams()
    assert b is s.stream

  def test_underlyingStreamRead1(self):
    b, s = self.generate_streams()
    d = b'\x00\x01\x02'
    self.write_underlying(b, s, d)
    r = s.read(1)
    assert d[0] == r[0]
    assert len(r) == 1

  def test_underlyingStreamRead1Fail(self):
    b, s = self.generate_streams()
    d = b''
    self.write_underlying(b, s, d)
    r = s.read(1)
    assert len(r) == 0

  def test_underlyingStreamReadAll(self):
    b, s = self.generate_streams()
    d = b'\x00\x01\x02'
    self.write_underlying(b, s, d)
    r = s.read(3)
    assert     r  ==     d
    assert len(r) == len(d)

  def test_underlyingStreamReadManyFail(self):
    b, s = self.generate_streams()
    d = b'\x00\x01\x02'
    self.write_underlying(b, s, d)
    r = s.read(10)
    assert     r  ==     d
    assert len(r) == len(d)

  def test_underlyingStreamWrite(self):
    b, s = self.generate_streams()
    b = BytesIO()
    s = MicroSpecBytesIOStream(stream=b)
    d = b'\x00\x01\x02'
    self.write_direct(b, s, d)
    self.seek( s, 0 )
    w = s.read()
    assert     w  ==     d
    assert len(w) == len(d)

  def test_write1Read1(self):
    b, s = self.generate_streams()
    d = b'\x00'
    self.write_direct(b, s, d)
    r = s.read(1)
    assert     r  ==     d
    assert len(r) == len(d)
    # No consume() means no moving forwards
    r = s.read(1)
    assert     r  ==     d
    assert len(r) == len(d)

  def test_write1Read1Consume1(self):
    b, s = self.generate_streams()
    d = b'\x00'
    self.write_direct(b, s, d)
    r = s.read(1)
    assert     r  ==     d
    assert len(r) == len(d)
    s.consume(1)
    r = s.read(1)
    assert     r  ==     b''
    assert len(r) == len(b'')

  def test_writeManyRead1(self):
    b, s = self.generate_streams()
    d = b'\x00\x01\x02'
    self.write_direct(b, s, d)
    r = s.read(1)
    assert     r  ==     d[0:1]
    assert len(r) == len(d[0:1])
    s.consume(1)
    r = s.read(1)
    assert     r  ==     d[1:2]
    assert len(r) == len(d[1:2])
    s.consume(1)
    r = s.read(1)
    assert     r  ==     d[2:3]
    assert len(r) == len(d[2:3])

  def test_writeManyReadInterleaved(self):
    b, s = self.generate_streams()
    d = b'\x00\x01\x02\x03\x04\x05'
    self.write_direct(b, s, d[0:3])
    r = s.read(1)
    assert     r  ==     d[0:1]
    assert len(r) == len(d[0:1])
    self.write_direct(b, s, d[3:4])
    s.consume(1)
    r = s.read(1)
    assert     r  ==     d[1:2]
    assert len(r) == len(d[1:2])
    s.consume(1)
    self.write_direct(b, s, d[4:5])
    r = s.read(1)
    assert     r  ==     d[2:3]
    assert len(r) == len(d[2:3])
    s.consume(1)
    r = s.read(1)
    self.write_direct(b, s, d[5:6])
    assert     r  ==     d[3:4]
    assert len(r) == len(d[3:4])
    s.consume(1)
    r = s.read(1)
    assert     r  ==     d[4:5]
    assert len(r) == len(d[4:5])
    s.consume(1)
    r = s.read(1)
    assert     r  ==     d[5:6]
    assert len(r) == len(d[5:6])

  def test_writeManyReadPartialConsume(self):
    b, s = self.generate_streams()
    d = b'\x00\x01\x02\x03\x04\x05'
    self.write_direct(b, s, d)
    r = s.read(4)
    assert     r  ==     d[0:4]
    assert len(r) == len(d[0:4])
    s.consume(2)
    r = s.read(4)
    assert     r  ==     d[2:6]
    assert len(r) == len(d[2:6])
    s.consume(2)
    r = s.read(4)
    assert     r  ==     d[4:6]
    assert len(r) == len(d[4:6])
    s.consume(2)
    r = s.read(4)
    assert     r  ==     d[6:6]
    assert len(r) == len(d[6:6])

  def test_writeReadCommand(self):
    b, s = self.generate_streams()
    w = []
    for cid in CHROMASPEC_COMMAND_ID.keys():
      if cid < 0: continue # Unimplemented test values in JSON
      cklass = getCommandByID(cid)
      c      = cklass()
      for v in c:
        c[v] = 99 # dummy data
      c.command_id = cklass.command_id # varibles include this, need to undo it
      self.sendCommand(b, s, c)
      w.append(c)
    self.small_wait()
    for cid in CHROMASPEC_COMMAND_ID.keys():
      if cid < 0: continue # Unimplemented test values in JSON
      c1 = s.receiveCommand()
      c2 = w.pop(0)
      assert c1 == c2

  def test_partialReadCommand(self):
    b, s = self.generate_streams()
    c = CommandGetBridgeLED(led_num=0)
    self.assert_getvalue(s.stream, b'')

    cb = bytes(c)
    cb1 = cb[0:len(cb)-1]
    cb2 = cb[len(cb)-1:]
    self.write_direct(b, s, cb1)
    self.assert_getvalue(s.stream, cb1)
    self.assert_readpos( s,        0  )
    assert s.buffer            == b''

    self.small_wait()
    r = s.receiveCommand()
    self.assert_getvalue(s.stream, cb1)
    self.assert_readpos( s,        1  )
    assert s.buffer            == cb1
    assert r is None

    self.write_direct(b, s, cb2)
    self.assert_getvalue(s.stream, cb1+cb2)
    self.assert_readpos( s,        1      )
    assert s.buffer            == cb1

    self.small_wait()
    r = s.receiveCommand()
    self.assert_getvalue(s.stream, cb1+cb2)
    self.assert_readpos( s,        2      )
    assert s.buffer            == b''
    assert r == CommandGetBridgeLED(led_num=0)

  def test_partialReadBridgeReply(self):
    b, s = self.generate_streams()
    r = BridgeGetBridgeLED(status=0, led_num=0, led_setting=1)
    self.assert_getvalue(s.stream, b'')

    rb = bytes(r)
    rb1 = rb[0:len(rb)-1]
    rb2 = rb[len(rb)-1:]
    self.write_direct(b, s, rb1)
    self.assert_getvalue(s.stream, rb1)
    self.assert_readpos( s,        0  )
    assert s.buffer            == b''

    self.small_wait()
    x = s.receiveReply(r.command_id)
    self.assert_getvalue(s.stream, rb1)
    self.assert_readpos( s,        1  )
    assert s.buffer            == rb1
    assert x is None

    self.write_direct(b, s, rb2)
    self.assert_getvalue(s.stream, rb1+rb2)
    self.assert_readpos( s,        1      )
    assert s.buffer            == rb1

    self.small_wait()
    x = s.receiveReply(r.command_id)
    self.assert_getvalue(s.stream, rb1+rb2)
    self.assert_readpos( s,        2      )
    assert s.buffer+s.read(0)  == b''
    assert x == BridgeGetBridgeLED(status=0, led_num=0, led_setting=1)

  def test_partialReadBridgeAndSensorReply(self):
    b, s = self.generate_streams()
    r1 = BridgeGetSensorLED(status=0)
    r2 = SensorGetSensorLED(status=1, led_setting=2)
    self.assert_getvalue(s.stream, b'')

    r1b = bytes(r1)
    r2b = bytes(r2)
    rb = r1b + r2b
    rb1 = rb[0:len(rb)-1]
    rb2 = rb[len(rb)-1:]
    self.write_direct(b, s, rb1)
    self.assert_getvalue(s.stream, rb1)
    self.assert_readpos( s,        0  )
    assert s.buffer            == b''

    self.small_wait()
    x = s.receiveReply(r1.command_id)
    self.assert_getvalue(s.stream, rb1)
    self.assert_readpos( s,        2  )
    assert s.buffer            == rb1
    assert x is None

    self.write_direct(b, s, rb2)
    self.assert_getvalue(s.stream, rb1+rb2)
    self.assert_readpos( s,        2      )
    assert s.buffer            == rb1

    self.small_wait()
    x = s.receiveReply(r1.command_id)
    self.assert_getvalue(s.stream, rb1+rb2)
    self.assert_readpos( s,        3      )
    assert s.buffer            == b''
    assert x == SensorGetSensorLED(status=1, led_setting=2)

  def test_partialReadBridgeNonzerostatusAndSensorReply(self):
    b, s = self.generate_streams()
    r1 = BridgeGetSensorLED(status=1)
    r2 = SensorGetSensorLED(status=0, led_setting=2)
    self.assert_getvalue(s.stream, b'')

    r1b = bytes(r1)
    r2b = bytes(r2)
    rb = r1b + r2b
    rb1 = rb[0:len(rb)-1]
    rb2 = rb[len(rb)-1:]
    self.write_direct(b, s, rb1)
    self.assert_getvalue(s.stream, rb1)
    self.assert_readpos( s,        0  )
    assert s.buffer            == b''

    self.small_wait()
    x = s.receiveReply(r1.command_id)
    self.assert_getvalue(s.stream, rb1)
    self.assert_readpos( s,        2  )
    assert s.buffer            == rb1[1:]
    assert x == BridgeGetSensorLED(status=1)

  def test_writeReadReply(self):
    b, s = self.generate_streams()
    w = []
    for cid in CHROMASPEC_COMMAND_ID.keys():
      if cid < 0: continue # Unimplemented test values in JSON
      r1klass = getBridgeReplyByID(cid)
      r1      = r1klass()
      for v in r1:
        r1[v] = 99 # dummy data
      r1.command_id = r1klass.command_id              # varibles include this, need to undo it
      if r1.__dict__.get("status", None) is not None: # the null replies don't have this
        r1.status   = 0                               # set status 0 otherwise we trigger a different check
      log.info("sending bridge %s"%(r1))
      self.sendReply(b, s, r1)
      w.append(r1)
      r2klass = getSensorReplyByID(cid)
      if r2klass:
        r2      = r2klass()
        for v in r2:
          if r2.__dict__.get("repeat", None) is not None:
            if r2.repeat.get(v):
              r2[v] = [99]*99
              r2[r2.repeat[v]] = 99
            else:
              r2[v] = 99 # dummy data
          else:
            r2[v] = 99 # dummy data
        r2.command_id = r2klass.command_id              # varibles include this, need to undo it
        if r2.__dict__.get("status", None) is not None: # the null replies don't have this
          r2.status   = 0                               # set status 0 otherwise we trigger a different check
        log.info("sending sensor %s"%(r1))
        self.sendReply(b, s, r2)
        w.append(r2)
    self.small_wait()
    for cid in CHROMASPEC_COMMAND_ID.keys():
      if cid < 0: continue # Unimplemented test values in JSON
      r1 = s.receiveReply(cid)
      log.info("received %s"%(r1))
      r2 = w.pop(0)
      log.info("popped %s"%(r2))
      if getSensorReplyByID(cid):
        # If there's a sensor reply, we'll only get that half back with this call,
        #   never the bridge reply portion
        r2 = w.pop(0)
        log.info("popped additional %s"%(r2))
      assert r1 == r2

  # Note: all of these are here so we can override them in the emulator test and change where we're
  # pushing and pulling the data from/to:

  def seek(self, stream, pos):
    return stream.stream.seek(pos)

  def write_underlying(self, b, s, *args, **kwargs):
    return b.write(*args, **kwargs)

  def write_direct(self, b, s, *args, **kwargs):
    return s.write(*args, **kwargs)

  def sendCommand(self, b, s, *args, **kwargs):
    return s.sendCommand(*args, **kwargs)

  def sendReply(self, b, s, *args, **kwargs):
    return s.sendCommand(*args, **kwargs)

  def assert_getvalue(self, stream, value):
    assert stream.getvalue() == value

  def assert_readpos(self, stream, pos):
    assert stream.readpos == pos

  def small_wait(self):
    pass


















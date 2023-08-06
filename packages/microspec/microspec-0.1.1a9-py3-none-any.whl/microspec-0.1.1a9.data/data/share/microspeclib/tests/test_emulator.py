
# Copyright 2020 by Chromation, Inc
# All Rights Reserved by Chromation, Inc

import unittest, os
from microspeclib.internal.emulator import *
from microspeclib.datatypes         import *

class MicroSpecTestEmulator(unittest.TestCase):

  def test_chromationEmulatorSettings(self):
    #TODO: when we make more settings, test them here
    e = MicroSpecEmulator()

  def test_chromationEmulatorDefaults(self):
    e = MicroSpecEmulator()
    self.test_chromationEmulatorCompare(e, e)

  def test_chromationEmulatorNull(self):
    e = MicroSpecEmulator()
    assert e.process(CommandNull()) == []

  def test_chromationEmulatorVerify(self):
    e = MicroSpecEmulator()
    assert e.process(CommandVerify()) == [BridgeVerify(status=StatusOK)]

  def test_chromationEmulatorAutoExposure(self):
    e = MicroSpecEmulator()
    assert e.process(CommandAutoExposure()) == \
                    [BridgeAutoExposure(status=StatusOK),
                     SensorAutoExposure(status=StatusOK, success=0, iterations=0)]

  def test_chromationEmulatorCaptureFrame(self):
    e = MicroSpecEmulator()
    #TODO: need to change this when we make the capture frame emulation better
    assert e.process(CommandCaptureFrame()) == \
                    [BridgeCaptureFrame(status=StatusOK),
                     SensorCaptureFrame(status=StatusOK, num_pixels=4, pixels=[111,222,333,444])]

  def test_chromationEmulatorReset(self):
    e1 = MicroSpecEmulator()
    e2 = MicroSpecEmulator()
    self.test_chromationEmulatorSet(e2, bled0=LEDGreen, sled0=LEDRed, sled1=LEDGreen,
                                        binning=True, gain=Gain2_5x, rows=0x15, cycles=2345)
    assert e2.process(CommandReset()) == [BridgeReset(status=StatusOK)]
    self.test_chromationEmulatorCompare(e2, e1)

  def test_chromationEmulatorCompare(self, emulator=None, control=None):
    e = emulator or MicroSpecEmulator()
    c = control  or emulator or MicroSpecEmulator()
    assert e.process(CommandGetBridgeLED(led_num=0)) == \
                    [BridgeGetBridgeLED(status=StatusOK, led_num=0, led_setting=c.bridge_led[0])]
    assert e.process(CommandGetSensorLED(led_num=0)) == \
                    [BridgeGetSensorLED(status=StatusOK),
                     SensorGetSensorLED(status=StatusOK, led_num=0, led_setting=c.sensor_led[0])]
    assert e.process(CommandGetSensorLED(led_num=1)) == \
                    [BridgeGetSensorLED(status=StatusOK),
                     SensorGetSensorLED(status=StatusOK, led_num=1, led_setting=c.sensor_led[1])]
    assert e.process(CommandGetSensorConfig()) == \
                    [BridgeGetSensorConfig(status=StatusOK),
                     SensorGetSensorConfig(status=StatusOK, binning=c.binning, gain=c.gain, row_bitmap=c.rows)]
    assert e.process(CommandGetExposure()) == \
                    [BridgeGetExposure(status=StatusOK),
                     SensorGetExposure(status=StatusOK, cycles=c.cycles)]

  def test_chromationEmulatorSet(self, emulator=None, bled0=LEDOff, sled0=LEDOff, sled1=LEDOff,
                                       binning=BinningDefault, gain=GainDefault, rows=RowsDefault, cycles=0):
    e = emulator or MicroSpecEmulator()
    assert e.process(CommandSetBridgeLED(led_num=0, led_setting=bled0)) == \
                    [BridgeSetBridgeLED(status=StatusOK)]
    assert e.process(CommandSetSensorLED(led_num=0, led_setting=sled0)) == \
                    [BridgeSetSensorLED(status=StatusOK),
                     SensorSetSensorLED(status=StatusOK)]
    assert e.process(CommandSetSensorLED(led_num=1, led_setting=sled1)) == \
                    [BridgeSetSensorLED(status=StatusOK),
                     SensorSetSensorLED(status=StatusOK)]
    assert e.process(CommandSetSensorConfig(binning=binning, gain=gain, row_bitmap=rows)) == \
                    [BridgeSetSensorConfig(status=StatusOK),
                     SensorSetSensorConfig(status=StatusOK)]
    assert e.process(CommandSetExposure(cycles=cycles)) == \
                    [BridgeSetExposure(status=StatusOK),
                     SensorSetExposure(status=StatusOK)]
    assert e.bridge_led[0] == bled0
    assert e.sensor_led[0] == sled0
    assert e.sensor_led[1] == sled1
    assert e.binning       == binning
    assert e.gain          == gain
    assert e.rows          == rows
    assert e.cycles        == cycles

  def test_chromationEmulatorBadData(self):
    e = MicroSpecEmulator()
    assert e.process(CommandGetBridgeLED(led_num=-1)) == \
                    [BridgeGetBridgeLED(status=StatusError, led_num=0, led_setting=LEDOff)]
    assert e.process(CommandGetBridgeLED(led_num=1)) == \
                    [BridgeGetBridgeLED(status=StatusError, led_num=0, led_setting=LEDOff)]
    assert e.process(CommandGetSensorLED(led_num=-1)) == \
                    [BridgeGetSensorLED(status=StatusOK),
                     SensorGetSensorLED(status=StatusError, led_num=0, led_setting=LEDOff)]
    assert e.process(CommandGetSensorLED(led_num=2)) == \
                    [BridgeGetSensorLED(status=StatusOK),
                     SensorGetSensorLED(status=StatusError, led_num=0, led_setting=LEDOff)]
    assert e.process(CommandSetBridgeLED(led_num=-1, led_setting=LEDOff)) == \
                    [BridgeSetBridgeLED(status=StatusError)]
    assert e.process(CommandSetBridgeLED(led_num=1, led_setting=LEDOff)) == \
                    [BridgeSetBridgeLED(status=StatusError)]
    assert e.process(CommandSetBridgeLED(led_num=0, led_setting=99)) == \
                    [BridgeSetBridgeLED(status=StatusError)]
    assert e.process(CommandSetSensorLED(led_num=-1, led_setting=LEDOff)) == \
                    [BridgeSetSensorLED(status=StatusOK),
                     SensorSetSensorLED(status=StatusError)]
    assert e.process(CommandSetSensorLED(led_num=2, led_setting=LEDOff)) == \
                    [BridgeSetSensorLED(status=StatusOK),
                     SensorSetSensorLED(status=StatusError)]
    assert e.process(CommandSetSensorLED(led_num=2, led_setting=99)) == \
                    [BridgeSetSensorLED(status=StatusOK),
                     SensorSetSensorLED(status=StatusError)]
    assert e.process(CommandSetSensorConfig(binning=-1, gain=GainDefault, row_bitmap=RowsDefault)) == \
                    [BridgeSetSensorConfig(status=StatusOK),
                     SensorSetSensorConfig(status=StatusError)]
    assert e.process(CommandSetSensorConfig(binning=True, gain=99, row_bitmap=RowsDefault)) == \
                    [BridgeSetSensorConfig(status=StatusOK),
                     SensorSetSensorConfig(status=StatusError)]
    assert e.process(CommandSetSensorConfig(binning=True, gain=GainDefault, row_bitmap=0x00)) == \
                    [BridgeSetSensorConfig(status=StatusOK),
                     SensorSetSensorConfig(status=StatusError)]
    assert e.process(CommandSetSensorConfig(binning=True, gain=GainDefault, row_bitmap=0x8000)) == \
                    [BridgeSetSensorConfig(status=StatusOK),
                     SensorSetSensorConfig(status=StatusError)]
    assert e.process(CommandSetExposure(cycles=-1)) == \
                    [BridgeSetExposure(status=StatusOK),
                     SensorSetExposure(status=StatusError)]

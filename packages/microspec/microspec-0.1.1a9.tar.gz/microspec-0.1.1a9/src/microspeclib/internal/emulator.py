
# Copyright 2020 by Chromation, Inc
# All Rights Reserved by Chromation, Inc

from microspeclib.datatypes import *

class MicroSpecEmulator(object):
  
  def __init__(self):
    #TODO: more initialization state
    self.bridge_led = {0: LEDOff}
    self.sensor_led = {0: LEDOff, 1: LEDOff}
    self.binning    = BinningDefault
    self.gain       = GainDefault
    self.rows       = RowsDefault
    self.cycles     = 0 #TODO: default cycles value
    self.max_tries        = 0
    self.start_pixel      = 0
    self.stop_pixel       = 0
    self.target           = 0
    self.target_tolerance = 0
    self.max_exposure     = 0
    self.success          = 0
    self.iterations       = 0

  def process(self, command):
    #import pdb; pdb.set_trace()
    if command.command_id == CommandGetBridgeLED.command_id:
      try:
        num = command.led_num
        assert 0 <= num <= 0
        return [BridgeGetBridgeLED(led_num=num, led_setting=self.bridge_led[num], status=StatusOK)]
      except:
        return [BridgeGetBridgeLED(led_num=num, led_setting=LEDOff,               status=StatusError)]
    elif command.command_id == CommandSetBridgeLED.command_id:
      try:
        num = command.led_num
        led = command.led_setting
        assert 0 <= num <= 0
        assert led in [LEDOff, LEDGreen, LEDRed]
        self.bridge_led[num] = led
        return [BridgeSetBridgeLED(status=StatusOK)]
      except:
        return [BridgeSetBridgeLED(status=StatusError)]
    elif command.command_id == CommandGetSensorLED.command_id:
      try:
        num = command.led_num
        assert 0 <= num <= 1
        return [BridgeGetSensorLED(                                               status=StatusOK),
                SensorGetSensorLED(led_num=num, led_setting=self.sensor_led[num], status=StatusOK)]
      except:
        return [BridgeGetSensorLED(                                               status=StatusOK),
                SensorGetSensorLED(led_num=num, led_setting=LEDOff,               status=StatusError)]
    elif command.command_id == CommandSetSensorLED.command_id:
      try:
        num = command.led_num
        led = command.led_setting
        assert 0 <= num <= 1
        assert led in [LEDOff, LEDGreen, LEDRed]
        self.sensor_led[num] = led
        return [BridgeSetSensorLED(status=StatusOK),
                SensorSetSensorLED(status=StatusOK)]
      except:
        return [BridgeSetSensorLED(status=StatusOK),
                SensorSetSensorLED(status=StatusError)]
    elif command.command_id == CommandReset.command_id:
      self.bridge_led = {0: LEDOff}
      self.sensor_led = {0: LEDOff, 1: LEDOff}
      self.binning    = BinningDefault
      self.gain       = GainDefault
      self.rows       = RowsDefault
      self.cycles     = 0 #TODO: default cycles value
      return [BridgeReset(status=StatusOK)]
    elif command.command_id == CommandVerify.command_id:
      return [BridgeVerify(status=StatusOK)]
    elif command.command_id == CommandNull.command_id:
      return []
    elif command.command_id == CommandGetSensorConfig.command_id:
      return [BridgeGetSensorConfig(status=StatusOK),
              SensorGetSensorConfig(status=StatusOK, binning=self.binning, gain=self.gain, row_bitmap=self.rows)]
    elif command.command_id == CommandSetSensorConfig.command_id:
      try:
        assert False <= command.binning <= True
        assert command.gain in [Gain1x, Gain2_5x, Gain4x, Gain5x]
        assert command.row_bitmap != 0
        assert command.row_bitmap&0x1F != 0
        self.gain = command.gain
        self.binning = command.binning
        self.rows = command.row_bitmap
        return [BridgeSetSensorConfig(status=StatusOK),
                SensorSetSensorConfig(status=StatusOK)]
      except:
        return [BridgeSetSensorConfig(status=StatusOK),
                SensorSetSensorConfig(status=StatusError)]
    elif command.command_id == CommandAutoExposure.command_id:
      return [BridgeAutoExposure(status=StatusOK),
              SensorAutoExposure(status=StatusOK, success=0, iterations=0)]
    elif command.command_id == CommandGetAutoExposeConfig.command_id:
      return [BridgeGetAutoExposeConfig(status=StatusOK),
              SensorGetAutoExposeConfig(status=StatusOK, max_tries=self.max_tries, start_pixel=self.start_pixel,
                                        stop_pixel=self.stop_pixel, target=self.target, 
                                        target_tolerance=self.target_tolerance, max_exposure=self.max_exposure)]
    elif command.command_id == CommandSetAutoExposeConfig.command_id:
      self.max_tries        = command.max_tries
      self.start_pixel      = command.start_pixel
      self.stop_pixel       = command.stop_pixel
      self.target           = command.target
      self.target_tolerance = command.target_tolerance
      self.max_exposure     = command.max_exposure
      return [BridgeSetAutoExposeConfig(status=StatusOK),
              SensorSetAutoExposeConfig(status=StatusOK)]
    elif command.command_id == CommandGetExposure.command_id:
      return [BridgeGetExposure(status=StatusOK),
              SensorGetExposure(status=StatusOK, cycles=self.cycles)]
    elif command.command_id == CommandSetExposure.command_id:
      try:
        assert 0x00 <= command.cycles <= 0xFFFF
        self.cycles = command.cycles
        return [BridgeSetExposure(status=StatusOK),
                SensorSetExposure(status=StatusOK)]
      except:
        return [BridgeSetExposure(status=StatusOK),
                SensorSetExposure(status=StatusError)]
    elif command.command_id == CommandCaptureFrame.command_id:
      #TODO: big todo - play back recorded or make up data etc
      return [BridgeCaptureFrame(status=StatusOK),
              SensorCaptureFrame(status=StatusOK, num_pixels=4, pixels=[111,222,333,444])]
    return []

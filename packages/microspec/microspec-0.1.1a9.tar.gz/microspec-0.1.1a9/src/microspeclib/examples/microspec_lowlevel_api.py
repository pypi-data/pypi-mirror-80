#!/usr/bin/env python

'''Examples using the low-level version of the API.

USAGE
-----
After "pip install microspec", this script runs from the command
line with the command "microspec-lowlevel-api-example"

$ microspec-lowlevel-api-example
'''

from microspeclib.datatypes import *

def main():
    from microspeclib.expert    import MicroSpecExpertInterface

    xi = MicroSpecExpertInterface(timeout=0.1)
    #xi = MicroSpecExpertInterface(timeout=0.1, device="COM3")
    #xi = MicroSpecExpertInterface(timeout=0.1, device="/dev/cu.usbserial-CHROMATION09310")
    #xi = MicroSpecExpertInterface(timeout=0.1, emulation=True)

    xi.sendCommand(CommandSetBridgeLED(led_num=0, led_setting=LEDOff))
    print(xi.receiveReply())
    xi.sendCommand(CommandSetSensorLED(led_num=0, led_setting=LEDGreen))
    print(xi.receiveReply())
    xi.sendCommand(CommandSetSensorLED(led_num=1, led_setting=LEDRed))
    print(xi.receiveReply())

    xi.sendCommand(CommandGetBridgeLED(led_num=0))
    xi.sendCommand(CommandGetSensorLED(led_num=0))
    xi.sendCommand(CommandGetSensorLED(led_num=1))
    print(xi.receiveReply())
    print(xi.receiveReply())
    reply = xi.receiveReply()
    print(reply.status)
    print(reply.led_setting)

    command = CommandSetSensorConfig(binning=True, gain=Gain1x, row_bitmap=0x1F)
    print(xi.sendAndReceive(command))

    command = CommandSetExposure()
    command.cycles = 100
    print(xi.sendAndReceive(command))

    import time
    for i in range(0,5):
        reply = xi.sendAndReceive(CommandCaptureFrame())
        print(reply.status)
        print(reply.num_pixels)
        pixels = [str(pixel) for pixel in reply.pixels]
        print("first 3 pixels: %s"%(",".join(pixels[:3])))
        time.sleep(0.5)

if __name__ == "__main__":
    main()


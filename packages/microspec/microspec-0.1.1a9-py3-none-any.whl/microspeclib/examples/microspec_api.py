#!/usr/bin/env python

'''Examples using the API.

USAGE
-----
After "pip install microspec", this script runs from the command
line with the command "microspec-api-example"

$ microspec-api-example
'''

def main():
    '''A few examples using the microspec API.

    Usage
    -----
    Execute this function at the command line with command
    "microspec-api-example":

    $ microspec-api-example

    Entry Point
    -----------
    The name of this function must match the attribute in
    `setup.py` `setuptools.setup()` argument `entry_points`.
    '''
    from microspeclib.simple    import MicroSpecSimpleInterface
    from microspeclib.datatypes import LEDOff, LEDGreen, LEDRed, Gain1x

    si = MicroSpecSimpleInterface(timeout=0.1)
    #si = MicroSpecSimpleInterface(timeout=0.1, device="COM3")
    #si = MicroSpecSimpleInterface(timeout=0.1, device="/dev/cu.usbserial-CHROMATION09310")
    #si = MicroSpecSimpleInterface(timeout=0.1, emulation=True)

    print(si.setBridgeLED(led_num=0, led_setting=LEDOff))
    print(si.setSensorLED(led_num=0, led_setting=LEDGreen))
    print(si.setSensorLED(led_num=1, led_setting=LEDRed))
    print(si.getBridgeLED(led_num=0))
    print(si.getSensorLED(led_num=0))
    reply = si.getSensorLED(led_num=1)
    print(reply.status)
    print(reply.led_setting)

    print(si.setSensorConfig(binning=True, gain=Gain1x, row_bitmap=0x1F))
    print(si.setExposure(cycles=100))

    import time
    for i in range(0,5):
        reply = si.captureFrame()
        print(reply.status)
        print(reply.num_pixels)
        pixels = [str(pixel) for pixel in reply.pixels]
        print("first 3 pixels: %s"%(",".join(pixels[:3])))
        time.sleep(0.5)

if __name__ == '__main__':
    main()

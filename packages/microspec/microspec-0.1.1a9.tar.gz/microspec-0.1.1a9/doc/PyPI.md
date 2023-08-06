# MicroSpec Overview
Package `microspeclib` is a Python API for the Chromation
spectrometer dev-kit.

The `microspec` project also includes:

- command line utility `microspec-cmdline` for running basic
  measurements without developing a Python application
- an emulator (Mac and Linux only) for faking the dev-kit
  hardware in unit tests

## Spectrometer Hardware

The Chromation spectrometer is a surface-mount PCB package
consisting of a linear photodiode array and optical components.

The Python API communicates with firmware on the two
microcontrollers in the dev-kit, one on each of the stacked PCBs.

- The microcontroller on the bottom of the stack provides a SPI
interface to the Chromation spectrometer.
- The microcontroller on the PCB stacked above provides a USB
  bridge that turns the SPI interface into a USB interface.

`microspeclib` accesses this USB interface using `pyserial`.

# Install the Python API

Install the `microspec` project with `pip`:

```
$ pip install microspec
```

To extend/customize/repurpose the API, clone the repository from
the project homepage:
<https://github.com/microspectrometer/microspec> and install in
`--editable` mode.

## Windows Load VCP
On Windows, when connecting the dev-kit for the first time:

- Open Device Manager:
    - right-click on USB Serial Converter
    - select Properties
    - go to tab "Advanced"
    - check "Load VCP"
    - cycle power to the dev-kit (unplug/plug the USB cable)

Now "Load VCP" is enabled every time the dev-kit is connected to
this Windows computer.

If "Load VCP" is not enabled, `pyserial` cannot communicate with
the dev-kit and `microspec` will report that it does not see a
connected USB device.

## Install extra requirements for testing and documentation

Developers may want to install additional packages required for
running unit tests and rebuilding documentation.

```
$ pip install microspec[dev]
```

Many of the `microspec` unit tests use an emulator to fake the
dev-kit hardware. The emulator requires utility `socat`, which is
only available for Mac and Linux.

3. The documentation is built with Sphinx. Developers extending
   the API will need to rebuild the documentation. Install the
   Sphinx-related requirements by adding `[dev]` to the `install`
   command:

```
$ pip install microspec[dev]
```

# Use the Python API

Import the API in a Python script or at a Python REPL:

```python
>>> from microspeclib.simple import MicroSpecSimpleInterface
```

The API is a set of commands for configuring the spectrometer and
acquiring data.

There is one method for each command. Commands are
camelCaseFormatted. Commands return the received reply object. If
there is an error or a timeout, the reply is `None`.

The following will connect to the dev-kit USB hardware, capture a
single frame, then print the status, number of pixels, and the
value of the 3rd pixel.

```
from microspeclib.simple    import MicroSpecSimpleInterface
si = MicroSpecSimpleInterface(timeout=2)
reply = si.captureFrame()
print(reply.status)
print(reply.num_pixels)
print(reply.pixels[2])
```

## Command Line API

The `microspec_cmdline.py` executable will run a single command
and print the reply to stdout, optionally in CSV format. The
default is to look for hardware, but -f FILE can be used to point
it to either a device file or the name of a port, as in "COM3",
if necessary. The command itself is case-insensitive, and after
the command are key=value pairs of options for the command, if
necessary, such as `led_num=0` or `cycles=100`. 

The -t timeout is how long it will wait for the command each
time, and if it fails it will print None and move on. If a -r
repeat is specified, it will run the command that many times.
And if it is repeating, a -w wait will wait that long in between
commands. All times are in fractional seconds.

For example, to set the exposure and cycles and then get 3
capture frames spaced 1.5 seconds apart, with a timeout of 0.2
seconds on each, and print it in CSV format:

```
microspec_cmdline.py setsensorconfig binning=true gain=gain1x row_bitmap=0x1f
microspec_cmdline.py setexposure cycles=100
microspec_cmdline.py captureframe -t 0.2 -r 3 -w 1.5 --csv
```

### The command line utility is a `.exe` on Windows

On Windows, replace `microspec_cmdline.py` in the above lines
with `microspec_cmdline.exe`.

For example:

```powershell
> microspec-cmdline.exe captureframe -t 0.2 -r 3 -w 1.5 --csv
```

### Emulate hardware with `-e`

Note that if you have no hardware connected, you can (on Linux
and MacOSX) add a "-e" flag to use the emulator. It won't return
very interesting capture frame data, but it will give an
opportunity to test the interface.

## Emulator

For now, this is only supported on Linux and MacOSX, and requires
the `socat` executable to be installed and available on your PATH.

Use the emulator with the command-line utility by adding a "-e"
flag.

Use the emulator with the `microspeclib.simple` or
`microspeclib.expert` API with keyword argument `emulation=True`.

## More information
Please see the project homepage for more information:

<https://github.com/microspectrometer/microspec>

## Authors

- **Sean Cusack** - *Initial version* - [GitHub](https://github.com/eruciform) [Blog](https://eruciform.com)

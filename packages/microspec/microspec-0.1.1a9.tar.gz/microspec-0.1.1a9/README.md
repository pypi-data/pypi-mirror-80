# MicroSpecLib README

This library provides a number of interfaces for Chromation Spectrometer hardware, both in Python code, executables, servers, and emulators.

## Getting Started

The following instructions will get you going in a flash.

### Prerequisites

Since everything is Python in this library, with the exception of some documentation and configuration files, make sure that Python 3.7 or later is installed, as well as "pip". Then, use that to install some more Python modules:

* `python -m pip install pyserial`
* `python -m pip install pytest`
* `python -m pip install psutil`
* `python -m pip install tabulate`
* `python -m pip install sphinx`
* `python -m pip install recommonmark`
* `python -m pip install m2r`
* `python -m pip install sphinxcontrib-argdoc`

NOTE: The prerequisite for the emulator is to be running on Linux or MacOSX and installing the `socat` executable. The emulator does not work on other platforms.

### Installing

First, download microspeclib in the appropriate python location, and make sure that the src/ directory is in your PYTHONPATH and the bin/ directory is in your PATH. 

*NOTE: Include github download instructions.*

*NOTE: Pip install instructions will be in a future release.*

If you do not update your paths, you may need to specify them every time you use tools that utilize microspeclib, including the microspeclib executables themselves, for example:

```
cd microspeclib_install_dir
PATH=$PATH:bin PYTHONPATH=$PYTHONPATH:src python /my/script/dir/tool.py
PATH=$PATH:bin PYTHONPATH=$PYTHONPATH:src microspec_cmdline.py captureframe -e --csv
```

### File Locations

The breakdown of the installed files is thus:

* `microspeclib_install_dir`
  * `doc` - Documentation
  * `cfg`
    * `microspeclib.json` - Hardware Protocol
  * `bin`
    * `microspec_cmdline.py` - Command-line utility
    * `microspec_emulator.py` - Emulation server
    * `microspec_expert_example.py` - Example file for Expert interface
    * `microspec_simple_example.py` - Example file for Simple interface
  * `src`
    * `microspeclib`
      * `cmdline.py` - Used by cmdline tool
      * `exceptions.py` - List of custom exceptions
      * `expert.py` - Import to use Expert interface
      * `logger.py` - Import to use verbose(), debug(), and quiet()
      * `simple.py` - Import to use Simple interface
      * `datatypes` - Import * from this to access constants, classes, and data types
        * `bridge.py` - Import just bridge reply payload classes
        * `command.py` - Import just command payload classes
        * `sensor.py` - Import just sensor reply payload classes
        * `types.py` - Import just global constants
      * `internal`
        * `emulator.py` - Receive and response rules for hardware emulation
        * `jsonparse.py` - Parsing of protocol file
        * `payload.py` - Underlying classes that convert between binary payload and usable objects
        * `stream.py` - Test, emulation, and USB stream classes
        * `util.py` - Metaclass factory for payload data types using protocol file

NOTE: If you dig into the code to look for lists of functions, you will not find much that way, as almost all interface functions are auto-generated from the protocol JSON file. Please use documentation instead.

## Running the tests

Testing is done via `pytest`. Simply run it from the install directory:

```
cd microspeclib_install_dir
pytest
```

NOTE: It is not necessary to run the tests, but it will show if everything is installed correctly. It will also connect to the hardware if it's plugged in, or will skip hardware tests if it cannot find the hardware.

## Documentation

As long as the paths are set up properly, `pydoc` will find and display information about the library for you.

`pydoc microspeclib`

### HTML Documentation

Sphinx is used to create full API information. Simply point your browser of choice at the url:

`microspec_install_dir/doc/build/html/index.html`

### Rebuilding Documentation

You should not have to rebuild the documentation unless you made changes to the code or are forking the project. But if this is the case, you can update the Sphinx documentation in this way:

```
cd microspec_install_dir/doc
make clean html
```

Depending on the path setup, something akin to the following might be necessary. This is because, in order to pull in the tests, cfg, and bin directories as well, many things must be on the PYTHONPATH or PATH, that might not be there during a normal run of the API.

```
PATH=$PATH:../bin PYTHONPATH=../src:../:../tests make clean html
```

If you are truly restarting from scratch, you can recreate all the autodoc documentation files by doing the following, however, *this will wipe out a number of customizations* that were made after using this command to create the initial versions of the files. Note that you will also need to `make clean html` afterwards as well. This also only grabs code from microspeclib, not also the tests, cfg, or bin directories.

```
sphinx-apidoc -o source/ ../src/microspeclib -f -e -M
```

## Code API

The Python code APIs are broken down into Simple and Expert. Both are viable, but they balance usability and flexibility. Roughly speaking, if you don't need to heavily control timeouts and error cases, stick with Simple. If you need to send multiple messages and then extract replies one at a time, waiting for each in it's own loop, then feel free to use Expert.

### Simple API

Import the MicroSpecSimpleInterface, and use its methods to send a command and return a reply, if any. There is one method for each command, all of them camelCaseFormatted with initial lowercase, and taking arguments as necessary. They all return the received reply object, if any, or None if there's an error or a timeout. The reply objects all have member variables for each data field. At no point do you have to pack or unpack any objects or binary.

The following will connect to USB hardware if it's available, do one CaptureFrame command with whatever settings are on the hardware at the time, and print the status, number of pixels, and the value of the 3rd pixel.

```
from microspeclib.simple    import MicroSpecSimpleInterface
from microspeclib.datatypes import *
si = MicroSpecSimpleInterface(timeout=0.1)
reply = si.captureFrame()
print(reply.status)
print(reply.num_pixels)
print(reply.pixels[2])
```

By adding optional arguments to the original interface call, you can also point the API at a specific COM port, a specific /dev/ file, or the emulator.

For an executable example, see `bin/microspec_simple_example.py`.

For greater detail, see `pydoc microspeclib.simple`

NOTE: If the timeout runs out in the Simple interface, the data is lost, there is no recovering it.

### Expert Interface

The Expert interface requires putting together a Command object first, and sending it to the device... and then waiting until you get a reply object back. The setup of the interface is identical to Simple, as is the nature of the Reply object you get back. And the Command objects work the same was as Reply objects, just with different member variables. However, rather than a single call for each command, you must pack an object and then wait in a loop (or optionally a sendAndReceive can loop for you). This provides some flexibility for managing timing and error cases, but is more code. The Simple interface literally wraps the Expert one.

The following will connect to USB hardware if it's available, do one CaptureFrame command with whatever settings are on the hardware at the time, and print the status, number of pixels, and the value of the 3rd pixel.

```
from microspeclib.expert    import MicroSpecExpertInterface
from microspeclib.datatypes import *
xi = MicroSpecExpertInterface(timeout=0.1)
command = CommandCaptureFrame()
xi.sendCommand(command)
reply = xi.receiveReply()
while reply is None:
  # Do whatever waiting or other things you want
  reply = xi.receiveReply()
print(reply.status)
print(reply.num_pixels)
print(reply.pixels[2])
```

For an executable example, see `bin/microspec_expert_example.py`.

For greater detail, see `pydoc microspeclib.expert`

NOTE: If the timeout runs out in the Expert interface, the next receiveReply() will receive it, in an expected FIFO order.

## Command Line API

The `microspec_cmdline.py` executable will run a single command and print the reply to stdout, optionally in CSV format. The default is to look for hardware, but -f FILE can be used to point it to either a device file or the name of a port, as in "COM3", if necessary. The command itself is case-insensitive, and after the command are key=value pairs of options for the command, if necessary, such as `led_num=0` or `cycles=100`. 

The -t timeout is how long it will wait for the command each time, and if it fails it will print None and move on. If a -r repeat is specificied, it will run the command that many times. And if it is repeating, a -w wait will wait that long inbetween commands. All times are in fractional seconds.

For example, to set the exposure and cycles and then get 3 capture frames spaced 1.5 seconds apart, with a timeout of 0.2 seconds on each, and print it in CSV format:

```
microspec_cmdline.py setsensorconfig binning=true gain=gain1x row_bitmap=0x1f
microspec_cmdline.py setexposure cycles=100
microspec_cmdline.py captureframe -t 0.2 -r 3 -w 1.5 --csv
```

Note that if you have no hardware connected, you can (on Linux and MacOSX) add a "-e" flag to use the emulator. It won't return very interesting capture frame data, but it will give an opportunity to test the interface.

## Emulator

For now, this is only supported on Linux and MacOSX, and requires the `socat` executable to be installed and available on yor PATH. Technically the emulator executable can be run independently, though this is considered advanced and out of the scope of the public API. In order to use the emulator with the command-line utility, add a "-e" flag. In order to use it with either the Simple or Expert interface, add "emulation=True", and that's all that's needed.

### Emulator Internals

However, sometimes it's helpful to run the emulator so you can see what your code is actually sending through the line. You can bring up a copy of the emulator with:

`microspec_emulator.py -s`

which will print a line of text similar to `/var/folders/bq/91866d5j6zb06c04td5871kc0000gq/T/tmpmd7e9ab_/chromation.software` on stdout. You can then use "-f TEXT" with the cmdline utility, or device="TEXT" in the Simple or Expert interface, in order to connect to that emulator instance. If you add "-v" or "-d" to the emulator instance, you can get verbose or debug-level trace for what it's receiving (-d is heavier trace).

Or you can run the `socat` instance yourself, creating the two ends of the fake USB tunnel, and then connect the emulator to the hardware end. (Or theoretically connect to the hardware end yourself if you really wanted to.) 

```
socat -D PTY,raw,echo=0,link=./chromation.hardware PTY,raw,echo=0,link=./chromation.software
microspec_emulator.py -v -f microspec_emulator.py
```

...at which point you would have to connect to `microspec_emulator.py`.

## FAQ

1. Why can it not find my hardware? It's plugged in.
  * On Windows, sometimes VCP is not set. Go to Device Manager:
    * Right-click on USB Serial Converter
    * Select Properties
    * Go to tab "Advanced"
    * Check "Load VCP"

2. It's still not connecting.
  * Depending on the setup of the machine, you may need to be explicit about the device, rather than letting it auto-detect. Use "-f COM3" or "device='COM3'" if you know it's connected to the third COM port.

3. It says permission denied on the port.
  * You might have two interfaces connected to it at the same time. You can't have two on the same machine, let alone the same program, connected to a single USB port. So either another task is using that port, or your code has an old interface still lying around actively connected.

4. The emulator won't work on Windows.
  * The emulator only works on Linux and MacOSX and only if you have `socat` installed.

5. It's continually returning None.
  * Try increaing the timeout.



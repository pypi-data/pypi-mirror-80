
# Copyright 2020 by Chromation, Inc
# All Rights Reserved by Chromation, Inc

__doc__ = """Automated and static docstrings for json-generated classes, functions, and globals

Most of the API objects in MicroSpecLib are dynamically generated from cfg/microspec.json.
For example CommandSetBridgeLED, MicroSpecSimpleInterface.setBridgeLED, and LEDGreen are not
defined in code, they are created by meta-class factories, so that if the configuration changes
to permit new protocol commands and replies, the functions and classes will automatically update
as well. However, this causes a problem for documentation. 

Great pains were taken to auto-generate the proper function and class signatures such as
CommandSetBridgeLED(led_num=None, led_setting=None) rather than just CommandSetBridgeLED(\*args,
\**kwargs), so that pydoc and sphinx could introspect and document them properly. However,
the ONE thing that cannot be auto-generated is the per-function and per-class human-read
documentation. It could go into yet another json file and be auto-generated, but that would
be no more compact than making a file elsewhere for it. It could be written directly in
sphinx doc/source/\*.rst files, but then pydoc wouldn't find them. So the only choice left
is to make a separate internals docstrings library with the data in one place there, and
that is what this module is. Luckily, it at least saves some repetition, since both
CommandSetBridgeLED and MicroSpecSimpleInterface.setBridgeLED need the same documentation,
for example.

Thus, this module contains dictionaries for the different data and class types, and the datatype
module imports and implements them when it instantiates the metaclasses and generates the
globals. Since the json protocol and the documentation are separate, we must assume that one might
get out of sync with the other, thus it is assumed that this documentation may be missing
something. As such, implementers of these dictionaries should use DOC.get(value, None) and
handle lack of documentation in a responsible way.

The CHROMASPEC_DYNAMIC_DOC["command"]["CommandGetBridgeLED"] contains that docstring, for example.

And the _common global is used to hold common replacement patterns, to eliminate having to type
the same things over and over below - they are replaced at the end of the module.

What is the ~ for in ~{dt}.blah?
--------------------------------
The "~" is short-hand to use the class name as the link text in the
Sphinx HTML documentation.

Without the ~, the link text is the fully qualified class name:
microspeclib.blah.blah.classname.

~ is shorthand compared with the usual syntax to specify link text:
:class:`classname <microspeclib.blah.blah.classname>`

    - the link text is "classname"
    - the actual link (the matching identifier) is in the "<>"
    - the link text and <> must be separated by a space

":class:" is a cross-reference to a Python class. A hyperlink to that
class's documentation is created if the documentation exists.

":py:class:" and ":class:" are identical because Sphinx assumes the
language is Python.

Same goes for ":func:", ":mod:", etc.

"""

CHROMASPEC_DYNAMIC_DOC = {"command":{}, "bridge":{}, "sensor":{}}

_common = { 
  "api": "microspeclib.simple.MicroSpecSimpleInterface",
  "dt": "microspeclib.datatypes", 
  "default": "Default (after dev-kit power-on):",
  "valid": "Valid range:",
  "int": "microspeclib.internal.util.MicroSpecInteger",
  "led_settings": """:data:`~{dt}.types.LEDOff`, """
                """:data:`~{dt}.types.LEDGreen`, or """
                """:data:`~{dt}.types.LEDRed`""",
  "led_setting": """led_setting : :class:`~{int}`""",
  "gain1x": """:data:`~{dt}.types.Gain1x`""",
  "gain25x": """:data:`~{dt}.types.Gain2_5x`""",
  "gain4x": """:data:`~{dt}.types.Gain4x`""",
  "gain5x": """:data:`~{dt}.types.Gain5x`""",
  "gains": """{gain1x}, {gain25x}, {gain4x}, {gain5x}""",
  "OK":         """:data:`~{dt}.types.StatusOK`""",
  "ERROR":      """:data:`~{dt}.types.StatusError`""",
  "status":     """status : :class:`MicroSpecInteger <microspeclib.internal.util.MicroSpecInteger>`"""
                """\n\n"""
                """  0: {OK}"""
                """\n"""
                """    The dev-kit successfully executed the command."""
                """\n\n"""
                """  1: {ERROR}"""
                """\n"""
                """    The dev-kit failed to execute the command """
                """for one of the following reasons:"""
                """\n"""
                """\n      - serial communication failed"""
                """\n      - the command is invalid"""
                """\n      - one or more command parameters are invalid"""
                """\n\n"""
                """  If status is :data:`~{dt}.types.StatusError` """
                """the other attributes are not valid.""",
  "useful":     """see return values under **Parameters**""",
  "noimplement": """NOT IMPLEMENTED. Future: """,
  "notfinal":   """This is not the final payload for this command type. """  + \
                """If the Simple or Expert API returns this object, """ + \
                """then the command failed in the Bridge """ + \
                """and did not even make it to the Sensor.""",
  "null": """:func:`~{api}.null`""",
  "getBridgeLED": """:py:func:`~{api}.getBridgeLED`""",
  "setBridgeLED": """:py:func:`~{api}.setBridgeLED`""",
  "getSensorLED": """:py:func:`~{api}.getSensorLED`""",
  "setSensorLED": """:py:func:`~{api}.setSensorLED`""",
  "reset": """:py:func:`~{api}.reset`""",
  "verify": """:py:func:`~{api}.verify`""",
  "getSensorConfig": """:py:func:`~{api}.getSensorConfig`""",
  "setSensorConfig": """:py:func:`~{api}.setSensorConfig`""",
  "getExposure": """:py:func:`~{api}.getExposure`""",
  "setExposure": """:py:func:`~{api}.setExposure`""",
  "captureFrame": """:py:func:`~{api}.captureFrame`""",
  "autoExposure": """:py:func:`~{api}.autoExposure`""",
  "getAutoExposeConfig": """:py:func:`~{api}.getAutoExposeConfig`""",
  "setAutoExposeConfig": """:py:func:`~{api}.setAutoExposeConfig`""",
}

CHROMASPEC_DYNAMIC_DOC["command"]["CommandNull"] = """
Send `Null` to flush serial communication.

The Null command is a loopback request: the dev-kit ignores
`Null` and does not send a reply, but the API returns empty
object :class:`~{dt}.bridge.BridgeNull`.

Call {null} to flush the serial line in case of
desynchronization. This is a way to synchronize serial
communication with the dev-kit without exiting the application.

Returns
-------
:class:`~{dt}.bridge.BridgeNull`
    - empty object (no API attributes, not even `status`)

Example
-------
>>> from microspeclib.simple import MicroSpecSimpleInterface
>>> kit = MicroSpecSimpleInterface()
>>> print(kit.null())
BridgeNull()

"""
CHROMASPEC_DYNAMIC_DOC["command"]["CommandGetBridgeLED"] = """
Retrieve the state of the LED on the Bridge board.

The Bridge board is the top PCB in the dev-kit. There is only one
LED on the Bridge.

The state is either:
{led_settings}

Parameters
----------
led_num: int
  Valid input: 0

Returns
-------
:class:`~{dt}.bridge.BridgeGetBridgeLED`
  - status
  - led_setting

Example
-------
>>> from microspeclib.simple import MicroSpecSimpleInterface
>>> kit = MicroSpecSimpleInterface()
>>> print(kit.getBridgeLED(led_num=0))
BridgeGetBridgeLED(status=0, led_setting=1)

"""
CHROMASPEC_DYNAMIC_DOC["command"]["CommandSetBridgeLED"] = """
Set the state of the LED on the Bridge board.

The Bridge board is the top PCB in the dev-kit.

Parameters
----------
led_num : int

  - {valid} 0 (there is only one LED)

led_setting : int

  - {valid} {led_settings}

Returns
-------
:class:`~{dt}.bridge.BridgeSetBridgeLED`
  - status
"""
CHROMASPEC_DYNAMIC_DOC["command"]["CommandGetSensorLED"] = """
Retrieve the state of an LED on the Sensor board.

The Sensor board is the bottom PCB in the dev-kit. There are two
LEDs on the Sensor.

The state is either:
{led_settings}.

Parameters
----------
led_num : int

  - {valid} 0, 1

Returns
-------
:class:`~{dt}.sensor.SensorGetSensorLED`
    - status
    - led_setting

"""
CHROMASPEC_DYNAMIC_DOC["command"]["CommandSetSensorLED"] = """
Set the state of an LED on the Sensor board.

The Sensor board is the bottom PCB in the dev-kit. There are two
LEDs on the Sensor.

Parameters
----------
led_num : int

  - {valid} 0, 1

led_setting : int

  - {valid} {led_settings}

Returns
-------
:class:`~{dt}.sensor.SensorSetSensorLED`
  - status

"""
CHROMASPEC_DYNAMIC_DOC["command"]["CommandReset"] = """{noimplement} Resets the hardware and replies when the reset is complete.

Returns
-------
:class:`~{dt}.bridge.BridgeReset`
  - status

"""
CHROMASPEC_DYNAMIC_DOC["command"]["CommandVerify"] = """{noimplement} Verifies running status of the hardware.

Returns
-------
:class:`~{dt}.bridge.BridgeVerify`
  - status

"""
CHROMASPEC_DYNAMIC_DOC["command"]["CommandGetSensorConfig"] = """
Retrieve the spectrometer configuration.

Returns
-------
:class:`~{dt}.sensor.SensorGetSensorConfig`
  - status
  - binning
  - gain
  - row_bitmap

"""
CHROMASPEC_DYNAMIC_DOC["command"]["CommandSetSensorConfig"] = """
Configure the photodiode array in the spectrometer chip.

Parameters
----------
binning : int
  Connect adjacent pixels to double pixel width.

  0: OFF
    With binning **off** there are 784 pixels with 7.8µm pitch.
  1: ON
    With binning **on** there are 392 pixels with 15.6µm pitch.

  {default} 1 (binning ON)

gain : int
  The spectrometer chip has an internal analog gain. The gain
  setting applies to all pixels.

  - {valid} {gains}
  - {default} {gain1x}

row_bitmap : int

  Each pixel is 312.5µm tall and this height is divided into 5
  sub-pixels which can be enabled/disabled. Use all 5 rows of
  sub-pixels with a binary bitmap of 5 1's, i.e. 0001 1111 or
  0x1F. Use only the first three rows with 0000 0111. Any
  combination of rows is permitted.

  {default} 0x1F (0001 1111)

Returns
-------
:class:`~{dt}.sensor.SensorSetSensorConfig`
  - status

"""
CHROMASPEC_DYNAMIC_DOC["command"]["CommandAutoExposure"] = """
Auto-expose the spectrometer.

Tell dev-kit firmware to adjust spectrometer exposure time until
peak signal strength hits the auto-expose target.

Returns
-------
:class:`~{dt}.sensor.SensorAutoExposure`
  - status
  - success
  - iterations

Example
-------
>>> from microspeclib.simple import MicroSpecSimpleInterface
>>> kit = MicroSpecSimpleInterface()
>>> reply = kit.autoExposure()
>>> print(reply.success)
1
>>> print(reply.iterations)
3

See Also
--------
setAutoExposeConfig: configure auto-expose parameters
getExposure: get the new exposure time after the auto-expose

"""
CHROMASPEC_DYNAMIC_DOC["command"]["CommandGetAutoExposeConfig"] = """
Retrieve the current auto-expose configuration.

Returns
-------
:class:`~{dt}.sensor.SensorGetAutoExposeConfig`
    - status
    - max_tries
    - start_pixel
    - stop_pixel
    - target
    - target_tolerance
    - max_exposure

Example
-------
>>> from microspeclib.simple import MicroSpecSimpleInterface
>>> kit = MicroSpecSimpleInterface()
>>> reply = kit.getAutoExposeConfig()
>>> print(reply.max_tries)
12
>>> print(reply.start_pixel)
7
>>> print(reply.stop_pixel)
392
>>> print(reply.target)
46420
>>> print(reply.target_tolerance)
3277

See Also
--------
setAutoExposeConfig
"""
CHROMASPEC_DYNAMIC_DOC["command"]["CommandSetAutoExposeConfig"] = """
Set the auto-expose configuration.

The application should set `start_pixel` and `stop_pixel` to
match the pixel range in the spectrometer wavelength calibration
data. Chromation recommends using the default power-on values for
`target` and `target_tolerance`.

Parameters
----------
max_tries : int
  Maximum number of exposures to try before auto-expose gives up.

  - {valid} 1-255
  - {default} 12

  If `max_tries` is 0:

    - reply status is {ERROR}
    - auto-expose configuration is not changed

  The auto-expose algorithm usually terminates after a couple of
  tries, usually less than `max_tries`. The precise value of
  `max_tries` is not important as long as it is big enough for
  auto-expose to hit the target. `max_tries` is a safeguard
  against the auto-expose algorithm oscillating forever.

  Adjusting `max_tries` is useful when troubleshooting why
  {autoExposure} fails. To determine if {autoExposure} failed
  beacuse it hit `max_tries`, see the `iterations` attribute in
  the :class:`reply <{dt}.sensor.SensorAutoExposure>`.

start_pixel : int

  Auto-expose ignores pixels below `start_pixel` when finding
  the peak counts.

  - {valid} 7-392 (14-784 with pixel binning off)
  - {default} 7

  Recommended `start_pixel` is the lowest pixel number in the
  pixel-to-wavelength map.

  If `start_pixel` is outside the allowed range, reply
  `status` is {ERROR} and the auto-expose configuration is not
  changed.

stop_pixel : int

  Auto-expose ignores pixels above `stop_pixel` when finding
  the peak counts.

  - {valid} 7-392 (14-784 with pixel binning off),
  - `stop_pixel` must be >= `start_pixel`
  - {default} 7

  Recommended `stop_pixel` is the highest pixel number in the
  pixel-to-wavelength map.

  If `stop_pixel` is outside the allowed range, reply
  `status` is {ERROR} and the auto-expose configuration is not
  changed.

target : int

  Target peak-counts for exposure gain calculation.

  - {valid} 4500-65535
  - {default} 46420

  If `target` is outside the allowed range, reply `status` is
  {ERROR} and the auto-expose configuration is not changed.

  .. note::

    The lowest allowed target is 4500 counts, not 0 counts.

    4500 counts is chosen as the lowest allowed target to ensure
    that the signal is at least above the dark background.

    This is a conservative over-estimate on the dark background.
    Chromation ships the dev-kits with the dark background
    trimmed to approximately 1000 counts.

target_tolerance : int

  Auto-expose is finished when the peak counts lands within
  `target +/- target_tolerance`.

  - {valid} 0-65535
  - {default} 3277

  If the combination of `target` and `target_tolerance`
  results in target ranges extending **below 4500** counts or
  **above 65535 counts**, auto-expose **ignores** the
  `target_tolerance` and clamps the target range at these
  boundaries.

max_exposure : int

  The maximum integration time (exposure time) auto-expose is
  allowed to try. Auto-expose gives up if the exposure time is
  `max_exposure` and the peak counts is **below** the target
  range. 

  - {valid} 5-65535 (0.1ms to 1.3s)
  - {default} 10000 (200ms)

  The default is only 200ms, while the maximum integration time
  is 1.3s. There is nothing significant about 200ms. It is a
  compromise between detecting weak optical signals while keeping
  the wait time reasonably short.

  .. warning::

     There is a known bug in the dev-kit firmware that
     occassionally sets `max_exposure` to 4112 (82.24ms),
     regardless of the actual value sent in the
     {setAutoExposeConfig} command.

Returns
-------
:class:`~{dt}.sensor.SensorSetAutoExposeConfig`
  - status

Notes
-----
The default auto-expose configuration is optimized for the design
specifications of the spectrometer readout circuit on the Sensor
board.

The dev-kit uses a **16-bit ADC** to convert **pixel voltages**
to **counts**. The signal strength, therefore, is in **units of
counts** in the **range 0-65535**.

The default values for `target` and `target_tolerance`
guarantee that auto-expose, if it hits the target counts
range, chooses an exposure time that is within the **linear**
range of the spectrometer chip output.

- `target`: 46420 counts
- `target_tolerance`: 3277 counts

  3277 counts is a **+/-5%** of 65535, the full-scale counts.
  This **large** tolerance helps the auto-expose algorithm
  settle within a few iterations.

The largest peak considered to be within target, therefore,
is 49697 counts.

49697 counts is the **top** of the **guaranteed linear
range** of output values for the spectrometer chip when used
with the dev-kit.

49697 counts is based on:

- dev-kit specifications:

  - **16-bit** ADC
  - **1.8V** ADC voltage reference
  - **3.3V** power supply for the spectrometer chip

- spectrometer chip configuration:

  - binning **on**
  - gain **1x**
  - **all rows** active (i.e., use full pixel height)

"""
CHROMASPEC_DYNAMIC_DOC["command"]["CommandGetExposure"] = """
Retrieve the spectrometer integration time (exposure time).

Returns
-------
:class:`~{dt}.sensor.SensorGetExposure`
  - status
  - cycles

See Also
--------
setExposure
"""
CHROMASPEC_DYNAMIC_DOC["command"]["CommandSetExposure"] = """
Set spectrometer integration time (exposure time).

Parameters
----------
cycles : int
  Exposure time in units of 20µs cycles. For example, a 1ms
  exposure time is 50 cycles.

  - {valid} 5-65535 (0.1ms to 1.3s)
  - {default} 50 (1ms)

Returns
-------
:class:`~{dt}.sensor.SensorSetExposure`
  - status

"""
CHROMASPEC_DYNAMIC_DOC["command"]["CommandCaptureFrame"] = """
Retrieve one frame of spectrometer data.

Expose the pixels at the current integration time (exposure
time). Return an array of counts (signal strength) at each pixel.

Returns
-------
:class:`~{dt}.sensor.SensorCaptureFrame`
  - status
  - num_pixels
  - pixels

Example
-------
>>> from microspeclib.simple import MicroSpecSimpleInterface
>>> kit = MicroSpecSimpleInterface()
>>> print(kit.captureFrame())
SensorCaptureFrame(status=0, num_pixels=392, pixels=[7904, 8295, ...

See Also
--------
autoExposure: set optimal exposure time before capturing a frame
setExposure: manually set exposure time before capturing a frame
"""
CHROMASPEC_DYNAMIC_DOC["bridge"]["BridgeNull"] = """This packet doesn't actually exist, as the request for a Null
has no reply. However, to distinguish between an error, when a :class:`~{dt}.command.CommandNull` is requested, the
API returns this object rather than None.

"""
CHROMASPEC_DYNAMIC_DOC["bridge"]["BridgeGetBridgeLED"] = """
Contains result of command
{getBridgeLED}.

Attributes
----------
{status}

led_num : :class:`~{int}`

  Which LED the setting applies to.
  Valid range: 0 (only one LED on the Bridge)

{led_setting}

  State of the LED:
  {led_settings}

"""
CHROMASPEC_DYNAMIC_DOC["bridge"]["BridgeSetBridgeLED"] = """Contains the status of the :class:`~{dt}.command.CommandSetBridgeLED`
command.

Parameters
----------
{status}

"""
CHROMASPEC_DYNAMIC_DOC["bridge"]["BridgeGetSensorLED"] = """
Contains a transitory status of the
:class:`~{dt}.command.CommandGetSensorLED` command as it passes
through the Bridge. {notfinal}

Parameters
----------
{status}

"""
CHROMASPEC_DYNAMIC_DOC["bridge"]["BridgeSetSensorLED"] = """
Contains a transitory status of the
:class:`~{dt}.command.CommandGetSensorLED` command as it passes
through the Bridge. {notfinal}

Parameters
----------
{status}

"""
CHROMASPEC_DYNAMIC_DOC["bridge"]["BridgeReset"] = """Contains status status of the :class:`~{dt}.command.CommandReset`
command.

Parameters
----------
{status}

"""
CHROMASPEC_DYNAMIC_DOC["bridge"]["BridgeVerify"] = """Contains the status of the :class:`~{dt}.command.CommandVerify`
command.

Parameters
----------
{status}

"""
CHROMASPEC_DYNAMIC_DOC["bridge"]["BridgeGetSensorConfig"] = """
Contains a transitory status of the
:class:`~{dt}.command.CommandGetSensorConfig` command as it
passes through the Bridge. {notfinal}

Parameters
----------
{status}

"""
CHROMASPEC_DYNAMIC_DOC["bridge"]["BridgeSetSensorConfig"] = """
Contains a transitory status of the
:class:`~{dt}.command.CommandSetSensorConfig` command as it
passes through the Bridge. {notfinal}

Parameters
----------
{status}

"""
CHROMASPEC_DYNAMIC_DOC["bridge"]["BridgeAutoExposure"] = """
Contains a transitory status of the
:class:`~{dt}.command.CommandAutoExposure` command as it passes
through the Bridge. {notfinal}

Parameters
----------
{status}

"""
CHROMASPEC_DYNAMIC_DOC["bridge"]["BridgeGetExposure"] = """
Contains a transitory status of the :class:`~{dt}.command.CommandGetExposure`
command as it passes through the Bridge. {notfinal}

Parameters
----------
{status}

"""
CHROMASPEC_DYNAMIC_DOC["bridge"]["BridgeSetExposure"] = """
Contains a transitory status of the
:class:`~{dt}.command.CommandSetExposure` command as it passes
through the Bridge. {notfinal}

Parameters
----------
{status}

"""
CHROMASPEC_DYNAMIC_DOC["bridge"]["BridgeCaptureFrame"] = """
Contains a transitory status of the
:class:`~{dt}.command.CommandCaptureFrame` command as it passes
through the Bridge. {notfinal}

Parameters
----------
{status}

"""

CHROMASPEC_DYNAMIC_DOC["sensor"]["SensorGetSensorLED"] = """
Contains result of command
{getSensorLED}.

Attributes
----------
{status}

led_num : :class:`~{int}`

  Which LED the setting applies to.
  Valid range: 0, 1

{led_setting}

  State of the LED:
  {led_settings}

"""
CHROMASPEC_DYNAMIC_DOC["sensor"]["SensorSetSensorLED"] = """Contains the status of the :class:`~{dt}.command.CommandSetSensorLED`
command.

Parameters
----------
{status}

"""
CHROMASPEC_DYNAMIC_DOC["sensor"]["SensorGetSensorConfig"] = """
Contains result of command
`getSensorConfig`.

Parameters
----------
{status}
binning : 0, 1
  Whether or not to bin adjacent pixels.
  0: binning off, LIS-770i has 784 7.8µm-pitch pixels, 770 optically active
  1: binning on, LIS-770i has 392 15.6µm-pitch pixels, 385 optically active
gain : 0-255
  Analog pixel voltage gain. Allowed values:
  0x01: 1x gain
  0x25: 2.5x gain (37 in decimal)
  0x04: 4x gain
  0x05: 5x gain
row_bitmap:
  Which rows to permit sensing on. There are 5, and can all be
  activated with a binary bitmap of 5 1's, i.e. 011111 or 0x1F.
  The three most significant bits must be 0. Otherwise, any
  combination is permitted except 0x00.

"""
CHROMASPEC_DYNAMIC_DOC["sensor"]["SensorSetSensorConfig"] = """Contains the result of a :class:`~{dt}.command.CommandSetSensorConfig`
command.

Parameters
----------
{status}

"""
CHROMASPEC_DYNAMIC_DOC["sensor"]["SensorAutoExposure"] = """
Contains result of command
{autoExposure}.

Attributes
----------
{status}

success : :class:`~{int}`

  1: SUCCESS
    The peak signal is in the target counts range.

  0: FAILURE
    The peak signal is not in the target counts range.
    Fail for any of the following reasons:

      - reached the maximum number of tries
      - hit maximum exposure time and signal is below target range
      - hit minimum exposure time and signal is above target range

iterations : :class:`~{int}`

  Number of exposures tried by auto-expose.
  Valid range: 1-255

  `iterations` never exceeds {setAutoExposeConfig} parameter
  `max_tries`, the maximum number of iterations to try.

"""
CHROMASPEC_DYNAMIC_DOC["sensor"]["SensorGetExposure"] = """
Contains result of command
`getExposure`.

Parameters
----------
{status}
cycles : int
  Exposure time in units of 20µs cycles. For example, a 1ms
  exposure time is 50 cycles.

  - {valid} 5-65535 (0.1ms to 1.3s)
  - {default} 50 (1ms)

"""
CHROMASPEC_DYNAMIC_DOC["sensor"]["SensorSetExposure"] = """Contains the result of a :class:`~{dt}.command.CommandSetExposure`
command.

Parameters
----------
{status}

"""
CHROMASPEC_DYNAMIC_DOC["sensor"]["SensorCaptureFrame"] = """
Contains result of command {captureFrame}.

Attributes
----------
{status}
num_pixels : :class:`~{int}`

    Number of pixels to expect in the pixels parameter.

    - expect 392 pixels when pixel binning is ON

        - ON is the default value in firmware after dev-kit
          power-on

    - expect 784 pixels when pixel binning is OFF

pixels : list

    Counts (signal strength) at each pixel.
    Pixel counts are in the range 0-65535.

"""
CHROMASPEC_DYNAMIC_DOC["sensor"]["SensorSetAutoExposeConfig"] = """
Contains result of command {setAutoExposeConfig}.

Attributes
----------
{status}

"""
CHROMASPEC_DYNAMIC_DOC["sensor"]["SensorGetAutoExposeConfig"] = """
Contains result of command {getAutoExposeConfig}.

Attributes
----------
{status}
max_tries : :class:`~{int}`

  Maximum number of exposures to try before auto-expose gives up.

  - {valid} 1-255
  - {default} 12

start_pixel : :class:`~{int}`

  Auto-expose does not use pixels below `start_pixel`.

  - {valid} 1-392 (1-784 with pixel binning off)
  - {default} 7

stop_pixel : :class:`~{int}`

  Auto-expose does not use pixels above `stop_pixel`.

  - {valid} 1-392 (1-784 with pixel binning off)
  - {default} 392

target : :class:`~{int}`

  Auto-expose target peak counts.

  - {valid} 4500-65535
  - {default} 46420

target_tolerance : :class:`~{int}`

  Tolerance for hitting the auto-expose target. Auto-expose hits
  its target if the peak counts is in the range `target +/-
  target_tolerance`.

  - {valid} 0-65535
  - {default} 3277

max_exposure : :class:`~{int}`

  The maximum integration time (exposure time) auto-expose is
  allowed to try. Auto-expose gives up if the exposure time is
  `max_exposure` and the peak counts is **below** the target
  range. 

  - {valid} 5-65535 (0.1ms to 1.3s)
  - {default} 10000 (200ms)

"""
CHROMASPEC_DYNAMIC_DOC["sensor"]["SensorGetSensorConfig"] = """
Contains result of command {getSensorConfig}.

Attributes
----------
{status}
num_pixels : :class:`~{int}`

    Number of pixels to expect in the pixels parameter.

    - expect 392 pixels when pixel binning is ON

        - ON is the default value in firmware after dev-kit
          power-on

    - expect 784 pixels when pixel binning is OFF

pixels : list

    Counts (signal strength) at each pixel.
    Pixel counts are in the range 0-65535.

"""

for protocol in CHROMASPEC_DYNAMIC_DOC:
  for klass in CHROMASPEC_DYNAMIC_DOC[protocol]:
    while [found for found in _common.keys() if "{%s}"%found in CHROMASPEC_DYNAMIC_DOC[protocol][klass]]:
      #import pdb; pdb.set_trace()
      CHROMASPEC_DYNAMIC_DOC[protocol][klass] = CHROMASPEC_DYNAMIC_DOC[protocol][klass].format(**_common)

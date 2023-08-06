# -*- coding: utf-8 -*-
"""Define classes of command responses.

Every command has a response. This module defines the attributes
each response has.

Application code should **not** instantiate classes defined in
this module. Command responses are generated internally by module
:mod:`~microspec.commands`.
"""

from collections import namedtuple

# ----------------------
# | Docstring Snippets |
# ----------------------

_status = """\
status : str

    Serial communication status is either
    :data:`~microspec.constants.OK`, 
    :data:`~microspec.constants.ERROR`, or
    ``TIMEOUT``.

    :data:`~microspec.constants.TIMEOUT`:

        ``'TIMEOUT'`` means the command timed out before a
        response was received from the dev-kit, so the other
        response attributes are not valid. The timeout time in
        seconds is set by :class:`~microspec.commands.Devkit`
        attribute ``timeout``.
"""

_led_setting = """\
led_setting : str

    The LED is set to one of three states:
    :data:`~microspec.OFF`, :data:`~microspec.GREEN`, or
    :data:`~microspec.RED`.
"""

_created_from = """\
This response contains the attributes output with the
``__str__()`` method of ``microspeclib`` response:\
"""

_has_no_serial_attrs = """\
This response does not include the serial communication
attributes of the lower-level response. This is to prevent
applications from directly referencing the serial
communication data.
"""

_replaces_int_with_str = """\
In addition, this response replaces attribute integer values
with strings (e.g., 'OK' replaces 0). This makes the response
easier to read. The strings match the names of the constants
defined in :mod:`microspec.constants`.
"""

_common = {
    "status"                : _status,
    "led_setting"           : _led_setting,
    "created_from"          : _created_from,
    "has_no_serial_attrs"   : _has_no_serial_attrs,
    "replaces_int_with_str" : _replaces_int_with_str,
    }

# -----------
# | Replies |
# -----------

getBridgeLED_response = namedtuple(
        'getBridgeLED_response',
        ['status', 'led_setting']
        )
getBridgeLED_response.__doc__ = """
Response to command :func:`~microspec.commands.Devkit.getBridgeLED`.

Attributes
----------
{status}
{led_setting}

Notes
-----
{created_from}
:data:`~microspeclib.datatypes.bridge.BridgeGetBridgeLED`.

See Also
--------
~microspec.commands.Devkit.getBridgeLED
""".format(**_common)

setBridgeLED_response = namedtuple(
        'setBridgeLED_response',
        ['status']
        )
setBridgeLED_response.__doc__ = """
Response to command :func:`~microspec.commands.Devkit.setBridgeLED`.

Attributes
----------
{status}

Notes
-----
{created_from}
:data:`~microspeclib.datatypes.bridge.BridgeSetBridgeLED`.

See Also
--------
~microspec.commands.Devkit.setBridgeLED
""".format(**_common)

getSensorLED_response = namedtuple(
        'getSensorLED_response',
        ['status', 'led_setting']
        )
getSensorLED_response.__doc__ = """
Response to command :func:`~microspec.commands.Devkit.getSensorLED`.

Attributes
----------
{status}
{led_setting}

Notes
-----
{created_from}
:data:`~microspeclib.datatypes.sensor.SensorGetSensorLED`.

See Also
--------
~microspec.commands.Devkit.getSensorLED
""".format(**_common)

setSensorLED_response = namedtuple(
        'setSensorLED_response',
        ['status']
        )
setSensorLED_response.__doc__ = """
Response to command :func:`~microspec.commands.Devkit.setSensorLED`.

Attributes
----------
{status}

Notes
-----
{created_from}
:data:`~microspeclib.datatypes.sensor.SensorSetSensorLED`.

See Also
--------
~microspec.commands.Devkit.setSensorLED
""".format(**_common)

getSensorConfig_response = namedtuple(
        'getSensorConfig_response',
        ['status', 'binning', 'gain', 'row_bitmap']
        )
getSensorConfig_response.__doc__ = """
Response to command :func:`~microspec.commands.Devkit.getSensorConfig`.

Attributes
----------
{status}
binning
gain
row_bitmap

Notes
-----
{created_from}
:data:`~microspeclib.datatypes.sensor.SensorGetSensorConfig`.

See Also
--------
~microspec.commands.Devkit.getSensorConfig
""".format(**_common)

setSensorConfig_response = namedtuple(
        'setSensorConfig_response',
        ['status']
        )
setSensorConfig_response.__doc__ = """
Response to command :func:`~microspec.commands.Devkit.setSensorConfig`.

Attributes
----------
{status}

Notes
-----
{created_from}
:data:`~microspeclib.datatypes.sensor.SensorSetSensorConfig`.

See Also
--------
~microspec.commands.Devkit.setSensorConfig
""".format(**_common)

setExposure_response = namedtuple(
        'setExposure_response',
        ['status']
        )
setExposure_response.__doc__ = """
Response to command :func:`~microspec.commands.Devkit.setExposure`.

Attributes
----------
{status}

Notes
-----
{created_from}
:data:`~microspeclib.datatypes.sensor.SensorSetExposure`.

See Also
--------
~microspec.commands.Devkit.setExposure
""".format(**_common)

getExposure_response = namedtuple(
        'getExposure_response',
        ['status', 'ms', 'cycles']
        )
getExposure_response.__doc__ = """
Response to command :func:`~microspec.commands.Devkit.getExposure`.

Attributes
----------
{status}
ms
cycles

Notes
-----
{created_from}
:data:`~microspeclib.datatypes.sensor.SensorGetExposure`.

See Also
--------
~microspec.commands.Devkit.getExposure
""".format(**_common)

captureFrame_response = namedtuple(
        'captureFrame_response',
        ['status', 'num_pixels', 'pixels', 'frame']
        )
captureFrame_response.__doc__ = """
Response to command :func:`~microspec.commands.Devkit.captureFrame`.

Attributes
----------
{status}
        If :func:`captureFrame` timed out in a data logging
        application, it might improve data quality to check for
        ``status='TIMEOUT'`` to note a missing frame and skip
        logging this bad dataset.

        Similarly, in a GUI plotting application, it might
        improve user experience (and simplify the plotting code)
        to check for ``status='TIMEOUT'`` and replot the
        *previous* (good) dataset rather than plot the bad
        dataset.
num_pixels
pixels
frame

Notes
-----
{created_from}
:data:`~microspeclib.datatypes.sensor.SensorCaptureFrame`.

See Also
--------
~microspec.commands.Devkit.captureFrame
""".format(**_common)

autoExposure_response = namedtuple(
        'autoExposure_response',
        ['status', 'success', 'iterations']
        )
autoExposure_response.__doc__ = """
Response to command :func:`~microspec.commands.Devkit.autoExposure`.

Attributes
----------
{status}
        If :func:`autoExposure` timed out, consider decreasing
        ``max_tries`` or ``max_exposure``, or consider increasing
        the ``timeout``.

success : :class:`~microspeclib.internal.util.MicroSpecInteger`

  1: SUCCESS
    The peak signal is in the target counts range.

  0: FAILURE
    The peak signal is not in the target counts range.
    Fail for any of the following reasons:

      - reached the maximum number of tries
      - hit maximum exposure time and signal is below target range
      - hit minimum exposure time and signal is above target range

iterations : :class:`~microspeclib.internal.util.MicroSpecInteger`

  Number of exposures tried by auto-expose.
  Valid range: 1-255

  ``iterations`` never exceeds
  :func:`~microspec.commands.Devkit.setAutoExposeConfig`
  parameter ``max_tries``, the maximum number of iterations to
  try.

Notes
-----
{created_from}
:data:`~microspeclib.datatypes.sensor.SensorAutoExposure`.

See Also
--------
~microspec.commands.Devkit.autoExposure
""".format(**_common)

getAutoExposeConfig_response = namedtuple(
        'getAutoExposeConfig_response',
        [
            'status',
            'max_tries',
            'start_pixel',
            'stop_pixel',
            'target',
            'target_tolerance',
            'max_exposure'
         ])
getAutoExposeConfig_response.__doc__ = """
Response to command :func:`~microspec.commands.Devkit.getAutoExposeConfig`.

Attributes
----------
{status}
max_tries
start_pixel
stop_pixel
target
target_tolerance
max_exposure

Notes
-----
{created_from}
:data:`~microspeclib.datatypes.sensor.SensorGetAutoExposeConfig`.

See Also
--------
~microspec.commands.Devkit.getAutoExposeConfig
""".format(**_common)

setAutoExposeConfig_response = namedtuple(
        'setAutoExposeConfig_response',
        ['status']
        )
setAutoExposeConfig_response.__doc__ = """
Response to command :func:`~microspec.commands.Devkit.setAutoExposeConfig`.

Attributes
----------
{status}

Notes
-----
{created_from}
:data:`~microspeclib.datatypes.sensor.SensorSetAutoExposeConfig`.

See Also
--------
~microspec.commands.Devkit.setAutoExposeConfig
""".format(**_common)

.. _dev-kit-API-guide:

Dev-kit API Guide
=================

Two Most Important Docs
-----------------------

These are the two most important pages in the documentation. Keep
them handy when developing applications.

1. :ref:`dev-kit-API-cmd`

  * documents the input arguments for each API command
  * example: the command :py:func:`setExposure
    <microspeclib.simple.MicroSpecSimpleInterface.setExposure>`
    takes input argument ``cycles``

2. :ref:`dev-kit-API-reply`

  * documents the *reply attributes* for each API
    command
  * example: the reply to
    :py:func:`autoExposure <microspeclib.simple.MicroSpecSimpleInterface.autoExposure>`
    has three attributes:

    * ``status``
    * ``success``
    * ``iterations``

API Commands
------------

The API commands are documented here: :ref:`dev-kit-API-cmd`

Command names
^^^^^^^^^^^^^

*API* command names and *automated documentation* command names
look a little different but they refer to the same function
definitions.

For example, API command
:py:func:`autoExposure <microspeclib.simple.MicroSpecSimpleInterface.autoExposure>`
shows up in the automated documentation as
:py:data:`CommandAutoExposure <microspeclib.datatypes.command.CommandAutoExposure>`.

The *automated documentation* uses the *low-level* command names.
These are defined in the dict
``microspeclib.datatypes.command.CHROMASPEC_COMMAND_NAME``. The
command names all start with ``Command``, and the next letter is
capitalized.

*For the curious:* the rename to the familiar API name happens in
``microspeclib.simple._generateFunction()``.

Command arguments
^^^^^^^^^^^^^^^^^

The automated documentation of the arguments is not great.

Please ignore ``=None``:

.. code-block:: python

   setAutoExposeConfig(max_tries=None, start_pixel=None, stop_pixel=None, target=None, target_tolerance=None, max_exposure=None, **kwargs)

When keyword arguments are listed they need values and it is
*never OK* to set an argument to ``None``. Showing ``=None`` is
the best we could automate to convey the idea that the dev-kit
expects values for these arguments.

The expected *type* and *valid range* are described in the
**Parameters** section for each commmand.

Please ignore ``**kwargs``:


.. code-block:: python

   autoExposure(**kwargs)

The ``**kwargs`` shows up in every signature in the
documentation. If an API command only shows ``**kwargs`` (like
this one) it *take no arguments*.

API Replies
-----------

The replies to API commands are documented here:
:ref:`dev-kit-API-reply`.

Return values
^^^^^^^^^^^^^

Every API command gets a reply. This is documented in the
``Returns`` section for each command in :ref:`dev-kit API
commands <dev-kit-API-cmd>`; click the ``Sensor...`` datatype
link.

Every reply has a ``status`` attribute, indicating the status of
the serial communication. Applications do not need to check
``status`` in an attempt to handle communication errors. This
low-level work is handled automatically by ``microspeclib``.

Typical return values
^^^^^^^^^^^^^^^^^^^^^

If serial communication is successful, the reply is a
``Sensor...`` datatype.

When sending ``Bridge`` commands, the reply is a ``Bridge...``
datatype. There are only three ``Bridge`` commands:
:py:func:`getBridgeLED
<microspeclib.simple.MicroSpecSimpleInterface.getBridgeLED>`,
:py:func:`setBridgeLED
<microspeclib.simple.MicroSpecSimpleInterface.setBridgeLED>`, and
:py:func:`null
<microspeclib.simple.MicroSpecSimpleInterface.null>`.

Value returned when communication fails
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the serial communication **fails**, the reply is ``None``.

In practice, a serial communication failure always results from a
timeout. See :ref:`how-to-handle-timeouts`.

Bridge return values are hidden for Sensor commands
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Every command with a ``Sensor`` reply also has a ``Bridge``
reply, but this is only accessible with the
``microspeclib.expert`` interface. These hidden ``Bridge``
replies are not helpful for writing applications. The ``Bridge``
replies are documented in
:py:mod:`microspeclib.datatypes.bridge`.

View API replies at the REPL
----------------------------

Another way to find out what a command returns is by printing its
reply:

* open a Python REPL
* send the command
* print its reply

Example:

.. code-block:: python
   :emphasize-lines: 4

   from microspeclib.simple import MicroSpecSimpleInterface
   kit = MicroSpecSimpleInterface()
   reply = kit.autoExposure()
   print(reply)

Reply:

.. code-block::

   SensorAutoExposure(status=0, success=0, iterations=1)

The values are accessed as ``reply.success``, ``reply.iterations``, etc.

*Every* command reply includes ``status``.

``status`` is part of the *low-level* serial communication data and is safe to
ignore as an API user. For example, Chromation's ``microspecgui`` application
never checks the reply status.

Other Useful Docs
-----------------

Two more useful API references:

1. :ref:`dev-kit-API-const`

  * constants defined by the API
  * example: :py:class:`StatusOK <microspeclib.datatypes.types.StatusOK>`

2. :ref:`dev-kit-API-JSON`

  * this is ``microspec.cfg``, the JSON file that defines the
    protocol agreed upon by the Python API and the dev-kit C
    firmware
  * it is the file that creates it all:

    * the ``microspeclib.simple`` API functions are
      auto-generated from ``microspec.cfg`` and the function
      factory :py:func:`microspeclib.simple._generateFunction`
    * the API function docstrings are auto-generated
      by :py:func:`microspeclib.simple._generateFunction` and
      human-written documentation added via module
      :py:mod:`microspeclib.interal.docstrings`
    * the ``microspec`` unit tests are similarly auto-generated
      from unit test factories



.. _how-to-handle-timeouts:

How to handle timeouts
======================

The default timeout is 2 seconds, but sometimes a command will timeout. If a
command timeouts, the reply is ``None``.

The most likely scenario to encounter a timeout is when acquiring spectra in a
loop. For example, Chromation's ``microspecgui`` is constantly acquiring frames
of spectrum data:

.. code-block:: python

   frame = kit.captureFrame() # acquire a spectrum
   counts = frame.pixels # the signal (in ADC counts) at each pixel

If this application runs for several hours, it is likely to drop a frame at
least once. When that happens ``frame`` is ``None``, raising the Exception:
``NoneType`` has no attribute ``pixels``.

A single dropped frame is not a reason to exit the application. Instead of
quitting, ignore the dropped frame and use the previous value stored in
``counts``:

.. code-block:: python

   frame = kit.captureFrame()
   if frame is not None: counts = frame.pixels


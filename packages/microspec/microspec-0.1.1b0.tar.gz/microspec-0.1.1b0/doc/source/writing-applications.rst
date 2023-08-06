Writing Applications
====================

``microspec`` contains many modules, but for writing applications, there is only
one module that matters: ``microspeclib.simple``.

``microspeclib.simple`` defines class ``MicroSpecSimpleInterface``.
*This class is the API.*

- create an instance of ``MicroSpecSimpleInterface`` to open communication with
  the dev-kit
- communication closes when the application exits, regardless of whether it
  exits normally or by an exception

Applications typically configure the dev-kit in a **setup**, then
acquire spectra in a **loop**:

- setup:

  - set the *pixel configuration* in the spectrometer chip
  - set the *auto-expose parameters* in the dev-kit firmware

**The setup is optional**. The firmware powers-on with the recommended default
values.

- loop:

  - adjust **exposure time**, either *manually* or with *auto-expose*
  - acquire a **spectrum**
  - **save** and/or **plot** the spectrum

*The API only provides commands to control the dev-kit*. Data processing, such
as representing the data in a plot with a wavelength axis, is up to the
application.

Here is an example application that acquires a spectrum and exits:

.. code-block:: python

   # Access the API
   from microspeclib.simple import MicroSpecSimpleInterface

   # Open communication
   kit = MicroSpecSimpleInterface()

   # Set exposure time
   kit.setExposure(500) # 500 cycles * 20µs/cycle = 10ms exposure time

   # Acquire a spectrum
   frame = kit.captureFrame()

   # Guard against dropped frames (important if looping acquisition for hours)
   if frame is not None:
       counts = frame.pixels # the signal (in ADC counts) at each pixel

   # Do something with the spectrum
   print(counts)

   # Communication closes when this application exits.



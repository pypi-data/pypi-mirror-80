"""Module ``microspec`` is the API for the Chromation Spectrometer dev-kit.

.. note::

    You are reading this because you are writing an application that
    uses the Chromation Spectrometer dev-kit.

    If you want a ready-made application that uses the dev-kit, ``pip
    install microspecgui``, then run the application from your
    command line with ``microspec-gui`` (works on Windows, Linux, and
    Mac).

See the API reference docs in :ref:`API`.

See the Chromation dev-kit user guide in
:ref:`chromation-dev-kit`

Install
-------

Install the ``microspec`` project:

.. code-block:: bash

    pip install microspec

This installs the ``microspec`` package and a few command line
utilities. The ``microspec`` package has submodules ``microspec``
and ``microspeclib``. Applications should use the ``microspec``
module.

Usage
-----

Use the ``microspec`` module in an application:

.. code-block:: python

    import microspec
    kit = microspec.Devkit()

Chromation recommends importing ``microspec`` *bound* as ``usp``
to reduce code line length:

.. code-block:: python

    import microspec as usp
    kit = usp.Devkit()
    kit.setBridgeLED(led_setting = usp.OFF)

.. note::

    If you are contributing to ``microspec``, install all the
    development requirements with ``pip install microspec[dev]``.
    See the developer docs for ``microspec`` (this module) and
    for ``microspeclib`` (the module this module is built on top
    of).

"""
from .commands import * # class Devkit
from .constants import * # OK, ERROR, OFF, GREEN, RED, etc.
from .helpers import * # to_cycles(), to_ms()

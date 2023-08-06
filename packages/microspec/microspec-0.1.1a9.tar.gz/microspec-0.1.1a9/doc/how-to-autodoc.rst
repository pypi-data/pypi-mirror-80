The following two examples result in identical output.

In the first example:

- `autoclass::` without any options just pulls the class
  docstring
- adding option `:members:` recursively documents members
- so the one specified class,
  :py:class:`MicroSpecSimpleInterface`, is documented, and all of
  its members are documented by the `:members` option

In the second example:

- `automodule::` without any options just pulls the module docstring
- adding option `:members:` recursively documents members
- module :py:mod:`microspeclib.simple` only has one member, class
  :py:class:`MicroSpecSimpleInterface`, so recursively
  documenting members means :py:class:`MicroSpecSimpleInterface`
  is documented AND the members of
  :py:class:`MicroSpecSimpleInterface` are also documented

The end result is the same: one page of documentation, with the
section title of the ``.rst`` file as its link in the toc.

The is one page of documentation has the one class and all of its
members.

.. code-block:: RST

    .. _dev-kit-API-cmd:

    microspeclib.simple module (dev-kit API commands)
    =================================================

    .. autoclass:: microspeclib.simple.MicroSpecSimpleInterface
       :members:
       :undoc-members:
       :inherited-members:
       :exclude-members: consume, flush, pushback, read, receiveCommand, receiveReply, sendAndReceive, sendCommand, sendReply, write, verify, reset

.. code-block:: RST

    .. _dev-kit-API-cmd:

    microspeclib.simple module (dev-kit API commands)
    =================================================

    .. automodule:: microspeclib.simple
       :members:
       :undoc-members:
       :inherited-members:
       :exclude-members: consume, flush, pushback, read, receiveCommand, receiveReply, sendAndReceive, sendCommand, sendReply, write, verify, reset

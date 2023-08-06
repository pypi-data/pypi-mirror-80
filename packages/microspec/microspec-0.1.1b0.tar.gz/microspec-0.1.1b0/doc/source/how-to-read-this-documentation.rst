How To Read This Documentation
==============================

Best way
--------
The **best way to read the documentation** is right here on *Read
the Docs*. Jump straight to the :ref:`dev-kit-API-guide` or to
the :ref:`dev-kit-API-cmd` reference.

No documentation in the source code
-----------------------------------
Searching the source code fails because the API functions are auto-generated.
Reading the documentation with ``pydoc`` is not recommended because the
docstrings are full of *reStructuredText* markup for hyperlinks.

Other options to read the docs
------------------------------
``pydoc`` is handy if you are offline and did not download a copy
of the docs from *Read the Docs*. The docstrings are full of
``reST`` markup, but at least they are formatted in the NumPy
style.

Read at the command line with pydoc:

.. code-block:: bash

   python -m pydoc microspeclib.simple._MicroSpecSimpleInterface

Or in a browser:

.. code-block:: bash

   python -m pydoc -b



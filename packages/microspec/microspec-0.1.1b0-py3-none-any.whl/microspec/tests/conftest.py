"""Test fixtures for module microspec.

The test fixture ``kit`` opens communication with the dev-kit
once at the beginning of the pytest session and closes
communication at the end of the session.

To see this in action, run pytest with the flag ``-s``.

Example
-------

Create the fixture for the entire pytest session:

.. code-block:: python

    @pytest.fixture(scope="session")
    def kit(): return usp.Devkit()

The fixture is defined in ``conftest.py`` to make it accessible
to all test modules.

Use the fixture to pass the dev-kit handle to a test:

.. code-block:: python

    class TestCommandName():
        def test_Call_commandName_with_default_values(self, kit):
            assert kit.commandName().status == 'OK'

To add setup/teardown, use ``yield`` instead of
``return`` in the pytest fixture:

.. code-block:: python

    print("\nsetup.")   # runs at beginning of scope
    yield usp.Devkit()  # yielded object is in memory for the duration of scope
    print("\nteardown") # runs at end of scope

Since the scope is ``session``, the setup runs at the start of
the session, the teardown runs at the end of the session.

To run setup and teardown for every test, create another fixture
using the default scope (the decorator is just
``@pytest.fixture()``) and pass the fixture to the test in the
same way. A lone ``yield`` statement does not pass an object to
the test but still acts to separate the setup code from the
teardown code.

Test teardown
-------------
See the pytest documentation:
https://docs.pytest.org/en/latest/fixture.html#fixture-finalization-executing-teardown-code

    all the code after the ``yield`` statement serves as the
    teardown code

Test setup
----------
Similarly, the code before the ``yield`` statement serves as
the setup code.

To see setup/teardown print statements on stdout, run pytest with
flag ``-s`` (same as ``--capture=no``):
https://docs.pytest.org/en/stable/capture.html
"""
import pytest
import microspec as usp

@pytest.fixture(scope="session")
def kit(): # simpler version
    """Open communication with the dev-kit once for all tests."""
    return usp.Devkit()

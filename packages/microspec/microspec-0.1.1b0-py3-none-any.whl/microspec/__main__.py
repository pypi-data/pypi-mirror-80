# -*- coding: utf-8 -*-
"""``__main__.py`` -- Doctest runner.

Run all doctests::

    python -m microspec

"""

import microspec
import doctest
def _print_all_tests(submodules, FLAGS):
    """Run doctest examples in each submodule and print each test.
    """
    for submod in submodules:
        doctest.testmod(m=getattr(microspec,submod), verbose=True, optionflags=FLAGS)
    # doctest.testmod(m=microspec.commands,  verbose=True, optionflags=FLAGS)
    # doctest.testmod(m=microspec.replies,   verbose=True, optionflags=FLAGS)
    # doctest.testmod(m=microspec.constants, verbose=True, optionflags=FLAGS)
    # doctest.testmod(m=microspec.helpers,   verbose=True, optionflags=FLAGS)
def _print_summary(submodules, FLAGS):
    """Run doctest examples in each submodule and print a summary only.
    
    Parameters
    ----------
    submodules : list
        List the names of the submodules to doctest:
        ['sub1', 'sub2', etc.]
    FLAGS
        Doctest flags.
    """
    print("Running doctest examples...\n")
    print(f"{'module'   :10}| doctest results")
    print(f"{'------'   :10}| ---------------")
    for submod in submodules:
        print(f"{submod :10}| {doctest.testmod(m=getattr(microspec,submod),  optionflags=FLAGS)}")
def run_doctest_examples(submodules: list, FLAGS, verbose=False):
    """Run the doctest examples in all the microspec submodules.

    With verbose=True, this behaves identical to calling
    doctest.testmod() on each microspec submodule.

    With verbose=False, only the summary of test results is printed.

    The default verbose=False behavior of doctest is to print nothing.
    This function modifies that behavior by collecting the test
    summaries and printing them in a table.
    """
    if verbose: _print_all_tests(submodules, FLAGS)
    else: _print_summary(submodules, FLAGS)
run_doctest_examples(
        submodules = ['commands', 'replies', 'constants', 'helpers'],
        # submodules = ['helpers'],
        # submodules = [],
        FLAGS = doctest.ELLIPSIS | doctest.FAIL_FAST | doctest.NORMALIZE_WHITESPACE,
        verbose=False
        )

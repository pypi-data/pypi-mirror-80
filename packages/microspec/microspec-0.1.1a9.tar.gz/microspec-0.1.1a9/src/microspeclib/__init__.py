import os

__copyright__ = """Copyright 2020 Chromation, Inc"""
__license__   = """All Rights Reserved by Chromation, Inc"""
__doc__       = """
see API documentation: 'python -m pydoc microspeclib.simple'
"""


# NOTE: Sphinx ignores __init__.py files, so for generalized documentation,
#       please use pydoc, or the sphinx-generated documents in doc/build,
#       or the README.md file

# NOTE on CHROMASPEC_ROOTDIR
#
# It is specifically located in the __init__.py of the base microspeclib
# package, so that the ../ (src) ../ (microspec) directory can be found,
# so that, in turn, the cfg and other directories can be referenced
# programmatically and without relative references throughout the
# packages. The test system can find root package directories, but the
# runtime system has no standard for this, and we are avoiding utilizing
# a test system for runtime use.
#
# If microspeclib is in /foo/bar/microspec/src/microspeclib then
# CHROMASPEC_ROOTDIR will be /foo/bar/microspec

CHROMASPEC_ROOTDIR = os.path.realpath(
                       os.path.join(
                         os.path.dirname(__file__), # microspeclib
                         "..",                        # src
                         ".."                         # microspec
                       )
                     )


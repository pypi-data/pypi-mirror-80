
# Copyright 2020 by Chromation, Inc
# All Rights Reserved by Chromation, Inc

import unittest, os, pytest, sys
from timeit import default_timer as timer
from test_simple_interface         import MicroSpecTestSimpleInterface
from microspeclib.simple          import MicroSpecSimpleInterface
from microspeclib.datatypes       import *

@pytest.mark.skipif(sys.platform not in ["darwin","linux"], reason="Emulation currently only runs on linux and MacOS")
class MicroSpecTestSimpleInterfaceEmulator(MicroSpecTestSimpleInterface):
  __test__ = True

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  @classmethod
  def setUpClass(cls):
    super().setUpClass()
    cls.software = MicroSpecSimpleInterface(emulation=True, timeout=1)












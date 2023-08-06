
# Copyright 2020 by Chromation, Inc
# All Rights Reserved by Chromation, Inc

import unittest, os, pytest
from timeit import default_timer as timer
from test_expert_interface    import MicroSpecTestExpertInterface
from microspeclib.expert     import MicroSpecExpertInterface
from microspeclib.datatypes  import *
from microspeclib.exceptions import *

@pytest.mark.xfail(raises=MicroSpecConnectionException, strict=False, reason="Hardware not connected")
class MicroSpecTestExpertInterfaceHardware(MicroSpecTestExpertInterface):
  __test__ = True

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  @classmethod
  def setUpClass(cls):
    super().setUpClass()
    cls.hardware = None
    if not hasattr(cls, "software"):
      cls.software = MicroSpecExpertInterface(timeout=0.1)

  @classmethod
  def tearDownClass(cls):
    super().tearDownClass()
    if hasattr(cls, "software"):
      del cls.software











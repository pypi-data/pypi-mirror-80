
# Copyright 2020 by Chromation, Inc
# All Rights Reserved by Chromation, Inc

import unittest, os, pytest, copy
from microspeclib.internal.payload import MicroSpecPayloadClassFactory, MicroSpecPayload, MicroSpecRepeatPayload

class MicroSpecTestPayloadFactory(unittest.TestCase):

  def test_payloadFactoryNormal(self):
    klass = MicroSpecPayloadClassFactory("command", 99, "grok", ["command_id","foo","bar","baz"], [1,1,2,4])
    assert klass.command_id == 99
    assert klass.__name__   == "grok"
    assert klass.variables  == ["command_id","foo","bar","baz"]
    assert klass.sizes      == [1,1,2,4]

  def test_payloadFactoryRepeat(self):
    klass = MicroSpecPayloadClassFactory("command", 99, "grok", ["command_id","foo","bar","baz"], [1,1,2,4], repeat={"foo":"bar"})
    assert klass.command_id == 99
    assert klass.__name__   == "grok"
    assert klass.variables  == ["command_id","foo","bar","baz"]
    assert klass.sizes      == [1,1,2,4]
    assert klass.repeat     == {"foo":"bar"}

class MicroSpecTestPayload(unittest.TestCase):

  def __init__(self, *args, **kwargs):
    super(MicroSpecTestPayload, self).__init__(*args, **kwargs)
    self.klass = MicroSpecPayloadClassFactory("command", 99, "grok", ["command_id","foo","bar","baz"], [1,1,2,4])

  def test_initEmpty(self):
    obj = self.klass()
    assert obj.foo        == None
    assert obj.bar        == None
    assert obj.baz        == None
    assert obj.command_id == 99
    assert obj.variables  == ["command_id","foo","bar","baz"]
    assert obj.sizes      == [1,1,2,4]

  def test_initKwargs(self):
    obj = self.klass(foo=1,bar=2,baz="0xFF")
    assert obj.foo        == 1
    assert obj.bar        == 2
    assert obj.baz        == 255
    assert obj.command_id == 99
    assert obj.variables  == ["command_id","foo","bar","baz"]
    assert obj.sizes      == [1,1,2,4]

  def test_initPayload(self):
    obj = self.klass(b'\x63\x01\x00\x02\x00\x00\x00\xFF')
    assert obj.foo        == 1
    assert obj.bar        == 2
    assert obj.baz        == 255
    assert obj.command_id == 99
    assert obj.variables  == ["command_id","foo","bar","baz"]
    assert obj.sizes      == [1,1,2,4]

  def test_unpack(self):
    obj = self.klass()
    obj.unpack(b'\x63\x01\x00\x02\x00\x00\x00\xFF')
    assert obj.foo        == 1
    assert obj.bar        == 2
    assert obj.baz        == 255
    assert obj.command_id == 99
    assert obj.variables  == ["command_id","foo","bar","baz"]
    assert obj.sizes      == [1,1,2,4]

  def test_iter(self):
    obj = self.klass(b'\x63\x01\x00\x02\x00\x00\x00\xFF')
    var = []
    for v in obj:
      var.append(v)
    assert var == ["command_id","foo","bar","baz"]

  def test_repr(self):
    obj = self.klass(b'\x63\x01\x00\x02\x00\x00\x00\xFF')
    s   = """<grok name=grok command_id=99 variables=['command_id', 'foo', 'bar', 'baz'] values={'command_id': 99, 'foo': 1, 'bar': 2, 'baz': 255} sizes=[1, 1, 2, 4] packformat=>BBHL length=8 packed=b'c\\x01\\x00\\x02\\x00\\x00\\x00\\xff'>"""
    assert repr(obj) == s

  def test_str(self):
    obj = self.klass(b'\x63\x01\x00\x02\x00\x00\x00\xFF')
    s   = """grok(command_id=99, foo=1, bar=2, baz=255)"""
    assert str(obj) == s

  def test_bytes(self):
    b = b'\x63\x01\x00\x02\x00\x00\x00\xFF'
    obj = self.klass(b)
    assert bytes(obj) == b

  def test_len(self):
    b = b'\x63\x01\x00\x02\x00\x00\x00\xFF'
    obj = self.klass(b)
    assert len(bytes(obj)) == len(b)

  def test_packformat(self):
    obj = self.klass(b'\x63\x01\x00\x02\x00\x00\x00\xFF')
    assert obj.packformat() == ">BBHL"

  def test_packvalues(self):
    obj = self.klass(b'\x63\x01\x00\x02\x00\x00\x00\xFF')
    assert obj.packvalues() == [99, 1, 2, 255]

  def test_pack(self):
    b = b'\x63\x01\x00\x02\x00\x00\x00\xFF'
    obj = self.klass(b)
    assert obj.pack() == b

  def test_equals(self):
    b = b'\x63\x01\x00\x02\x00\x00\x00\xFF'
    obj = self.klass(b)
    ob2 = self.klass(b)
    assert obj == ob2

    ob2.name = "fii"
    assert obj == ob2

    ob2 = self.klass(b)
    ob2.varsize[0] = 999
    assert obj != ob2

    ob2 = self.klass(b)
    ob2.command_id = 999
    assert obj == ob2

    ob2 = self.klass(b)
    ob2.variables = ["a","b","c","d"]
    assert obj == ob2

    ob2 = self.klass(b)
    ob2.sizes = [999,999,999,999]
    assert obj == ob2

  def test_packValues(self):
    obj = self.klass(foo=1, bar=2, baz=255)
    assert bytes(obj) == b'\x63\x01\x00\x02\x00\x00\x00\xFF'

  def test_packValuesMissing(self):
    obj = self.klass(foo=1, bar=2)
    assert bytes(obj) == b''

    obj = self.klass(foo=1, baz=255)
    assert bytes(obj) == b''

    obj = self.klass(bar=2, baz=255)
    assert bytes(obj) == b''

class MicroSpecTestRepeatPayload(MicroSpecTestPayload):

  def __init__(self, *args, **kwargs):
    super(MicroSpecTestRepeatPayload, self).__init__(*args, **kwargs)
    self.klass = MicroSpecPayloadClassFactory("command", 99, "grok", ["command_id","foo","bar","baz"], [1,1,2,4], repeat={"baz": "foo"})

  def test_initEmpty(self):
    obj = self.klass()
    assert obj.foo        == None
    assert obj.bar        == None
    assert obj.baz        == []
    assert obj.command_id == 99
    assert obj.variables  == ["command_id","foo","bar","baz"]
    assert obj.sizes      == [1,1,2,4]
    assert obj.repeat     == {"baz": "foo"}

  def test_initKwargs(self):
    obj = self.klass(foo=3,bar=2,baz=["0xFF",0,17])
    assert obj.foo        == 3
    assert obj.bar        == 2
    assert obj.baz        == [255,0,17]
    assert obj.command_id == 99
    assert obj.variables  == ["command_id","foo","bar","baz"]
    assert obj.sizes      == [1,1,2,4]
    assert obj.repeat     == {"baz": "foo"}

  def test_initPayload(self):
    obj = self.klass(b'\x63\x03\x00\x02\x00\x00\x00\xFF\x00\x00\x00\x00\x00\x00\x00\x11')
    assert obj.foo        == 3
    assert obj.bar        == 2
    assert obj.baz        == [255,0,17]
    assert obj.command_id == 99
    assert obj.variables  == ["command_id","foo","bar","baz"]
    assert obj.sizes      == [1,1,2,4]
    assert obj.repeat     == {"baz": "foo"}

  def test_unpack(self):
    obj = self.klass()
    obj.unpack(b'\x63\x03\x00\x02\x00\x00\x00\xFF\x00\x00\x00\x00\x00\x00\x00\x11')
    assert obj.foo        == 3
    assert obj.bar        == 2
    assert obj.baz        == [255,0,17]
    assert obj.command_id == 99
    assert obj.variables  == ["command_id","foo","bar","baz"]
    assert obj.sizes      == [1,1,2,4]

  def test_repr(self):
    obj = self.klass(b'\x63\x03\x00\x02\x00\x00\x00\xFF\x00\x00\x00\x00\x00\x00\x00\x11')
    s   = """<grok name=grok command_id=99 variables=['command_id', 'foo', 'bar', 'baz'] values={'command_id': 99, 'foo': 3, 'bar': 2, 'baz': [255, 0, 17]} sizes=[1, 1, 2, 4] packformat=>BBHLLL length=8 packed=b'c\\x03\\x00\\x02\\x00\\x00\\x00\\xff\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x11'>"""
    assert repr(obj) == s

  def test_str(self):
    obj = self.klass(b'\x63\x03\x00\x02\x00\x00\x00\xFF\x00\x00\x00\x00\x00\x00\x00\x11')
    s   = """grok(command_id=99, foo=3, bar=2, baz=[255, 0, 17])"""
    assert str(obj) == s

  def test_packformat(self):
    obj = self.klass(b'\x63\x03\x00\x02\x00\x00\x00\xFF\x00\x00\x00\x00\x00\x00\x00\x11')
    assert obj.packformat() == ">BBHLLL"

  def test_tooFewData(self):
    obj = self.klass(b'\x63\x03\x00\x02\x00\x00\x00\xFF\x00\x00\x00\x00\x00\x00\x00\x11')
    obj.foo = 4
    # NOTE: the "repeat" number doesn't follow the list
    #       and if the number is too large for the data, it will throw an exception
    assert obj.foo        == 4
    assert obj.baz        == [255,0,17]
    with pytest.raises(Exception) as excinfo:
      b = bytes(obj)
    assert "pack expected 7 items for packing (got 6)" in str(excinfo.value)

  def test_tooManyData(self):
    obj = self.klass(b'\x63\x03\x00\x02\x00\x00\x00\xFF\x00\x00\x00\x00\x00\x00\x00\x11')
    obj.foo = 4
    obj.baz = [255,0,17,42,99]
    # NOTE: the "repeat" number doesn't follow the list
    #       though the list does get chopped at bytes() or pack() time
    assert obj.foo        == 4
    assert obj.baz        == [255,0,17,42,99]
    b = bytes(obj)
    assert b == b'\x63\x04\x00\x02\x00\x00\x00\xFF\x00\x00\x00\x00\x00\x00\x00\x11\x00\x00\x00\x2A'

  def test_equals(self):
    super().test_equals()
    b = b'\x63\x01\x00\x02\x00\x00\x00\xFF'
    obj = self.klass(b)
    ob2 = self.klass(b)
    ob2.repeat = "xxx"
    assert obj == ob2

  def test_packValues(self):
    obj = self.klass(foo=1, bar=2, baz=[255])
    assert bytes(obj) == b'\x63\x01\x00\x02\x00\x00\x00\xFF'

  def test_packValuesMissing(self):
    obj = self.klass(foo=1, bar=2)
    with pytest.raises(Exception) as excinfo:
      b = bytes(obj)
    assert "pack expected 4 items for packing (got 3)" in str(excinfo.value)

    obj = self.klass(foo=1, baz=[255])
    assert bytes(obj) == b''

    obj = self.klass(bar=2, baz=[])
    assert bytes(obj) == b''












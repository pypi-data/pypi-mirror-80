
# Copyright 2020 by Chromation, Inc
# All Rights Reserved by Chromation, Inc

from microspeclib.logger import CHROMASPEC_LOGGER_PAYLOAD as log
from .util       import *
from .docstrings import *
from struct      import unpack, pack
import itertools
import re

class MicroSpecPayload(object):
  def _init(self, payload=None, **kwargs):
    log.info("payload=%s kwargs=%s", payload, kwargs)
    self.varsize = {}
    for n in range(0, len(self.variables)):
      log.debug("n=%d", n)
      var   = self.variables[n]
      value = kwargs.get(var, None)
      self.varsize[var] = self.sizes[n]
      setattr(self, var, value)
      log.debug("value[%s]=%s size[%s]=%d", var, value, var, self.sizes[n])
    if payload:
      self.unpack(payload)
    log.info("return")

  def __getitem__(self, attr):
    return getattr(self, attr)

  def __setitem__(self, attr, value):
    setattr(self, attr, value)

  def __setattr__(self, attr, value):
    log.info("attr=%s value=%s", attr, value)
    if attr in self.const:
      pass
    elif attr in self.variables and value is not None:
      self.__dict__.update({attr: MicroSpecInteger(dehex(value), self.varsize[attr])})
    else:
      self.__dict__[attr] = value
    log.info("return")

  def __iter__(self):
    log.info("return")
    return iter(self.variables)

  def __repr__(self):
    log.info("")
    s = "<%s name=%s command_id=%s variables=%s values=%s sizes=%s packformat=%s length=%d packed=%s>" % \
      (self.__class__.__name__, self.name, self.command_id, self.variables, \
        self.values(), self.sizes, self.packformat(), \
        len(self), self.pack())
    log.info("return %s", s)
    return s

  def __str__(self):
    log.info("")
    s = "%s(%s)" % (self.__class__.__name__, \
        ", ".join(["%s=%s"%(k, v) for k, v in self.values().items()]))
    log.info("return %s", s)
    return s

  def csv(self):
    log.info("")
    s = "%s,%s"%(self.__class__.__name__, \
          ",".join([ str(s) for s in flatten(self.values().items()) ])
        )
    log.info("return %s", s)
    return s

  def __bytes__(self):
    log.info("")
    b = self.pack()
    log.info("return %s", b)
    return b

  def __len__(self):
    log.info("")
    l = sum(self.sizes)
    log.info("return %s", l)
    return l

  def values(self):
    log.info("")
    v = {k: getattr(self, k) for k in self.variables}
    log.info("return %s", v)
    return v
    
  def packformat(self):
    log.info("")
    packformat = ">"
    for v in self.variables:
      log.debug("packformat=%s varsize[%s]=%d", packformat, v, self.varsize[v])
      packformat += "B" if self.varsize[v] == 1 else \
                    "H" if self.varsize[v] == 2 else \
                    "L" if self.varsize[v] == 4 else \
                    str(  self.varsize[v]) + "s"
    log.info("return %s", packformat)
    return packformat

  def packvalues(self):
    log.info("")
    pv = [getattr(self, v) for v in self.variables]
    log.info("return %s", pv)
    return pv

  def pack(self):
    log.info("")
    if None in self.values().values():
      log.warning("Marshalling a payload that is missing values, returning ''");
      return b''
    p = pack(self.packformat(), *self.packvalues())
    log.info("return %s", p)
    return p

  def unpack(self, payload):
    log.info("payload=%s", payload)
    # The payload may be bigger than needed, to accommodate
    #   chopping data down packet by packet
    length = len(self)
    values = unpack(self.packformat(), payload[0:length])
    log.debug("unpacked values=%s", values)
    for n in range(0, len(values)):
      log.debug("variables[%d]=%s <- values[%d]=%s", n, self.variables[n], n, values[n])
      setattr(self, self.variables[n], values[n])
    p = payload[length:]
    log.info("return %s", p)
    return p

  def __eq__(self, other):
    if not isinstance(other, MicroSpecPayload):
      return NotImplemented
    if self.name       != other.name:       return False
    if self.command_id != other.command_id: return False
    if self.variables  != other.variables:  return False
    if self.values()   != other.values():   return False
    if self.sizes      != other.sizes:      return False
    if self.varsize    != other.varsize:    return False
    return True

class MicroSpecRepeatPayload(MicroSpecPayload):
  """The difference from the parent class is that the repeat process
  requires packing arrays, and requires partially-gradually unpacking
  the payload, since part of the payload defines how much to continue
  to pack and unpack."""

  def _init(self, *args, **kwargs):
    self.__dict__["repeat"] = self.__class__.repeat.copy()
    super()._init(*args,**kwargs)

  def __setattr__(self, attr, value):
    log.info("attr=%s value=%s", attr, value)
    if attr in self.const:
      pass
    elif attr in self.variables:
      repeat = self.repeat.get(attr, None)
      if repeat:
        self.__dict__.update({attr:
          [] if value is None else
          [MicroSpecInteger(dehex(v), self.varsize[attr]) for v in value]
       })
      else:
        self.__dict__.update({attr:
          value if value is None else
          MicroSpecInteger(dehex(value), self.varsize[attr])
       })
    else:
      self.__dict__.update({attr: value})
    log.info("return")

  def __setitem__(self, attr, value):
    setattr(self, attr, value)

  def packformat(self):
    log.info("")
    packformat = ">"
    for v in self.variables:
      log.debug("packformat=%s v=%s", packformat, v)
      pf = "B" if self.varsize[v] == 1 else \
           "H" if self.varsize[v] == 2 else \
           "L" if self.varsize[v] == 4 else \
           str(  self.varsize[v]) + "s"
      repeat = self.repeat.get(v, None)
      log.debug("repeat=%s", repeat)
      if repeat:
        repeat_num = self[repeat]
        log.debug("repeat_num=%s", repeat_num)
        pf = pf * int(repeat_num if repeat_num is not None else 1)
      packformat += pf
    log.info("return %s", packformat)
    return packformat

  def packvalues(self):
    log.info("")
    pv = list(itertools.chain.from_iterable(
             [  getattr(self, v)[0:int(self[self.repeat.get(v)])] 
               if self.repeat.get(v,None) else
                 [getattr(self, v)]
               for v in self.variables]
          ))
    log.info("return %s", pv)
    return pv

  def unpack(self, payload): 
    log.info("payload=%s",payload)
    # The payload may be bigger than needed, to accommodate
    # chopping data down packet by packet
    packformat = super().packformat()
    # The superclass packformat doesn't repeat, so it's used to iterate through
    # the elements one at a time, whereas the pack function can pack everything
    # at once
    endian     = packformat[0]
    packrest   = packformat[1:]
    payrest    = payload[:]
    log.debug("packformat=%s payrest=%s",packformat,payrest)
    used   = 0
    for n in range(0, len(self.variables)):
      repeat = self.repeat.get(self.variables[n], None)
      log.debug("packformat=%s payrest=%s n=%d repeat=%s variables[%d]=%s", 
                packformat, payrest, n, repeat, n, self.variables[n])
      if repeat:
        size     = self.sizes[n]
        number   = int(self[repeat])
        packmany = packrest[0] * number
        log.debug("if-repeat size=%d number=%d packmany=%s", size, number, packmany)
        value    = unpack(endian+packmany, payrest[0:size*number])
        log.debug("value=%s", value)
        used    += size*number
        packrest = packrest[1:]
        payrest  = payrest[size*number:]
        log.debug("used=%d packrest=%s payrest=%s", used, packrest, payrest)
        setattr(self, self.variables[n], value)
      else:
        size     = self.sizes[n]
        log.debug("if-no-repeat size=%d", size)
        value    = unpack(endian+packrest[0], payrest[0:size])
        log.debug("value=%s", value)
        used    += size
        packrest = packrest[1:]
        payrest  = payrest[size:]
        log.debug("used=%d packrest=%s payrest=%s", used, packrest, payrest)
        setattr(self, self.variables[n], value[0])
    p = payload[used:]
    log.info("return %s", p)
    return p

  def __eq__(self, other):
    if not isinstance(other, MicroSpecRepeatPayload):
      log.info("return NotImplemented")
      return NotImplemented
    if not super().__eq__(other):   
      log.info("return False")
      return False
    if self.repeat != other.repeat: 
      log.info("return False")
      return False
    log.info("return True")
    return True

def MicroSpecPayloadClassFactory(protocol, command_id, name, variables, sizes, repeat=None):
  log.info("protocol=%s command_id=%d name=%s variables=%s sizes=%s repeat=%s", 
           protocol, command_id, name, variables, sizes, repeat)

  # First, form Voltron - er, the base class
  #
  # The classes don't differ based on protocol (i.e. command vs bridge vs sensor)
  #
  # However, they do need to pull out the variables and add them to the list of
  # attributes, hence the **dict(...for v in variables...)
  if repeat:
    klass = type(str(name), (MicroSpecRepeatPayload,), dict({
      'command_id'   : int(command_id),
      'name'         : name,
      'variables'    : variables,
      'sizes'        : sizes,
      'repeat'       : repeat,
      'const'        : ['command_id', 'name', 'variables', 'sizes', 'repeat', 'const'],
    }, **dict([[v, None] for v in variables if v != "command_id"])))
  else:
    klass = type(str(name), (MicroSpecPayload,), dict({
      'command_id'   : int(command_id),
      'name'         : name,
      'variables'    : variables,
      'sizes'        : sizes,
      'const'        : ['command_id', 'name', 'variables', 'sizes', 'const'],
    }, **dict([[v, None] for v in variables if v != "command_id"])))

  # Then create a custom __init__ function with the proper optional parameters, so
  # that documentation can pull out data via introspection later
  kwarg_param = "".join(["%s=None, "%(v) for v in variables if v != "command_id"])
  kwarg_data  = "".join(["%s=%s, "%(v,v) for v in variables if v != "command_id"])
  scope = locals().copy()
  exec("""def __init__(self, *args, %s**kwargs):
    self._init(*args, %s**kwargs)
  """%(kwarg_param, kwarg_data), scope)
  klass.__init__ = scope["__init__"]
  klass.__init__.__qualname__ = "%s.__init__"%(name)

  # And finally insert the docstrings from the internal library, taking care to not
  # assume the docs exist
  klass.__doc__ = CHROMASPEC_DYNAMIC_DOC.get(protocol, {}).get(str(name), "")

  log.info("return %s", klass)
  return klass

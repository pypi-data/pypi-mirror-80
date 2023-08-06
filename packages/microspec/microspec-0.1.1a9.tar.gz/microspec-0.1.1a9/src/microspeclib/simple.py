
# Copyright 2020 by Chromation, Inc
# All Rights Reserved by Chromation, Inc

from microspeclib.expert              import MicroSpecExpertInterface
from microspeclib.logger              import CHROMASPEC_LOGGER as log
from microspeclib.datatypes.command   import CHROMASPEC_COMMAND_NAME
from microspeclib.internal.docstrings import CHROMASPEC_DYNAMIC_DOC
import sys

# The Simple interface doesn't require creating objects or doing any sending and waiting
# loops, instead it simply acts like a hardware object that you query for information

# The names of the methods are the names of the Command objects, but with the first letter
# lowercased. You can also look at the names of the commands in the JSON cfg file, or the
# pydoc for this class.

# NOTE: This class is entirely auto-generated, you won't find the API here. Please refer to
#       the Sphinx documentation.

__all__ = [ "MicroSpecSimpleInterface" ]

def _generateFunction(command):
  cname = command.__name__
  name  = cname[7:8].lower()+cname[8:]
  kwargs_param = "".join(["%s=None, "%(v  ) for v in command.variables if v != "command_id"])
  kwargs_data  = "".join(["%s=%s, "  %(v,v) for v in command.variables if v != "command_id"])

  # Generate the parameter list for the function, so that later, documentation introspection finds it properly
  code = """def func(self, %s**kwargs):
    return self.sendAndReceive(command(%s**kwargs))
  """ % (kwargs_param, kwargs_data)
  scope = locals().copy()
  exec(code, scope)
  func = scope["func"]
  func.__qualname__ = "%s.%s"%("MicroSpecSimpleInterface", name)
  func.__doc__      = CHROMASPEC_DYNAMIC_DOC["command"].get(cname, None)

  return name, func

_MicroSpecSimpleInterface = type('_MicroSpecSimpleInterface',
                                 (MicroSpecExpertInterface,),
                                 dict([_generateFunction(command) for command in CHROMASPEC_COMMAND_NAME.values()]))

class MicroSpecSimpleInterface(_MicroSpecSimpleInterface):
  # NOTE: do not docstring this class, the sendAndReceive is overridden but still an underlying, hidden portion
  #       of the API. To see the interface, look at the Sphinx documentation.
  def sendAndReceive(self, command, *args, **kwargs):
    # Simple interface ignores all other processing or in-progress calls, unlike Expert.
    # They are not compatible interfaces, as Expert can be continued after a failed read,
    # but Simple cannot. Do not intermix their usage.
    #
    # It can still get out of sync, but with enough of a wait, it will catch up next time
    log.info("command=%s args=%s kwargs=%s", command, args, kwargs)
    self.stream.reset_input_buffer()
    self.buffer = b''
    self.current_command = []
    reply = super().sendAndReceive(command, *args, **kwargs)
    self.stream.reset_input_buffer()
    self.buffer = b''
    self.current_command = []
    log.info("return %s", reply)
    return reply



# Copyright 2020 by Chromation, Inc
# All Rights Reserved by Chromation, Inc

from microspeclib.datatypes import CommandNull
from microspeclib.logger    import CHROMASPEC_LOGGER as log
import time

# The intended difference between this and the Simple interface is to provide more
# fine control, such as breaking up sending commands and then looping to wait for
# replies. It requires creating Command objects and then passing them along, in 
# contrast to the one routine per command structure of the Simple interface.

__all__ = [ "MicroSpecExpertInterface" ]

from microspeclib.internal.stream import MicroSpecSerialIOStream, MicroSpecEmulatedStream
class MicroSpecExpertInterface(MicroSpecSerialIOStream):
  def __init__(self, serial_number=None, device=None, timeout=2.0, retry_timeout=0.001, emulation=False, *args, **kwargs):
    log.info("serial_number=%s, device=%s, timeout=%s, retry_timeout=%s, emulation=%s, args=%s, kwargs=%s",
             serial_number, device, timeout, retry_timeout, emulation, args, kwargs)
    if emulation:
      self.emulation = MicroSpecEmulatedStream(socat=True, fork=True, timeout=timeout)
      device = self.emulation.software
    super().__init__(serial_number=serial_number, 
                     device=device, timeout=timeout, 
                     *args, **kwargs)
    self.retry_timeout = retry_timeout
    self.current_command = []
    log.info("return")

  def __setattr__(self, attr, value):
    if attr == "timeout":
      log.info("set timeout to %s", value)
      self.stream.timeout = value
    else:
      self.__dict__[attr] = value
      
  def __getattribute__(self, attr):
    if attr == "timeout":
      log.info("return timeout=%s", self.stream.timeout)
      return self.stream.timeout
    else:
      return super().__getattribute__(attr)
      
  def sendCommand(self, command):
    """Send one command to the sensor, do not wait for a response. You may stack these, and they
    will return in FIFO order later.

    Parameters
    ----------
    command: :py:mod:`CommandObject <microspeclib.datatypes.command>`
      Create one of these objects and pass it as an argument

    Returns
    -------
    None

    """
    log.info("command=%s", command)
    try:
      if bytes(command) == b'':
        log.warning("Error packing payload for command '%s'", str(command))
        raise Exception("Unable to send partial command '%s'"%(str(command)))
    except:
      log.warning("Error packing payload for command '%s'", str(command))
      raise Exception("Unable to send partial command '%s'"%(str(command)))
    super().sendCommand(command)
    log.info("appending command=%s to current_command=%s", command, self.current_command)
    self.current_command.append(command)
    log.info("return")

  def receiveReply(self):
    """Receive one command result command sent. If multiple were sent, receive the next one in FIFO order,
    if available. A failure to retrieve it does not remove it from the queue, but a reply that contains
    a failed status does.

    Returns
    -------
    :py:mod:`BridgeReplyObject <microspeclib.datatypes.bridge>`
    :py:mod:`SensorReplyObject <microspeclib.datatypes.sensor>`

    """
    log.info("waiting for reply")
    start = time.time()
    reply = super().receiveReply(self.current_command[0].command_id) if self.current_command else None
    since = time.time() - start
    timeout = self.timeout if self.timeout else 0
    remain = timeout - since
    log.info("start=%s reply=%s since=%s timeout=%s remain=%s"%(start,reply,since,timeout,remain))
    while reply is None and remain > 0:
      log.info("no reply yet, timeout remaining=%s", remain)
      time.sleep( self.retry_timeout if remain > self.retry_timeout else remain )
      reply = super().receiveReply(self.current_command[0].command_id) if self.current_command else None
      since = time.time() - start
      remain = timeout - since
      log.info("start=%s reply=%s since=%s timeout=%s remain=%s"%(start,reply,since,timeout,remain))
    if reply:
      log.info("popping command since reply was found")
      self.current_command.pop(0)
    log.info("return %s", reply)
    return reply

  def sendAndReceive(self, command):
    """Send one command to the sensor, and receive one command result command sent. 
    If multiple were sent, receive the next one in FIFO order, if available. 
    This does NOT mean that the reply will match the command, if you already sent a command
    that you had not received yet. A failure to retrieve it does not remove it from
    the queue, but a reply that contains a failed status does.

    Parameters
    ----------
    command: :py:mod:`CommandObject <microspeclib.datatypes.command>`
      Create one of these objects and pass it as an argument

    Returns
    -------
    :py:mod:`BridgeReplyObject <microspeclib.datatypes.bridge>`
    :py:mod:`SensorReplyObject <microspeclib.datatypes.sensor>`

    """
    log.info("command=%s", command)
    self.sendCommand(command)
    reply = self.receiveReply()
    log.info("return %s", reply)
    return reply

  def flush(self, timeout=0.1):
    """Tell hardware to finish sending any remaining commands and flush it's communication line,
    then flush the local queue and throw away all waiting replies. This does not send a Reset command."""
    log.info("flushing stream by sending a null and clearing all data from the line")
    self.sendCommand(CommandNull())
    old_timeout = self.timeout
    self.timeout = timeout
    self.stream.read(None)
    self.stream.reset_input_buffer()
    self.buffer = b''
    self.timeout = old_timeout
    self.current_command = []
    log.info("return")

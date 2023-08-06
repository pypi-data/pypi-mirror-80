#!/usr/bin/env python

# Copyright 2020 by Chromation, Inc
# All Rights Reserved by Chromation, Inc

"""
Example Usage
=============

NOTE
----
  You probably never need to run this, unless you really need to turn on debugging trace on the
  emulator in order to see what you're sending to it. Usually, specifying emulator=True is enough
  to use the emulator, in the simple and expert API.

  Also, this will only work on Mac OSX and Linux systems, not on Windows.

Longwinded example
------------------
dir=`mktemp -d`

socat PTY,raw,echo=0,link=$dir/microspec.software PTY,raw,echo=0,link=$dir/microspec.hardware &

microspec_emulator.py -f $dir/microspec.hardware

# Then connect interface to $dir/microspec.software file

# And stop the socat background command, and clean up the $dir and it's contents

Short example
-------------
microspec_emulator.py -s -p

# Then connect interface to filename that the script prints to stdout

"""

def main():
  import sys
  import argparse
  parser = argparse.ArgumentParser(
    description="Create software instance of Chromation hardware for use with testing access software")
  parser.add_argument("-v", "--verbose", help="Print verbose trace",                action="count", default=0)
  parser.add_argument("-d", "--debug",   help="Internal debugging",                 action="count", default=0)
  parser.add_argument("-p", "--print",   help="Print socket to connect to",         action="count", default=0)
  parser.add_argument("-t", "--timeout", help="Timeout in (partial float) seconds", nargs=1,        default=[0],
                                                                                    action="store", type=float)
  parser.add_argument("-s", "--spawn",   help="Spawn socat instance?",              action="count", default=False)
  parser.add_argument("-f", "--file",    help="File to use as a pipe - default create anew and print location", 
                                                                                                    default=None)
  args = parser.parse_args()

  from microspeclib.internal.emulator import MicroSpecEmulator
  from microspeclib.internal.stream   import MicroSpecEmulatedStream
  from microspeclib.logger            import debug
  import logging
  
  log = logging.getLogger("microspec_emulator")
  if args.verbose or args.debug: 
    debug( args.debug>0 )
    log.setLevel( logging.DEBUG )
  
  serial   = MicroSpecEmulatedStream(hardware=args.file, timeout=args.timeout[0], socat=args.spawn, fork=False)
  emulator = MicroSpecEmulator()
  
  if args.file is None or args.print:
    print("%s"%(serial.software))
    # Note: necessary so that the emulator object that spawns this program and waits for some input
    # on stdout definitely gets data, otherwise it gets stuck in the buffer and never triggers select:
    sys.stdout.flush() 
  
  while True:
    log.info("Waiting for command...")
    command = serial.receiveCommand()
    if not command:
      log.info("No command found")
      continue
    log.info("Received command %s"%(command))
    reply = emulator.process(command)
    if reply:
      log.info("Sending reply %s"%(reply))
      for packet in reply:
        serial.sendReply(packet)
    else:
      log.info("No reply to send")

if __name__ == "__main__":
  main()

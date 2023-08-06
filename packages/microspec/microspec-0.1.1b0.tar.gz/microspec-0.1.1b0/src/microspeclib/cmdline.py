
# Copyright 2020 by Chromation, Inc
# All Rights Reserved by Chromation, Inc

from microspeclib.simple            import MicroSpecSimpleInterface
from microspeclib.logger            import debug, CHROMASPEC_LOGGER as log
from microspeclib.datatypes.command import CHROMASPEC_COMMAND_NAME as commands
from microspeclib.datatypes.types   import CHROMASPEC_GLOBAL       as constants
import time, datetime, sys

# NOTE: There is no docstring because the Sphinx documentation runs the argparse help and creates the
#       documentation there. See the Sphinx documentation for the microspec_cmdline.py executable.

cmdname = dict([ [s[7:].lower(), s[7:]] for s    in commands.keys() ])
cstname = dict([ [s    .lower(), v    ] for s, v in constants.items() ])

def get_command(c):
  return cmdname.get(c.lower())

def get_constant(c):
  return cstname.get(c.lower(), c)

def print_format(csv, response):
  current_time = datetime.datetime.now().strftime("%Y-%m-%dT%T.%f%z")
  if response is None:
    print("%s,%s"%(current_time,None))
  elif csv:
    print("%s,%s"%(current_time,response.csv()))
  else:
    print("%s,%s"%(current_time,str(response)))

def command_help_string():
  cmdstring = "List of commands and arguments:\n"
  for cname, cmd in commands.items():
    cmdstring += "  %-17s %s\n"%(cname[7:], " ".join(["%s=xxx"%(k) for k in cmd().variables if k != "command_id"]))
  cmdstring += "\nNote that command names are case-insensitive. For more information on each command, run `pydoc microspeclib.datatypes.command`"
  return cmdstring

if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser(
    description="Command line interface for MicroSpecLib", 
    epilog=command_help_string(),
    formatter_class=argparse.RawDescriptionHelpFormatter )
  parser.add_argument("-d", "--debug",    help="Internal debugging trace",           action="count", default=0    )
  parser.add_argument("-v", "--verbose",  help="Verbose trace",                      action="count", default=0    )
  parser.add_argument("-t", "--timeout",  help="Timeout (seconds)",                  type=float,     default=0.1  )
  parser.add_argument("-r", "--repeat",   help="Repeat N times, 1=once, 0=forever",  type=int,       default=1    )
  parser.add_argument("-w", "--wait",     help="Wait inbetween repeats (seconds)",   type=float,     default=1.0  )
  parser.add_argument("-e", "--emulator", help="Spawn emulator and connect to that", action="count", default=0    )
  parser.add_argument("-f", "--file",     help="File/socket/device to connect to, "+
                                               "default=auto-detect hardware",                       default=None )
  parser.add_argument("-c", "--csv",      help="Print-format: 'default' or 'csv'",   action="count", default=0    )
  parser.add_argument("command",          help="Command to send",                                                 )
  parser.add_argument("arguments",        help="Key=value pairs for command",        nargs="*",      default=[]   )
  import sys
  if "-i" in sys.argv or "--ignore" in sys.argv:
    parser.add_argument("-i", "--ignore", help="Ignore argument") # hidden argument for internal use
  args = parser.parse_args()
  
  from microspeclib.internal.stream import MicroSpecEmulatedStream
  from microspeclib.logger          import debug
  if args.debug or args.verbose: 
    debug(args.debug>0)

  timeout = args.timeout

  si = None
  if args.emulator:
    log.info("Starting emulation process...")
    hardware = MicroSpecEmulatedStream(socat=True, fork=True, timeout=0.1)
    software = MicroSpecSimpleInterface(device=hardware.software, timeout=timeout)
    log.info("Connecting to emulation")
    si       = software
  elif args.file:
    log.info("Connecting to device '%s'", args.file)
    si       = MicroSpecSimpleInterface(device=args.file, timeout=timeout)
  else:
    log.info("Connecting to default hardware")
    si       = MicroSpecSimpleInterface(timeout=timeout)

  try:
    getcmd  = get_command(args.command)
    command = getcmd[0].lower() + getcmd[1:]
  except:
    log.critical("Command '%s' not found!\n%s", args.command, command_help_string())
    sys.exit(1)

  try:
    kwargs  = dict([ [s.split("=")[0],get_constant(s.split("=")[1])]  for s in args.arguments ])
  except:
    log.critical("Error parsing arguments '%s'", str(args.arguments))
    sys.exit(1)

  i = 0
  while (True if args.repeat < 0 else i < args.repeat):
    log.info("Executing command %s(%s)", command, kwargs)
    try:
      reply = getattr(si, command)(**kwargs)
      print_format(args.csv, reply)
    except Exception as e:
      log.error(e)
      print_format(args.csv, None)
    i += 1
    if (True if args.repeat < 0 else i < args.repeat):
      if args.repeat > 0:
        log.info("%d calls remain", args.repeat - i + 1)
      log.info("Waiting %f seconds...", args.wait)
      time.sleep(args.wait)


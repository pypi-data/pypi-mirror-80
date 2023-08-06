#!/usr/bin/env python

"""
Example Usage
=============

In the examples below, Windows users replace ".py" with ".exe".

Capture one frame once
----------------------
microspec_cmdline.py captureframe

Capture a frame 50 times with 2 seconds inbetween
-------------------------------------------------
microspec_cmdline.py captureframe -r 50 -w 2

Capture a frame and print results in csv
----------------------------------------
microspec_cmdline.py captureframe -c

Set the binning to true, gain to 100, and row_bitmap to 010101 (0x15)
---------------------------------------------------------------------
microspec_cmdline.py setsensorconfig binning=1 gain=100 row_bitmap=0x15

Connect to a specific COM4 port
-------------------------------
microspec_cmdline.py -f COM4 ...

Connect to a specific /dev/com123 file
--------------------------------------
microspec_cmdline.py -f /dev/com123 ...

Connect to emulator instead of hardware
---------------------------------------
microspec_cmdline.py -e ...

"""

def main():
  import subprocess, sys
  # subprocess.call(["python", "-m", "microspeclib.cmdline"] + sys.argv[1:])
  # Use sys.executable instead of "python" to see the
  # microspeclib package installed in the active virtual
  # environment.
  subprocess.call([sys.executable, "-m", "microspeclib.cmdline"] + sys.argv[1:])

if __name__ == "__main__":
  main()


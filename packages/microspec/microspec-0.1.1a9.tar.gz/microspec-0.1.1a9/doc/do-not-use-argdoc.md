# Summary

argdoc runs scripts with main-like functions and argument
`--help` to generate documentation for :automdule:.

But this step because causes the build to fail.

If it was just one problematic script, I could skip it: add the
`@noargdoc` decorator to the main-like function def. This adds
the annoyance that running the command line script requires
installing a ton of Sphinx-related packages.

But I had to do this with all (two) of our command line scripts,
so what's the point? Instead of @noargdoc, I just stopped using
the sphinxcontrib-argdoc extension. This is the cleanest
solution.

# Details

argdoc finds two scripts with main-like functions:

  bin/microspec_cmdline.py
  bin/microspec_emulator.py

Add these two lines above `def main()`:

  from sphinxcontrib.argdoc import noargdoc
  @noargdoc
  def main():

The above tells `sphinxcontrib.argdoc.ext.post_process_automodule()`
to skip generating an argument list for the main-like function.

argdoc works by running the command line script with `--help` to
get the list of arguments, then it makes a pretty table in the
documentation where the :automodule: directive is.

It runs the script as python -m bin.microspec_cmdline --help

This runs fine if sys.path includes ../../

According to the conf.py, that is on sys.path, so this SHOULD
find it, but it does not.

From the command line, if I run the script with
PYTHONPATH=../../, I get the same ModuleNotFoundError

This error means the script returns with a non-zero exit status
which is interpreted by the build process as an error. Skip this
step with `@noargdoc` to avoid the error.

Use sphinx-build -vvv (maximum verbosity) to see the actual error. At
default verbosity, the reported error is `No module named 'bin'`
which mistakenly sounds like a `sys.path` problem. This problem has
nothing to do `sys.path`.

The alternative is to do the build as

  $ PYTHONPATH=../ make clean html

It is not clear why this works or how it is different from editing
sys.path in this conf.py.

This is not a viable solution since there is no way to tell "Read the
Docs" to add to PYTHONPATH (other than the conf.py file). Use
the @noargdoc solution instead.


# Code I wrote and erased while working on this...

A failed attempt: only decorate IF Sphinx is installed:

```python
from importlib.util import find_spec
if find_spec("argdoc", package="sphinxcontrib") is not None:
    print("Found argdoc")
    from sphinxcontrib.argdoc import noargdoc
else:
    print("Did not find argdoc")
    def noargdoc(func): func()
@noargdoc
def main():
```

Then in the definition of main, I tried manipulating the args
passed when argdoc runs this script. But then I realized argdoc
needs to pass --help, so this was definitely not the right way to
go.


```python
  # Fake args if running main() during a Sphinx build.
  from sys import argv
  from pathlib import Path
  if Path(argv[0]).name == 'sphinx-build':
    # fake_args = ["-e", "captureframe"]
    fake_args = []
    args = parser.parse_args(fake_args)

  else: # Not a Sphinx build. OK to read actual args.
```

# MicroSpectrometer

This development toolkit contains the setup necessary for enhancing and debugging the microspectrometer library

## Getting Started

Clone the repository:

<https://github.com/microspectrometer/microspec>

## Install Additional Tools

pip install passlib
pip install pypiserver
python -m pip install --upgrade pip setuptools wheel
pip install twine

## Setting up the Environment

Best to make a custom environment with a known Python version. It will make testing easier later, too.
So, first, install pyenv if you have not already:

https://realpython.com/intro-to-pyenv/

Activate that environment, and install python 3.8.

Add microspectrometer/src to your PYTHONPATH and /bin to your PATH:

export PATH=$PATH:microspectrometer/bin
export PYTHONPATH=$PYTHONPATH:microspectrometer/src

## Building Documentation

In the microspectrometer/doc directory lies all the Sphinx documentation. To build that, step into
the doc directory and run the following. Note that this means adding a few things to your PYTHONPATH
*just* for the documentation build, because you don't want the document directory or test directory on
your path normally, but Sphinx needs it to document the test directories.

cd microspectrometer/doc
PATH=$PATH:../bin PYTHONPATH=../src:../:../tests make clean html

## Testing

To test, simply run pytest while the library is properly set up on your PYTHONPATH. Note that the bin
directory does also need to be on your PATH, as is mentioned above, as the emulator functionality
assumes it can get to the emulation executables:

python -m pytest

## Setting up a PIP server

In order to test building a version of the software and upload it, without actually pushing it to a
public pip server, you can run a separate pip server locally and try uploading, and downloading, from there.

Create a couple mandatory directories and a password file:

touch ~/pypiserver-htpasswd
mkdir ~/pypiserver-packages/

Create a user (here literally called username and with incredibly secure password "password"):

htpassword ~/pypiserver-htpasswd username password

Depending on how you upload and download from pipserver, it may ask for this password.

To run:

pypi-server -p 8080 -P ~/pypiserver-htpasswd ~/pypiserver-packages/

Note that this will run in the foreground, so run it in a separate window or in the background.

## Build a New Version

Edit setup.py and change the version='0.0.0' line to a new version number.

Then build it:

python setup.py bdist\_wheel

This will create a new \*-0.0.0-\*.whl file in a ./dist directory. This is the one-file compressed version
of your whole library.

Next, upload it to your pipserver:

twine upload --repository-url http://0.0.0.0:8080 --sign --identity "Sean Cusack <seanbcusack@gmail.com>" dist/microspeclib-0.1.1a1-py3-none-any.whl --verbose

Of course, change the 0.1.1a1 file to the specific one you're uploading, and choose a different identity.

## Download and Test

Create a new test environment:

python3 -m venv ~/.testenv
source ~/.testenv/bin/activate

This basically makes a fresh python installation without any modules, into which you can install new
things from scratch, and test how they work with no dependencies assumed. You can then destroy that environment
and try again next time you test.

You should see the new version on the server:

pip search --index http://localhost:8080 microspec

Install your new library from your pip server:

pip install --index http://localhost:8080 microspectrometer

You can then test it from scratch.

## Authors

* **Sean Cusack** - *Initial version* - [GitHub](https://github.com/eruciform) [Blog](https://eruciform.com)

## License

Copyright 2020 by Chromation, Inc

All Rights Reserved by Chromation, Inc



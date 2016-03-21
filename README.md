[![Build Status](https://travis-ci.org/mjdietzx/nrfjprog.svg?branch=master)](https://travis-ci.org/mjdietzx/nrfjprog)
[![PyPI](https://img.shields.io/pypi/l/Django.svg)](https://opensource.org/licenses/BSD-3-Clause)

# nrfjprog
The nrfjprog command line tool implemented in Python. nrfjprog.exe is a tool to program Nordic Semiconductor's nRF51 and nRF52 series devices. The goal is to use a tool such as PyInstaller or py2exe to convert this module to an executable. This will give the basic user the option to run nrfjprog without worrying about their python environment and the advanced user to use this module in their custom scripts (i.e. automated testing).

# Running
1. $ sudo pip install pynrfjprog
2. Clone or download this repository.
3. Navigate to the repository's directory (~/nrfjprog/).
4. $ python nrfjprog --help
5. $ python nrfjprog program --file PATH_TO_APP.hex --eraseall --verify --systemreset

# Structure
```python
nrfjprog\
  # LICENSE, README.md, and requirements.txt (used to install this module). setup.py and tests\ to be added here in the future.
  nrfjprog\
    __init__.py # Package marker to make nrfjprog a module.
    __main__.py # This is where the command line interface is implemented. It parsers arguemnts using argparse and calls nRF5x to perform the requested operation.
    nrfjprog_version.py # Contains a global variable containing the version of nrfjprog.
      device\
        __init__.py # Package marker to make device a module.
        nrf5x.py # This is where the functionality of each command is implemented. Uses the pynrfjprog module.
```

# Architecture
```python
"""
Detailed below is how our software is stacked. Each layer depends on the layer below.
"""
nrfjprog.exe # Command line tool providing high level programming functionality for nRF5x devices.
pynrfjprog # Imports the nrfjprog DLL into Python and wraps it to be used in applications like this one or directly in scripts.
nrfjprogdll # A DLL that does some error checking and calls SEGGER's JLink API. Wraps JLink API specifically for nRF5x devices.
JLinkARMDLL # Performs all low level operations with our device.
```

# Future
We want nrfjprog to be flexible and open. We want it to be an option for our users all the way from development and testing to production programming. In the future we will open source pynrfjprog as well.

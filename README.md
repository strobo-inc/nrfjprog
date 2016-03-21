[![Build Status](https://travis-ci.org/mjdietzx/nrfjprog.svg?branch=develop)](https://travis-ci.org/mjdietzx/nrfjprog)
[![PyPI](https://img.shields.io/pypi/l/Django.svg)](https://opensource.org/licenses/BSD-3-Clause)

# nrfjprog
The nrfjprog command line tool implemented in Python. nrfjprog.exe is a tool to program Nordic Semiconductor's nRF51 and nRF52 series devices.

# Running
1. Download nRF5x Command Line Tools: http://www.nordicsemi.com/eng/Products/Bluetooth-Smart-Bluetooth-low-energy/nRF52-Preview-DK
2. $ sudo pip install pynrfjprog
3. Clone or download this repository.
4. Navigate to the repository's directory (~/nrfjprog/).
5. $ python nordicsemi --help

# Structure
```python
nrfjprog\
  # LICENSE, README.md, and requirements.txt (used to install this module). setup.py and tests\ to be added here in the future.
  nordicsemi\
    __init__.py # Package marker to make nordicsemi a module.
    __main__.py # This is where the command line interface is implemented. It parsers arguemnts using argparse and calls nRF5x to perform the requested operation.
    nrfjprog_version.py # Contains a global variable containing the version of nrfjprog.
      lib\
        __init__.py # Package marker to make lib a module.
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

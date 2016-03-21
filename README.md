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
  nordicsemi\
    __init__.py # Package marker to make nordicsemi a module.
    __main__.py # This is where the command line interface is implemented. It parsers arguemnts using argparse and calls nRF5x to perform the requested operation.
    nrfjprog_version.py # Contains a global variable containing the version of nrfjprog.
      lib\
        __init__.py # Package marker to make lib a module.
        nrf5x.py # This is where the functionality of each command is implemented. Uses the pynrfjprog module.
```

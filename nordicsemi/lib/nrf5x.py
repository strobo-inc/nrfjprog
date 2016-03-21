# Copyright (c) 2016, Nordic Semiconductor
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of Nordic Semiconductor ASA nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import nrfjprog_version

from pynrfjprog import API, Hex

class NRF5x:
    """
    Common class that manages the api instance, some shared arguments amongst commands, and logging.

    """
    def __init__(self, args):
        """
        Constructor that initializes the class's properties.

        :param Object args: The arguments the command was called with.
        :return: None
        """
        try: # Quiet may not be an argument for some commands so args.quiet would be undefined causing an error.
            self.clockspeed = args.clockspeed
        except Exception:
            self.clockspeed = None

        try:
            self.quiet = args.quiet
        except Exception:
            self.quiet = None

        try:
            self.snr = args.snr
        except Exception:
            self.snr = None

        self.api = self._setup()

    def _setup(self):
        """
        Discovers the family (either NRF51 or NRF52) of the target device (through trial and error) and connects to it.

        :return API api: Instance of an API object that is initialized and connected to an nRF5x device.
        """
        device_family = API.DeviceFamily.NRF51
        api = API.API(device_family)
        api.open()
        self._connect_to_emu(api)
        
        try:
            device_version = api.read_device_version()
        except API.APIError as e:
            if e.err_code == API.NrfjprogdllErr.WRONG_FAMILY_FOR_DEVICE:
                device_family = API.DeviceFamily.NRF52
                api.close()
                api = API.API(device_family)
                api.open()
                self._connect_to_emu(api)
            else:
                raise e

        api.connect_to_device()
        return api

    def _connect_to_emu(self, api):
        if self.snr and self.clockspeed:
            api.connect_to_emu_with_snr(self.snr, self.clockspeed)
        elif self.snr:
            api.connect_to_emu_with_snr(self.snr)
        elif self.clockspeed:
            api.connect_to_emu_without_snr(self.clockspeed)
        else:
            api.connect_to_emu_without_snr()

    def log(self, msg):
        if self.quiet:
            pass
        else:
            print(msg)

    def cleanup(self):
        self.api.disconnect_from_emu()
        self.api.close()

"""
The functions that are called from argparse based on the command-line input.

All functions follow the same structure: initialize NRF5x, log (exactly what the help menu prints for the command, but in different tense), perform functionality, cleanup.
"""

def erase(args):
    nrf = NRF5x(args)
    nrf.log('Erasing the device.') # This should go to stderr.

    if args.erasepage:
        nrf.api.erase_page(args.erasepage)
    elif args.eraseuicr:
        nrf.api.erase_uicr()
    else:
        nrf.api.erase_all()

    nrf.cleanup()

def halt(args):
    nrf = NRF5x(args)
    nrf.log("Halting the device's CPU.")

    nrf.api.halt()

    nrf.cleanup()

def ids(args):
    nrf = NRF5x(args)
    nrf.log('Displaying the serial numbers of all debuggers connected to the PC.')

    print(nrf.api.enum_emu_snr()) # This should go to stdout.

    nrf.cleanup()

def memrd(args):
    nrf = NRF5x(args)
    nrf.log("Reading the device's memory.")

    #nrf.log(nrf.api.enum_emu_snr())

    nrf.cleanup()

def memwr(args):
    nrf = NRF5x(args)
    nrf.log("Writing the device's memory.")

    #nrf.log(nrf.api.enum_emu_snr())

    nrf.cleanup()

def program(args):
    nrf = NRF5x(args)
    nrf.log('Programming the device.')

    module_dir, module_file = os.path.split(__file__)
    hex_file_path = os.path.join(os.path.abspath(module_dir), args.file.name)
    
    # Parse hex, program to device
    nrf.log('# Parsing hex file into segments  ')
    test_program = Hex.Hex(hex_file_path) # Parse .hex file into segments
    nrf.log('# Writing %s to device  ' % hex_file_path)
    for segment in test_program:
        nrf.api.write(segment.address, segment.data, True)

    nrf.cleanup()

def readregs(args):
    nrf = NRF5x(args)
    nrf.log('Reading the CPU registers.')

    for reg in API.CpuRegister:
        print(nrf.api.read_cpu_register(reg))

    nrf.cleanup()

def readtofile(args):
    nrf = NRF5x(args)
    nrf.log("Reading and storing the device's memory.")

    #nrf.log(nrf.api.enum_emu_snr())

    nrf.cleanup()

def recover(args):
    nrf = NRF5x(args)
    nrf.log("Erasing all user FLASH and RAM and disabling any readback protection mechanisms that are enabled.")

    nrf.api.recover()

    nrf.cleanup()

def reset(args):
    nrf = NRF5x(args)
    nrf.log('Resetting the device.')

    if args.debugreset:
        nrf.api.debug_reset()
    elif args.pinreset:
        nrf.api.pin_reset()
    else:
        nrf.api.sys_reset()
    
    nrf.api.go()
    nrf.cleanup()

def run(args): # TODO: run should accept pc and sp as input.
    nrf = NRF5x(args)
    nrf.log("Running the device's CPU.")

    nrf.api.go()

    nrf.cleanup()

def verify(args):
    nrf = NRF5x(args)
    nrf.log("Verifying that the device's memory contains the correct data.")

    nrf.cleanup()

def version(args):
    nrf = NRF5x(args)
    nrf.log('Displaying the nrfjprog and JLinkARM DLL versions.')

    jlink_arm_dll_version = nrf.api.dll_version()
    print(jlink_arm_dll_version)
    print(nrfjprog_version.NRFJPROG_VERSION)

    nrf.cleanup()

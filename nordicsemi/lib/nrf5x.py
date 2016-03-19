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

from pynrfjprog import API, Hex
import nrfjprog_version
import os

class NRF5x:
    """
    Common class that manages API.py and some shared options.

    """
    def __init__(self, args):
        """
        Constructor that requires the arguments the command was called with.

        :param Object args: The options the command was called with.

        :return: None
        """
        try: # A bit hacky?
            self.quiet = args.quiet
        except Exception:
            self.quiet = None

        try:
            self.snr = args.snr
        except Exception:
            self.snr = None

        try:
            self.clockspeed = args.clockspeed
        except Exception:
            self.clockspeed = None

        self.api = self._setup()

    def _setup(self):
        """
        Discovers the family of the target device and connects to it.

        :return Object api: Instance of an API object that is initialized and connected to an nRF5x device.
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

        assert(api.is_connected_to_device()), 'unable to connect to target device'
        return api

    def _connect_to_emu(self, api):
        if self.snr:
            if self.clockspeed:
                api.connect_to_emu_with_snr(self.snr, self.clockspeed)
            else:
                api.connect_to_emu_with_snr(self.snr)
        else:
            if self.clockspeed:
                api.connect_to_emu_without_snr(self.clockspeed)
            else:
                api.connect_to_emu_without_snr()

    def _set_clock_speed(self):
        pass

    def log(self, msg):
        if self.quiet:
            pass
        else:
            print(msg)

    def cleanup(self):
        self.api.disconnect_from_emu()
        self.api.close()

def erase(args):
    nrf = NRF5x(args)
    nrf.log('erasing device')

    if args.erasepage:
        nrf.api.erase_page(args.erasepage) # TODO: Not working.
    elif args.eraseuicr:
        nrf.api.erase_uicr()
    else:
        nrf.api.erase_all()

    nrf.cleanup()

def ids(args):
    nrf = NRF5x(args)
    nrf.log('displaying ids of all connected debuggers')
    nrf.log(nrf.api.enum_emu_snr())
    nrf.cleanup()

def program(args):
    nrf = NRF5x(args)
    nrf.log('programming device')

    module_dir, module_file = os.path.split(__file__)
    hex_file_path = os.path.join(os.path.abspath(module_dir), args.file.name)
    
    # Parse hex, program to device
    nrf.log('# Parsing hex file into segments  ')
    test_program = Hex.Hex(hex_file_path) # Parse .hex file into segments
    nrf.log('# Writing %s to device  ' % hex_file_path)
    for segment in test_program:
        nrf.api.write(segment.address, segment.data, True)

    nrf.cleanup()

def recover(args):
    nrf = NRF5x(args)
    nrf.log('recovering device')

    nrf.api.recover()

    nrf.cleanup()

def reset(args):
    """
    Performs a reset of the device. Performs a system reset by default.

    :param : The optional flags specified.
    """
    nrf = NRF5x(args)
    nrf.log('resetting device')

    if args.debugreset:
        nrf.api.debug_reset()
    elif args.pinreset:
        nrf.api.pin_reset()
    else:
        nrf.api.sys_reset()
    
    nrf.api.go()
    nrf.cleanup()

def verify(args):
    """
    Verifies that memory contains the right data.

    """
    nrf = NRF5x(args)
    nrf.log('verifying memory of device')

def version(args):
    """
    Display the nrfjprog and JLinkARM DLL versions.

    """
    nrf = NRF5x(args)
    nrf.log('displaying the nrfjprog and JLinkARM DLL versions.')
    jlink_arm_dll_version = nrf.api.dll_version()
    nrf.log(jlink_arm_dll_version)
    nrf.log(nrfjprog_version.NRFJPROG_VERSION)
    nrf.cleanup()

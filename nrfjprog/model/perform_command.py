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
import numpy as np
from pynrfjprog import API, Hex


class SetupCommand(object):
    """
    Class that handles the api instance, some arguments that commands share, and logging.

    """
    
    def __init__(self, args, do_not_initialize_api = False):
        """
        Initialize the class's properties.

        :param Object  args:                  The arguments the command was called with.
        :param Boolean do_not_initialize_api: If api should be initialized (the connection to the target device should be set up).
        """
        self.args = args
        self.api = None
        self.device_version = None

        if do_not_initialize_api:
            pass
        else:
            if self._setup('NRF51'):
                pass
            elif self._setup('NRF52'):
                pass
            else:
                assert(False), 'Unknown device family.'

        np.set_printoptions(formatter={'int':hex}) # Output values displayed as hex instead of dec.

    def cleanup(self):
        """
        Disconnect from the emulator (debugger) and close api. Then set properties no longer valid to None.

        """
        self.api.disconnect_from_emu()
        self.api.close()
        self.api = None
        self.device_version = None

    def log(self, msg):
        """
        Controls how info should be displayed to the user.

        """
        if self.args.quiet:
            pass
        else:
            print(msg)

    def _setup(self, device_family_guess):
        """
        Connect to target device and check if device_family_guess is correct. If correct, initialize api and device_version and return True. Else, cleanup and return False.

        :param  String:  The device family type to try.
        :return Boolean: If device_family_guess was correct and we initialized everything successfully.
        """
        self.api = API.API(device_family_guess)
        self.api.open()
        self._connect_to_emu()
        
        try:
            self.device_version = self.api.read_device_version()
        except API.APIError as error:
            if error.err_code == API.NrfjprogdllErr.WRONG_FAMILY_FOR_DEVICE:
                self.cleanup()
                return False
            else:
                assert(False), 'Error!'

        return True
        
    def _connect_to_emu(self):
        """
        Connect to the emulator (debugger) with the specific serial number and/or clock speed if either was specified in the command-line arguments.

        """
        if self.args.snr and self.args.clockspeed:
            self.api.connect_to_emu_with_snr(self.args.snr, self.args.clockspeed)
        elif self.args.snr:
            self.api.connect_to_emu_with_snr(self.args.snr)
        elif self.args.clockspeed:
            self.api.connect_to_emu_without_snr(self.args.clockspeed)
        else:
            self.api.connect_to_emu_without_snr()


"""
The callback functions that are called from __main__.py (argparse) based on the command-line input.

All functions follow the same structure: initialize NRF5x, log (exactly what the help menu prints for the command, but in different tense), perform functionality, cleanup.
"""

def erase(args):
    nrf = SetupCommand(args)
    nrf.log('Erasing the device.')

    if args.erasepage:
        nrf.api.erase_page(args.erasepage)
    elif args.eraseuicr:
        nrf.api.erase_uicr()
    else:
        nrf.api.erase_all()

    nrf.cleanup()

def halt(args):
    nrf = SetupCommand(args)
    nrf.log("Halting the device's CPU.")

    nrf.api.halt()

    nrf.cleanup()

def ids(args):
    nrf = SetupCommand(args, do_not_initialize_api = True)
    nrf.log('Displaying the serial numbers of all debuggers connected to the PC.')

    api = API.API('NRF51') # Family doesn't matter since we are not connecting to a device so use NRF51 by default.
    api.open()

    ids = api.enum_emu_snr()
    print(sorted(ids))

    api.close()

def memrd(args):
    nrf = SetupCommand(args)
    nrf.log("Reading the device's memory.")

    read_data = nrf.api.read(args.addr, args.length)
    print(np.array(read_data))

    nrf.cleanup()

def memwr(args):
    nrf = SetupCommand(args)
    nrf.log("Writing the device's memory.")

    nrf.api.write_u32(args.addr, args.val, args.flash) # TODO: args.flash can be automatically determined or we can introduce error checking.

    nrf.cleanup()

def pinresetenable(args): # TODO: User should be able to select which pin to configure as reset.
    nrf = SetupCommand(args)
    nrf.log("Enabling the pin reset on nRF52 devices. Invalid command on nRF51 devices.")

    assert(nrf.device_version[:5] != 'NRF51'), "Enabling pin reset is not a valid command for nRF51 devices."
  
    UICR_PSELRESET0_ADDR = 0x10001200
    UICR_PSELRESET1_ADDR = 0x10001204
    UICR_PSELRESET_21_CONNECT = 0x15 # Writes the CONNECT and PIN bit fields (reset is connected and GPIO pin 21 is selected as the reset pin).

    nrf.api.write_u32(UICR_PSELRESET0_ADDR, UICR_PSELRESET_21_CONNECT, True)
    nrf.api.write_u32(UICR_PSELRESET1_ADDR, UICR_PSELRESET_21_CONNECT, True)
    nrf.api.sys_reset()

    nrf.cleanup()

def program(args):
    nrf = SetupCommand(args)
    nrf.log('Programming the device.')

    if args.eraseall:
        nrf.api.erase_all()
    elif args.sectorserase:
        assert (False), "Not implemented in nrf5x.py yet."
    elif args.sectorsanduicrerase:
        assert (False), "Not implemented in nrf5x.py yet."

    hex_file_path = _get_file_path(args.file.name)
    
    nrf.log('Parsing hex file into segments.')
    test_program = Hex.Hex(hex_file_path)
    nrf.log('Writing %s to device.' % hex_file_path)
    for segment in test_program:
        read_data = nrf.api.read(segment.address, len(segment.data))
        assert (read_data == ([0xFF] * len(read_data))), 'FLASH being written to must be erased.'
        nrf.api.write(segment.address, segment.data, True)
        if args.verify:
            read_data = nrf.api.read(segment.address, len(segment.data))
            assert (read_data == segment.data), 'Verify failed. Data readback from memory does not match data written.'

    if args.verify:
        nrf.log('Programming verified.')

    _reset(nrf, args)

    nrf.cleanup()

def readback(args):
    nrf = SetupCommand(args)
    nrf.log('Enabling the readback protection mechanism.')

    nrf.api.readback_protect(API.ReadbackProtection.ALL) # TODO: What should this be?

    nrf.cleanup()

def readregs(args):
    nrf = SetupCommand(args)
    nrf.log('Reading the CPU registers.')

    for reg in API.CpuRegister:
        print(hex(nrf.api.read_cpu_register(reg)))

    nrf.cleanup()

def readtofile(args):
    nrf = SetupCommand(args)
    nrf.log("Reading and storing the device's memory.")

    assert (False), "Not implemented in nrf5x.py yet."

    nrf.cleanup()

def recover(args):
    nrf = SetupCommand(args)
    nrf.log("Erasing all user FLASH and RAM and disabling any readback protection mechanisms that are enabled.")

    assert (False), "Not implemented in nrf5x.py yet."

    nrf.cleanup()

def reset(args):
    nrf = SetupCommand(args)
    nrf.log('Resetting the device.')

    _reset(nrf, args, default_sys_reset = True)
    
    nrf.cleanup()

def run(args):
    nrf = SetupCommand(args)
    nrf.log("Running the device's CPU.")

    if args.pc != None and args.sp != None:
        nrf.api.run(args.pc, args.sp)
    elif args.pc != None or args.sp != None:
        assert(False), 'Both the PC and the SP must be specified.'
    else:
        nrf.api.go()

    nrf.cleanup()

def verify(args):
    nrf = SetupCommand(args)
    nrf.log("Verifying that the device's memory contains the correct data.")

    hex_file_path = _get_file_path(args.file.name)

    hex_file = Hex.Hex(hex_file_path)
    for segment in hex_file:
        read_data = nrf.api.read(segment.address, len(segment.data))
        assert (read_data == segment.data), 'Verify failed. Data readback from memory does not match data written.'

    nrf.log('Verified.')

    nrf.cleanup()

def version(args):
    nrf = SetupCommand(args, do_not_initialize_api = True)
    nrf.log('Displaying the nrfjprog and JLinkARM DLL versions.')

    api = API.API('NRF51')
    api.open()

    jlink_arm_dll_version = api.dll_version()
    print(jlink_arm_dll_version)
    print(nrfjprog_version.NRFJPROG_VERSION)

    api.close()


"""
Helper functions.

"""

def _get_file_path(user_specified_path):
    if os.path.exists(user_specified_path): # If user specified an absolute path.
        return user_specified_path
    else: # Otherwise append the path user specified to nrfjprog/.
        tmp_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        tmp_path = os.path.abspath(os.path.join(tmp_path, os.pardir))
        return os.path.join(tmp_path, user_specified_path)

def _reset(nrf, args, default_sys_reset = False):
    """
    Reset and run the device.

    """
    if args.debugreset:
        nrf.api.debug_reset()
    elif args.pinreset:
        nrf.api.pin_reset()
    elif args.systemreset or default_sys_reset:
        nrf.api.sys_reset()
    else:
        return

    nrf.api.go() # Really we should not need this call, but nrfjprog DLL halts after a reset.

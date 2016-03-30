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
import device
import nrfjprog_version
import numpy as np
from pynrfjprog import API, Hex


class SetupCommand(object):
    """
    Class that handles the pynrfjprog api instance, some shared arguments, and logging.

    """
    
    def __init__(self, args, do_not_initialize_api = False):
        """
        Initialize the class's properties, sets up the connection to our target device and configures some printing options.

        :param Object  args:                  The arguments the command was called with.
        :param Boolean do_not_initialize_api: If api should be initialized (the connection to the target device should be set up - a command may not need to connect to the target device).
        """
        self.args = args
        self.api = None
        self.device = None
        self.device_version = None

        if do_not_initialize_api == False:
            if self._setup('NRF51'):
                pass
            elif self._setup('NRF52'):
                pass
            else:
                assert(False), 'Unknown device family.'

        np.set_printoptions(formatter={'int':hex}, threshold=np.nan) # Output values displayed as hex instead of dec and print the entire array (not a truncated array).

    def cleanup(self):
        """
        Disconnect from the emulator (debugger) and close the pynrfjprog api instance.

        """
        self.api.disconnect_from_emu()
        self.api.close()
        self.api = None
        self.device_version = None

    def connect_to_emu(self, api):
        """
        This method should only be called when this class is created with the do_not_initialize_api flag (i.e. called by recover()).

        :param API api: An instance of api that has been initialized by the caller.
        """
        assert (self.api == None), "The class's api property has already been initialized."
        self.api = api
        self._connect_to_emu()

    def log(self, msg):
        """
        Controls how info should be displayed to the user.

        """
        if self.args.quiet:
            pass
        else:
            print(msg)

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

        self.device = device.NRF5xDevice(self.device_version)
        return True     


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

    api = API.API('NRF51') # Device family type arbitrary since we are not connecting to a device. Use NRF51 by default.
    api.open()

    ids = api.enum_emu_snr()
    print(sorted(ids))

    api.close()

def memrd(args):
    nrf = SetupCommand(args)
    nrf.log("Reading the device's memory.")

    data = np.array(nrf.api.read(args.addr, args.length))
    _output_data(args.addr, data)

    nrf.cleanup()

def memwr(args):
    nrf = SetupCommand(args)
    nrf.log("Writing the device's memory.")

    flash = False
    if (args.addr in range(nrf.device.FLASH_START, nrf.device.FLASH_END) or args.addr in range(nrf.device.UICR_START, nrf.device.UICR_END)):
        flash = True

    nrf.api.write_u32(args.addr, args.val, flash)

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

def program(args): # TODO: more implementation/cleanup to be done here.
    nrf = SetupCommand(args)
    nrf.log('Programming the device.')

    if args.eraseall:
        nrf.api.erase_all()
    elif args.sectorserase:
        assert (False), "Not implemented in nrf5x.py yet. Use --eraseall for now."
    elif args.sectorsanduicrerase:
        assert (False), "Not implemented in nrf5x.py yet. Use --eraseall for now."

    hex_file_path = _get_file_path(args.file)
    
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
        print('{}: {}'.format(reg.name, hex(nrf.api.read_cpu_register(reg))))

    nrf.cleanup()

def readtofile(args):
    nrf = SetupCommand(args)
    nrf.log("Reading and storing the device's memory.")

    try:
        with open(args.file, 'w') as file:
            if args.readcode or not (args.readuicr or args.readram):
                file.write('----------Code FLASH----------\n\n')
                _output_data(nrf.device.FLASH_START,  np.array(nrf.api.read(nrf.device.FLASH_START, nrf.device.FLASH_SIZE)), file)
                file.write('\n\n')
            if args.readuicr:
                file.write('----------UICR----------\n\n')
                _output_data(nrf.device.UICR_START, np.array(nrf.api.read(nrf.device.UICR_START, nrf.device.PAGE_SIZE)), file)
                file.write('\n\n')
            if args.readram:
                file.write('----------RAM----------\n\n')
                _output_data(nrf.device.RAM_START, np.array(nrf.api.read(nrf.device.RAM_START, nrf.device.RAM_SIZE)), file)
    except IOError as error:
        nrf.log("Error when opening/writing file.")

    nrf.cleanup()

def recover(args):
    nrf = SetupCommand(args, do_not_initialize_api = True)
    nrf.log("Erasing all user FLASH and RAM and disabling any readback protection mechanisms that are enabled.")

    api = API.API(args.family)
    api.open()
    
    nrf.connect_to_emu(api)
    nrf.api.recover()

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

    hex_file_path = _get_file_path(args.file)

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
    print('JLink version: {}'.format(jlink_arm_dll_version))
    print('nRFjprog version: {}'.format(nrfjprog_version.NRFJPROG_VERSION))

    api.close()


"""
Helper functions.

"""

def _get_file_path(user_specified_path):
    """
    The user can either specify a relative path from their current directory or an absolute path.

    """
    if os.path.exists(user_specified_path):
        return user_specified_path

def _output_data(addr, byte_array, file = None):
    """
    When we read data from memory and output it to the console or file, we want to print with following format: ADDRESS: WORD\n

    """
    index = 0
    
    while index < len(byte_array):
        tmp = "{}: {}".format(hex(addr), byte_array[index : index + 4])
        if file:
            file.write(tmp + '\n')
        else:
            print(tmp) 
        addr = addr + 4
        index = index + 4

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

    nrf.api.go()

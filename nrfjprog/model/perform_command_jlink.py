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

"""


"""
from intelhex import IntelHex
import numpy as np
from pynrfjprog import API

from model import device
import nrfjprog_version


class SetupCommand(object):
    """
    Class that handles the pynrfjprog api instance, some shared arguments, and logging.

    """

    DEFAULT_JLINK_SPEED_KHZ = 5000

    def __init__(self, args, do_not_initialize_api=False):
        """
        Initialize the class's properties, sets up the connection to our target device, and configures some logging options.

        :param Object args:                  Arguments the command was called with.
        :param bool  do_not_initialize_api:  If api should be initialized (the connection to the target device should be set up - a command may not need to connect to the target device).
        """
        self.args = args
        self.api = None
        self.device = None
        self.device_version = None

        if not do_not_initialize_api:
            if self._setup('NRF52'):
                pass
            elif self._setup('NRF51'):
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
        self.device = None
        self.device_version = None

    def connect_to_emu(self, api):
        """
        This method should only be called when this class is created with the do_not_initialize_api flag (i.e. called by recover()).

        :param API api: An instance of api that has been initialized by the caller.
        """
        assert (self.api is None), "The class's api property has already been initialized."
        self.api = api
        self._connect_to_emu()

    def _connect_to_emu(self):
        """
        Connect to the emulator (debugger) with the specific serial number and/or clock speed if either was specified in the command-line arguments.

        """
        if self.args.snr and self.args.clockspeed:
            self.api.connect_to_emu_with_snr(self.args.snr, self.args.clockspeed)
        elif self.args.snr:
            self.api.connect_to_emu_with_snr(self.args.snr, self.DEFAULT_JLINK_SPEED_KHZ)
        elif self.args.clockspeed:
            self.api.connect_to_emu_without_snr(self.args.clockspeed)
        else:
            self.api.connect_to_emu_without_snr(self.DEFAULT_JLINK_SPEED_KHZ)

    def _setup(self, device_family_guess):
        """
        Connect to target device and check if device_family_guess is correct. If correct, initialize api and device_version and return True. Else, cleanup and return False.

        :param  String device_family_guess: The device family type to try.
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


def erase(args):
    nrf = SetupCommand(args)

    if args.erasepage:
        nrf.api.erase_page(args.erasepage)
    elif args.eraseuicr:
        nrf.api.erase_uicr()
    else:
        nrf.api.erase_all()

    nrf.cleanup()

def halt(args):
    nrf = SetupCommand(args)

    nrf.api.halt()

    nrf.cleanup()

def ids(args):
    nrf = SetupCommand(args, do_not_initialize_api=True)

    api = API.API('NRF52') # Device family type arbitrary since we are not connecting to a device. Use NRF52 by default.
    api.open()

    ids = api.enum_emu_snr()
    if ids:
        print(sorted(ids))

    api.close()

def memrd(args):
    nrf = SetupCommand(args)

    data = np.array(nrf.api.read(args.addr, args.length))
    _output_data(args.addr, data)

    nrf.cleanup()

def memwr(args):
    nrf = SetupCommand(args)

    flash = False
    if (args.addr in range(nrf.device.flash_start, nrf.device.flash_end) or args.addr in range(nrf.device.uicr_start, nrf.device.uicr_end)):
        flash = True

    nrf.api.write_u32(args.addr, args.val, flash)

    nrf.cleanup()

def pinresetenable(args):
    nrf = SetupCommand(args)

    assert(nrf.device_version[:5] != 'NRF51'), "Enabling pin reset is not a valid command for nRF51 devices."

    uicr_pselreset0_addr = 0x10001200
    uicr_pselreset1_addr = 0x10001204
    uicr_pselreset_21_connect = 0x15 # Writes the CONNECT and PIN bit fields (reset is connected and GPIO pin 21 is selected as the reset pin).

    nrf.api.write_u32(uicr_pselreset0_addr, uicr_pselreset_21_connect, True)
    nrf.api.write_u32(uicr_pselreset1_addr, uicr_pselreset_21_connect, True)
    nrf.api.sys_reset()

    nrf.cleanup()

def program(args):
    nrf = SetupCommand(args)

    if args.eraseall:
        nrf.api.erase_all()
    if args.sectorsanduicrerase:
        nrf.api.erase_uicr()

    hex_file = IntelHex(args.file)
    for segment in hex_file.segments():
        start_addr, end_addr = segment
        size = end_addr - start_addr

        if args.sectorserase or args.sectorsanduicrerase:
            start_page = int(start_addr / nrf.device.page_size)
            end_page = int(end_addr / nrf.device.page_size)
            for page in range(start_page, end_page + 1):
                nrf.api.erase_page(page * nrf.device.page_size)

        data = hex_file.tobinarray(start=start_addr, size=(size))
        nrf.api.write(start_addr, data.tolist(), True)

        if args.verify:
            read_data = np.array(nrf.api.read(start_addr, len(data)))
            assert (np.array_equal(data, read_data)), 'Verify failed. Data readback from memory does not match data written.'

    if args.verify:
        nrf.log('Programming verified.')

    _reset(nrf, args)

    nrf.cleanup()

def readback(args):
    nrf = SetupCommand(args)

    if args.rbplevel == 'CR0':
        nrf.api.readback_protect(API.ReadbackProtection.REGION_0)
    else:
        nrf.api.readback_protect(API.ReadbackProtection.ALL)

    nrf.cleanup()

def readregs(args):
    nrf = SetupCommand(args)

    for reg in API.CpuRegister:
        print('{}: {}'.format(reg.name, hex(nrf.api.read_cpu_register(reg))))

    nrf.cleanup()

def readtofile(args):
    nrf = SetupCommand(args)

    try:
        with open(args.file, 'w') as file:
            if args.readcode or not (args.readuicr or args.readram):
                file.write('----------Code FLASH----------\n\n')
                _output_data(nrf.device.flash_start, np.array(nrf.api.read(nrf.device.flash_start, nrf.device.flash_size)), file)
                file.write('\n\n')
            if args.readuicr:
                file.write('----------UICR----------\n\n')
                _output_data(nrf.device.uicr_start, np.array(nrf.api.read(nrf.device.uicr_start, nrf.device.page_size)), file)
                file.write('\n\n')
            if args.readram:
                file.write('----------RAM----------\n\n')
                _output_data(nrf.device.ram_start, np.array(nrf.api.read(nrf.device.ram_start, nrf.device.ram_size)), file)
    except IOError as error:
        nrf.log("{}.".format(error))

    nrf.cleanup()

def recover(args):
    nrf = SetupCommand(args, do_not_initialize_api=True)

    api = API.API(args.family)
    api.open()

    nrf.connect_to_emu(api)
    nrf.api.recover()

    nrf.cleanup()

def reset(args):
    nrf = SetupCommand(args)

    _reset(nrf, args, default_sys_reset=True)

    nrf.cleanup()

def run(args):
    nrf = SetupCommand(args)

    if args.pc != None and args.sp != None:
        nrf.api.run(args.pc, args.sp)
    elif args.pc != None or args.sp != None:
        assert(False), 'Both the PC and the SP must be specified.'
    else:
        nrf.api.go()

    nrf.cleanup()

def verify(args):
    nrf = SetupCommand(args)

    hex_file = IntelHex(args.file)
    for segment in hex_file.segments():
        start_addr, end_addr = segment
        size = end_addr - start_addr

        data = hex_file.tobinarray(start=start_addr, size=size)
        read_data = nrf.api.read(start_addr, size)

        assert (np.array_equal(data, np.array(read_data))), 'Verify failed. Data readback from memory does not match data written.'

    nrf.log('Verified.')

    nrf.cleanup()

def version(args):
    nrf = SetupCommand(args, do_not_initialize_api=True)

    api = API.API('NRF52')
    api.open()

    jlink_arm_dll_version = api.dll_version()
    print('JLink version: {}'.format(jlink_arm_dll_version))
    print('nRFjprog version: {}'.format(nrfjprog_version.NRFJPROG_VERSION))

    api.close()


# Helper functions.

def _output_data(addr, byte_array, file=None):
    """
    When we read data from memory and output it to the console or file, we want to print with following format: ADDRESS: WORD\n

    """
    index = 0

    while index < len(byte_array):
        string = "{}: {}".format(hex(addr), byte_array[index : index + 4])
        if file:
            file.write(string + '\n')
        else:
            print(string)
        addr = addr + 4
        index = index + 4

def _reset(nrf, args, default_sys_reset=False):
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

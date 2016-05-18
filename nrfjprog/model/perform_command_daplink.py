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
import enum
from intelhex import IntelHex
import logging
import numpy as np
import os
from pyOCD.board import MbedBoard
from pyOCD.target import cortex_m

from model import device
import nrfjprog_version
import perform_command


@enum.unique
class Memory_Access_Mode(enum.IntEnum):
    READ_ENABLE  = 0
    WRITE_ENABLE = 1
    ERASE_ENABLE = 2


def _config_NVMC(target, access_mode):
    """
    Configure the NVMC to read, write, or erase FLASH.

    """
    NVMC_CONFIG_ADDR = 0x4001E504
    target.write32(NVMC_CONFIG_ADDR, access_mode)


def _setup():
    board = MbedBoard.chooseBoard()
    return board.target, board.flash


def erase(args):
    target, flash = _setup()
    flash.init()

    NVMC_ERASEUICR_ADDR = 0x4001E000

    if args.erasepage:
        flash.erasePage(args.erasepage)
    elif args.eraseuicr:
        _config_NVMC(target, Memory_Access_Mode.ERASE_ENABLE)
        target.write32(NVMC_ERASEUICR_ADDR, 1)
        _config_NVMC(target, Memory_Access_Mode.READ_ENABLE)
    else:
        flash.eraseAll()

def halt(args):
    target, flash = _setup()
    target.halt()

def ids(args):
    MbedBoard.listConnectedBoards()

def memrd(args):
    target, flash = _setup()
    data = target.readBlockMemoryUnaligned8(args.addr, args.length)
    perform_command.output_data(args.addr, data)

def memwr(args):
    target, flash = _setup()

    nRF5_device = device.NRF5xDevice('NRF52_FP1') # TODO: This should not be hard-coded.

    if perform_command.is_flash_addr(args.addr, nRF5_device):
        _config_NVMC(target, Memory_Access_Mode.WRITE_ENABLE)

    target.write32(args.addr, args.val)

    _config_NVMC(target, Memory_Access_Mode.READ_ENABLE)

def pinresetenable(args):
    assert(False), 'Not implemented in pyOCD.' # TODO: Implement this in pyOCD.
    target, flash = _setup()

    # BUG: shouldn't be possible for nRF51.

    uicr_pselreset0_addr = 0x10001200
    uicr_pselreset1_addr = 0x10001204
    uicr_pselreset_21_connect = 0x15 # Writes the CONNECT and PIN bit fields (reset is connected and GPIO pin 21 is selected as the reset pin).

    target.write32(uicr_pselreset0_addr, uicr_pselreset_21_connect, True) # BUG: pyOCD can't write UICR.
    target.write32(uicr_pselreset1_addr, uicr_pselreset_21_connect, True)
    target.reset()

def program(args):
    target, flash = _setup()
    flash.init()

    tmp_bin_file = 'tmp.bin'

    hex_file = IntelHex(args.file)
    hex_file.tobinfile(tmp_bin_file)
    flash.flashBinary(tmp_bin_file, chip_erase=args.eraseall, fast_verify=args.verify)

    if args.debugreset or args.pinreset or args.systemreset :
        target.reset()

    os.remove(tmp_bin_file)

def readback(args):
    assert(False), 'Not implemented in pyOCD.' # TODO: Implement this in pyOCD.

def readregs(args):
    target, flash = _setup()

    for reg in cortex_m.CORE_REGISTER:
        if cortex_m.CORE_REGISTER[reg] in range(0, 16):
            print(target.readCoreRegister(reg))

def readtofile(args):
    target, flash = _setup()
    nRF5_device = device.NRF5xDevice('NRF52_FP1') # TODO: This should not be hard-coded.

    try:
        with open(args.file, 'w') as file:
            if args.readcode or not (args.readuicr or args.readram):
                file.write('----------Code FLASH----------\n\n')
                perform_command.output_data(nRF5_device.flash_start, np.array(target.readBlockMemoryAligned32(nRF5_device.flash_start, nRF5_device.flash_size)), file)
                file.write('\n\n')
            if args.readuicr:
                file.write('----------UICR----------\n\n')
                perform_command.output_data(nRF5_device.uicr_start, np.array(target.readBlockMemoryAligned32(nRF5_device.uicr_start, nRF5_device.page_size)), file)
                file.write('\n\n')
            if args.readram:
                file.write('----------RAM----------\n\n')
                perform_command.output_data(nRF5_device.ram_start, np.array(target.readBlockMemoryAligned32(nRF5_device.ram_start, nRF5_device.ram_size)), file)
    except IOError as error:
        pass # TODO: do something...

def recover(args):
    target, flash = _setup()

    # target.setAutoUnlock() # TODO: This won't work.
    flash.init()
    flash.eraseAll()

def reset(args):
    target, flash = _setup()
    target.reset()

def run(args):
    target, flash = _setup()
    target.resume()

def verify(args):
    target, flash = _setup()

    hex_file = IntelHex(args.file)
    for segment in hex_file.segments():
        start_addr, end_addr = segment
        size = end_addr - start_addr

        data = hex_file.tobinarray(start=start_addr, size=size)
        read_data = target.readBlockMemoryUnaligned8(start_addr, size)

        assert (np.array_equal(data, np.array(read_data))), 'Verify failed. Data readback from memory does not match data written.'

def version(args):
    print('nRFjprog version: {}'.format(nrfjprog_version.NRFJPROG_VERSION))

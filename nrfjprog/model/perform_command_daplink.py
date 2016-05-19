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

import enum
from intelhex import IntelHex
import os
from pyOCD.board import MbedBoard
from pyOCD.target import cortex_m

from nrfjprog.model import device
from nrfjprog import nrfjprog_version


@enum.unique
class Memory_Access_Mode(enum.IntEnum):
    READ_ENABLE  = 0
    WRITE_ENABLE = 1
    ERASE_ENABLE = 2


# Helpers.

def _config_NVMC(target, access_mode):
    """
    Configure the NVMC to read, write, or erase FLASH.

    """
    NVMC_CONFIG_ADDR = 0x4001E504
    target.write32(NVMC_CONFIG_ADDR, access_mode)

def _erase_uicr(target):
    _config_NVMC(target, Memory_Access_Mode.ERASE_ENABLE)
    target.write32(NVMC_ERASEUICR_ADDR, 1)
    _config_NVMC(target, Memory_Access_Mode.READ_ENABLE)

def _setup():
    board = MbedBoard.chooseBoard()
    return board


# Commands.

def erase(args):
    board = _setup()
    board.flash.init()

    NVMC_ERASEUICR_ADDR = 0x4001E514

    if args.erasepage:
        board.flash.erasePage(args.erasepage)
    elif args.eraseuicr:
        _erase_uicr(board.target)
    else:
        board.flash.eraseAll()

def halt(args):
    board = _setup()
    board.target.halt()

def ids(args):
    MbedBoard.listConnectedBoards()

def memrd(args):
    board = _setup()
    data = board.target.readBlockMemoryUnaligned8(args.addr, args.length)
    perform_command.output_data(args.addr, data)

def memwr(args):
    board = _setup()

    nRF5_device = device.NRF5xDevice('NRF52_FP1') # TODO: This should not be hard-coded.

    if perform_command.is_flash_addr(args.addr, nRF5_device):
        _config_NVMC(board.target, Memory_Access_Mode.WRITE_ENABLE)
        board.target.write32(args.addr, args.val)
        _config_NVMC(board.target, Memory_Access_Mode.READ_ENABLE)
    else:
        board.target.write32(args.addr, args.val)

def pinresetenable(args):
    board = _setup()
    assert(board.getTargetType() is 'nrf52')

    _config_NVMC(board.target, Memory_Access_Mode.WRITE_ENABLE)

    uicr_pselreset0_addr = 0x10001200
    uicr_pselreset1_addr = 0x10001204
    uicr_pselreset_21_connect = 0x15 # Writes the CONNECT and PIN bit fields (reset is connected and GPIO pin 21 is selected as the reset pin).

    board.target.write32(uicr_pselreset0_addr, uicr_pselreset_21_connect)
    board.target.write32(uicr_pselreset1_addr, uicr_pselreset_21_connect)

    _config_NVMC(board.target, Memory_Access_Mode.READ_ENABLE)

    board.target.reset()

def program(args):
    board = _setup()
    board.flash.init()

    tmp_bin_file = 'tmp.bin'

    if args.sectorsanduicrerase:
        _erase_uicr(board.target) # TODO: May not be needed if pyOCD does this. Double check before removing.

    hex_file = IntelHex(args.file)
    hex_file.tobinfile(tmp_bin_file)
    board.flash.flashBinary(tmp_bin_file, chip_erase=args.eraseall, fast_verify=args.verify)

    if args.debugreset or args.pinreset or args.systemreset:
        board.target.reset()

    os.remove(tmp_bin_file)

def readback(args):
    print('Not implemented in nrfjprog when using pyOCD.')

def readregs(args):
    board = _setup()

    for reg in cortex_m.CORE_REGISTER:
        if cortex_m.CORE_REGISTER[reg] in range(0, 16):
            print(board.target.readCoreRegister(reg))

def readtofile(args):
    board = _setup()
    nRF5_device = device.NRF5xDevice('NRF52_FP1') # TODO: This should not be hard-coded.

    try:
        with open(args.file, 'w') as file:
            if args.readcode or not (args.readuicr or args.readram):
                file.write('----------Code FLASH----------\n\n')
                perform_command.output_data(nRF5_device.flash_start, board.target.readBlockMemoryAligned32(nRF5_device.flash_start, nRF5_device.flash_size), file)
                file.write('\n\n')
            if args.readuicr:
                file.write('----------UICR----------\n\n')
                perform_command.output_data(nRF5_device.uicr_start, board.target.readBlockMemoryAligned32(nRF5_device.uicr_start, nRF5_device.page_size), file)
                file.write('\n\n')
            if args.readram:
                file.write('----------RAM----------\n\n')
                perform_command.output_data(nRF5_device.ram_start, board.target.readBlockMemoryAligned32(nRF5_device.ram_start, nRF5_device.ram_size), file)
    except IOError as error:
        pass # TODO: do something...

def recover(args):
    print('WARNING: This will not actually unlock the chip right now, just does a full erase.')
    board = _setup()

    board.flash.init()
    board.flash.eraseAll()

def reset(args):
    board = _setup()
    board.target.reset()

def run(args):
    board = _setup()
    board.target.resume()

def verify(args):
    board = _setup()

    hex_file = IntelHex(args.file)
    for segment in hex_file.segments():
        start_addr, end_addr = segment
        size = end_addr - start_addr

        data = hex_file.tobinarray(start=start_addr, size=size)
        read_data = board.target.readBlockMemoryUnaligned8(start_addr, size)

        assert (byte_lists_equal(data, read_data)), 'Verify failed. Data readback from memory does not match data written.'

def version(args):
    print('nRFjprog version: {}'.format(nrfjprog_version.NRFJPROG_VERSION))


# Shared helper functions.

def byte_lists_equal(data, read_data):
    for i in xrange(len(data)):
        if data[i] != read_data[i]:
            return False
    return True

def is_flash_addr(addr, device):
    return addr in range(device.flash_start, device.flash_end) or addr in range(device.uicr_start, device.uicr_end)

def output_data(addr, byte_array, file=None):
    """
    Read data from memory and output it to the console or file with the following format: ADDRESS: WORD\n

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

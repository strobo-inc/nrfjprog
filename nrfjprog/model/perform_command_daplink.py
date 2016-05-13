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
import logging
import numpy as np
from pyOCD.board import MbedBoard
from pyOCD.target import cortex_m

from model import device
import nrfjprog_version


def _setup():
    #logging.basicConfig(level=logging.INFO)

    board = MbedBoard.chooseBoard()
    return board.target, board.flash


def erase(args):
    target, flash = _setup()
    flash.init()

    if args.erasepage:
        flash.erasePage(args.erasepage)
    elif args.eraseuicr:
        assert(False), 'Not implemented in pyOCD.' # TODO: Fix this in pyOCD.
    else:
        flash.eraseAll()

def halt(args):
    target, flash = _setup()
    target.halt()

def ids(args):
    assert(False), 'Not implemented in pyOCD.' # TODO: Fix this in pyOCD.

def memrd(args):
    target, flash = _setup()
    data = target.readBlockMemoryUnaligned8(args.addr, args.length)
    _output_data(args.addr, data)

def memwr(args):
    target, flash = _setup()
    target.write32(args.addr, args.val) # TODO: pyOCD can't write nRF5 FLASH.

def pinresetenable(args):
    assert(False), 'Not implemented in pyOCD.' # TODO: Fix this in pyOCD.

def program(args):
    target, flash = _setup()
    flash.init()

    if args.sectorserase or args.sectorsanduicrerase:
        assert(False), 'Not implemented in pyOCD.' # TODO: Fix this in pyOCD.

    hex_file = IntelHex(args.file)
    hex_file.tobinfile('tmp.bin')
    flash.flashBinary('tmp.bin', chip_erase=args.eraseall, fast_verify=args.verify)

    _reset(target, args)

    # TODO: Delete 'tmp.bin'.

def readback(args):
    assert(False), 'Not implemented in pyOCD.' # TODO: Fix this in pyOCD.

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
                _output_data(nRF5_device.flash_start, np.array(target.readBlockMemoryAligned32(nRF5_device.flash_start, nRF5_device.flash_size)), file)
                file.write('\n\n')
            if args.readuicr:
                file.write('----------UICR----------\n\n')
                _output_data(nRF5_device.uicr_start, np.array(target.readBlockMemoryAligned32(nRF5_device.uicr_start, nRF5_device.page_size)), file)
                file.write('\n\n')
            if args.readram:
                file.write('----------RAM----------\n\n')
                _output_data(nRF5_device.ram_start, np.array(target.readBlockMemoryAligned32(nRF5_device.ram_start, nRF5_device.ram_size)), file)
    except IOError as error:
        pass # TODO: do something...

def recover(args):
    target, flash = _setup()

    target.setAutoUnlock() # TODO: This won't work.
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

def _reset(target, args, default_sys_reset=False):
    """
    Reset and run the device.

    """
    if args.debugreset or args.pinreset or args.systemreset or default_sys_reset:
        target.reset()
    else:
        return

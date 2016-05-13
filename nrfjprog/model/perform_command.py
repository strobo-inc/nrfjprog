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
This module receives user input from __main__.py and performs them via JLink (pynrfjprog) or DAP-Link/CMSIS-DAP (pyOCD).

"""
from pynrfjprog import API

import perform_command_daplink
import perform_command_jlink


def log(args, msg):
    """
    Controls how info should be displayed to the user.

    """
    if args.quiet:
        pass
    else:
        print(msg)

def is_jlink():
    """
    Check if PC is connected to a SEGGER JLink debugger.

    """
    api = API.API('NRF52')
    api.open() # BUG: This will require the user to have JLink Software installed on their PC.

    if api.enum_emu_snr(): # BUG: What happens if both a JLink and DAP-Link debugger are both connected to the PC?
        return_value = True
    else:
        return_value = False

    api.close()
    return return_value


# The callback functions that are called from __main__.py (argparse) based on the command-line input.
# All functions follow the same structure: log (exactly what the help menu prints for the command but in different tense), initialize NRF5 device, perform functionality, cleanup.

def erase(args):
    log(args, 'Erasing the device.')
    perform_command_jlink.erase(args) if is_jlink() else perform_command_daplink.erase(args)

def halt(args):
    log(args, "Halting the device's CPU.")
    perform_command_jlink.halt(args) if is_jlink() else perform_command_daplink.halt(args)

def ids(args):
    log(args, 'Displaying the serial numbers of all debuggers connected to the PC.')
    perform_command_jlink.ids(args) if is_jlink() else perform_command_daplink.ids(args)

def memrd(args):
    log(args, "Reading the device's memory.")
    perform_command_jlink.memrd(args) if is_jlink() else perform_command_daplink.memrd(args)

def memwr(args):
    log(args, "Writing the device's memory.")
    perform_command_jlink.memwr(args) if is_jlink() else perform_command_daplink.memwr(args)

def pinresetenable(args):
    log(args, "Enabling the pin reset on nRF52 devices. Invalid command on nRF51 devices.")
    perform_command_jlink.pinresetenable(args) if is_jlink() else perform_command_daplink.pinresetenable(args)

def program(args):
    log(args, 'Programming the device.')
    perform_command_jlink.program(args) if is_jlink() else perform_command_daplink.program(args)

def readback(args):
    log(args, 'Enabling the readback protection mechanism.')
    perform_command_jlink.readback(args) if is_jlink() else perform_command_daplink.readback(args)

def readregs(args):
    log(args, 'Reading the CPU registers.')
    perform_command_jlink.readregs(args) if is_jlink() else perform_command_daplink.readregs(args)

def readtofile(args):
    log(args, "Reading and storing the device's memory.")
    perform_command_jlink.readtofile(args) if is_jlink() else perform_command_daplink.readtofile(args)

def recover(args):
    log(args, "Erasing all user FLASH and RAM and disabling any readback protection mechanisms that are enabled.")
    perform_command_jlink.recover(args) if is_jlink() else perform_command_daplink.recover(args)

def reset(args):
    log(args, 'Resetting the device.')
    perform_command_jlink.reset(args) if is_jlink() else perform_command_daplink.reset(args)

def run(args):
    log(args, "Running the device's CPU.")
    perform_command_jlink.run(args) if is_jlink() else perform_command_daplink.run(args)

def verify(args):
    log(args, "Verifying that the device's memory contains the correct data.")
    perform_command_jlink.verify(args) if is_jlink() else perform_command_daplink.verify(args)

def version(args):
    log(args, 'Displaying the nrfjprog and JLinkARM DLL versions.')
    perform_command_jlink.version(args) if is_jlink() else perform_command_daplink.version(args)


# Shared helper functions.

def output_data(addr, byte_array, file=None):
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
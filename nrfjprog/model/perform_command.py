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
This module receives user input from __main__.py and performs the operation via JLink (pynrfjprog) or DAP-Link/CMSIS-DAP (pyOCD).

"""

# Helpers.

def lazy_import(use_daplink):
    if not use_daplink:
        global perform_command_jlink
        from nrfjprog.model import perform_command_jlink
    else:
        global perform_command_daplink
        from nrfjprog.model import perform_command_daplink

def log(args, msg):
    """
    Controls how info should be displayed to the user.

    """
    if args.quiet:
        pass
    else:
        print(msg)


# The callback functions that are called from __main__.py (argparse) based on the command-line input.
# All functions follow the same structure: log (exactly what the help menu prints for the command but in different tense), initialize NRF5 device, perform functionality, cleanup.

def erase(args):
    lazy_import(args.daplink)
    log(args, 'Erasing the device.')
    perform_command_jlink.erase(args) if not args.daplink else perform_command_daplink.erase(args)
    log(args, 'Device erased.')

def halt(args):
    lazy_import(args.daplink)
    log(args, "Halting the device's CPU.")
    perform_command_jlink.halt(args) if not args.daplink else perform_command_daplink.halt(args)
    log(args, "Device's CPU halted.")

def ids(args):
    lazy_import(args.daplink)
    log(args, 'Displaying the serial numbers of all debuggers connected to the PC.')
    perform_command_jlink.ids(args) if not args.daplink else perform_command_daplink.ids(args)

def memrd(args):
    lazy_import(args.daplink)
    log(args, "Reading the device's memory.")
    perform_command_jlink.memrd(args) if not args.daplink else perform_command_daplink.memrd(args)

def memwr(args):
    lazy_import(args.daplink)
    log(args, "Writing the device's memory.")
    perform_command_jlink.memwr(args) if not args.daplink else perform_command_daplink.memwr(args)
    log(args, "Device's memory written.")

def pinresetenable(args):
    lazy_import(args.daplink)
    log(args, "Enabling the pin reset on nRF52 devices. Invalid command on nRF51 devices.")
    perform_command_jlink.pinresetenable(args) if not args.daplink else perform_command_daplink.pinresetenable(args)
    log(args, "Pin reset enabled.")

def program(args):
    lazy_import(args.daplink)
    log(args, 'Programming the device.')
    perform_command_jlink.program(args) if not args.daplink else perform_command_daplink.program(args)
    log(args, 'Device programmed.')

def readback(args):
    lazy_import(args.daplink)
    log(args, 'Enabling the readback protection mechanism.')
    perform_command_jlink.readback(args) if not args.daplink else perform_command_daplink.readback(args)
    log(args, 'Readback protection mechanism enabled.')

def readregs(args):
    lazy_import(args.daplink)
    log(args, 'Reading the CPU registers.')
    perform_command_jlink.readregs(args) if not args.daplink else perform_command_daplink.readregs(args)

def readtofile(args):
    lazy_import(args.daplink)
    log(args, "Reading and storing the device's memory.")
    perform_command_jlink.readtofile(args) if not args.daplink else perform_command_daplink.readtofile(args)
    log(args, "Device's memory read and stored")

def recover(args):
    lazy_import(args.daplink)
    log(args, "Erasing all user FLASH and RAM and disabling any readback protection mechanisms that are enabled.")
    perform_command_jlink.recover(args) if not args.daplink else perform_command_daplink.recover(args)
    log(args, "Device recovered.")

def reset(args):
    lazy_import(args.daplink)
    log(args, 'Resetting the device.')
    perform_command_jlink.reset(args) if not args.daplink else perform_command_daplink.reset(args)
    log(args, 'Device reset.')

def run(args):
    lazy_import(args.daplink)
    log(args, "Running the device's CPU.")
    perform_command_jlink.run(args) if not args.daplink else perform_command_daplink.run(args)
    log(args, "Device's CPU running.")

def verify(args):
    lazy_import(args.daplink)
    log(args, "Verifying that the device's memory contains the correct data.")
    perform_command_jlink.verify(args) if not args.daplink else perform_command_daplink.verify(args)
    log(args, "Device's memory contains the correct data.")

def version(args):
    lazy_import(args.daplink)
    log(args, 'Displaying the nrfjprog and JLinkARM DLL versions.')
    perform_command_jlink.version(args) if not args.daplink else perform_command_daplink.version(args)

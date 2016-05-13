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
This module can be seen as the model of nrfjprog in the MVC design pattern.

"""
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


# The callback functions that are called from __main__.py (argparse) based on the command-line input.
# All functions follow the same structure: log (exactly what the help menu prints for the command but in different tense), initialize NRF5 device, perform functionality, cleanup.

def erase(args):
    log(args, 'Erasing the device.')

    if not args.daplink:
        perform_command_jlink.erase(args)
    else:
        perform_command_daplink.erase(args)

def halt(args):
    log(args, "Halting the device's CPU.")

    if not args.daplink:
        perform_command_jlink.halt(args)
    else:
        perform_command_daplink.halt(args)

def ids(args):
    log(args, 'Displaying the serial numbers of all debuggers connected to the PC.')

    if not args.daplink:
        perform_command_jlink.ids(args)
    else:
        perform_command_daplink.ids(args)

def memrd(args):
    log(args, "Reading the device's memory.")

    if not args.daplink:
        perform_command_jlink.memrd(args)
    else:
        perform_command_daplink.memrd(args)

def memwr(args):
    log(args, "Writing the device's memory.")

    if not args.daplink:
        perform_command_jlink.memwr(args)
    else:
        perform_command_daplink.memwr(args)

def pinresetenable(args):
    log(args, "Enabling the pin reset on nRF52 devices. Invalid command on nRF51 devices.")

    if not args.daplink:
        perform_command_jlink.pinresetenable(args)
    else:
        perform_command_daplink.pinresetenable(args)

def program(args):
    log(args, 'Programming the device.')

    if not args.daplink:
        perform_command_jlink.program(args)
    else:
        perform_command_daplink.program(args)

def readback(args):
    log(args, 'Enabling the readback protection mechanism.')

    if not args.daplink:
        perform_command_jlink.readback(args)
    else:
        perform_command_daplink.readback(args)

def readregs(args):
    log(args, 'Reading the CPU registers.')

    if not args.daplink:
        perform_command_jlink.readregs(args)
    else:
        perform_command_daplink.readregs(args)

def readtofile(args):
    log(args, "Reading and storing the device's memory.")

    if not args.daplink:
        perform_command_jlink.readtofile(args)
    else:
        perform_command_daplink.readtofile(args)

def recover(args):
    log(args, "Erasing all user FLASH and RAM and disabling any readback protection mechanisms that are enabled.")

    if not args.daplink:
        perform_command_jlink.recover(args)
    else:
        perform_command_daplink.recover(args)

def reset(args):
    log(args, 'Resetting the device.')

    if not args.daplink:
        perform_command_jlink.reset(args)
    else:
        perform_command_daplink.reset(args)

def run(args):
    log(args, "Running the device's CPU.")

    if not args.daplink:
        perform_command_jlink.run(args)
    else:
        perform_command_daplink.run(args)

def verify(args):
    log(args, "Verifying that the device's memory contains the correct data.")

    if not args.daplink:
        perform_command_jlink.verify(args)
    else:
        perform_command_daplink.verify(args)

def version(args):
    log(args, 'Displaying the nrfjprog and JLinkARM DLL versions.')

    if not args.daplink:
        perform_command_jlink.version(args)
    else:
        perform_command_daplink.version(args)

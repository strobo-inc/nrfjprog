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

import argparse

from lib import nrf5x

def _add_erase_command(subparsers):
    """
    Adds the erase sub-command and it's command-line arguments to our top-level parser.

    """
    erase_parser = subparsers.add_parser('erase', help = 'Erases the device.')
    _add_erase_group(erase_parser)
    erase_parser.set_defaults(func = nrf5x.erase)

def _add_program_command(subparsers):
    """
    Adds the program sub-command and it's command-line arguments to our top-level parser.

    """
    program_parser = subparsers.add_parser('program', help = 'Programs the device.')
    _add_file_option(program_parser)
    _add_erase_group(program_parser)
    _add_verify_option(program_parser)
    _add_reset_group(program_parser)
    program_parser.set_defaults(func = nrf5x.program)

def _add_recover_command(subparsers):
    """
    Adds the recover sub-command to our top-level parser.

    """
    recover_parser = subparsers.add_parser('recover', help = 'Erases all user FLASH and RAM and disables any readback protection mechanisms that are enabled.')
    recover_parser.set_defaults(func = nrf5x.recover)

def _add_reset_command(subparsers):
    """
    Adds the reset sub-command and it's command-line arguments to our top-level parser.

    """
    reset_parser = subparsers.add_parser('reset', help = 'Resets the device.')
    _add_reset_group(reset_parser)
    reset_parser.set_defaults(func = nrf5x.reset)

def _add_verify_command(subparsers):
    """
    Adds the verify command and it's command-line arguments to our top-level parser.

    """
    verify_parser = subparsers.add_parser('verify', help = 'Verifies that memory contains the correct data.')
    _add_file_option(verify_parser)
    verify_parser.set_defaults(func = nrf5x.verify)

def _add_version_command(subparsers):
    """
    Adds the version command to our top-level parser.

    """
    version_parser = subparsers.add_parser('version', help = 'Display the nrfjprog and JLinkARM DLL versions.')
    version_parser.set_defaults(func = nrf5x.version)

def _add_erase_group(sub_parser):
    """
    Adds the mutually exclusive group of erase options to our command.

    """
    erase_group = sub_parser.add_mutually_exclusive_group()
    erase_group.add_argument('-e', '--eraseall', action = 'store_true', help = 'Erase all user flash, including UICR, before programming the device.')
    erase_group.add_argument('-s', '--sectorserase', action = 'store_true', help = 'Erase all sectors that FILE writes before programming.')
    erase_group.add_argument('-u', '--sectorsanduicrerase', action = 'store_true', help = 'Erase all sectors that FILE writes and the UICR before programming.')

def _add_reset_group(sub_parser):
    """
    Adds the mutually exclusive group of reset options to our command.

    """
    reset_group = sub_parser.add_mutually_exclusive_group()
    reset_group.add_argument('-d', '--debugreset', action = 'store_true', help = 'Executes a debug reset.')
    reset_group.add_argument('-p', '--pinreset', action = 'store_true', help = 'Executes a pin reset.')
    reset_group.add_argument('-r', '--systemreset', action = 'store_true', help = 'Executes a system reset.')

def _add_file_option(sub_parser):
    """
    Adds the required file option to our command.

    """
    sub_parser.add_argument('-f', '--file', type = file, help = 'The hex file to be programmed to the device.', required = True)

def _add_verify_option(sub_parser):
    """
    Adds the verify option to our command.
    """
    sub_parser.add_argument('-v', '--verify', action = 'store_true', help = 'Read back memory after programming and verify that FILE was correctly written.')


parser = argparse.ArgumentParser(description='nrfjprog is a command line tool used for programming nRF5x devices.')
subparsers = parser.add_subparsers()
_add_erase_command(subparsers)
_add_program_command(subparsers)
_add_recover_command(subparsers)
_add_reset_command(subparsers)
_add_verify_command(subparsers)
_add_version_command(subparsers)

if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)  # call the default function

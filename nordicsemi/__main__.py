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
import sys

from lib import nrf5x

def _add_erase_command(subparsers):
    """
    Adds the erase sub-command and it's command-line arguments to our top-level parser.

    """
    erase_parser = subparsers.add_parser('erase', help = 'Erases the device.')
    _add_clockspeed_option(erase_parser)
    _add_erase_group(erase_parser)
    _add_quiet_option(erase_parser)
    _add_snr_option(erase_parser)
    erase_parser.set_defaults(func = nrf5x.erase)

def _add_halt_command(subparsers):
    """
    Adds the halt sub-command to our top-level parser.

    """
    halt_parser = subparsers.add_parser('halt', help = 'Halts the CPU.')
    _add_quiet_option(halt_parser)
    _add_snr_option(halt_parser)
    halt_parser.set_defaults(func = nrf5x.halt)

def _add_ids_command(subparsers):
    """
    Adds the ids sub-command to our top-level parser.

    """
    ids_parser = subparsers.add_parser('ids', help = 'Displays the serial numbers of all debuggers connected to the PC.')
    ids_parser.set_defaults(func = nrf5x.ids)

def _add_memrd_command(subparsers):
    """
    Adds the memrd sub-command to our top-level parser.

    """
    memrd_parser = subparsers.add_parser('memrd', help = 'Reads memory.')
    _add_addr_option(memrd_parser)
    _add_bytes_option(memrd_parser)
    _add_quiet_option(memrd_parser)
    _add_snr_option(memrd_parser)
    memrd_parser.set_defaults(func = nrf5x.memrd)

def _add_memwr_command(subparsers):
    """
    Adds the memwr sub-command to our top-level parser.

    """
    memwr_parser = subparsers.add_parser('memwr', help = 'Writes to memory.')
    _add_addr_option(memwr_parser)
    _add_flash_option(memwr_parser)
    _add_quiet_option(memwr_parser)
    _add_snr_option(memwr_parser)
    _add_val_option(memwr_parser)
    memwr_parser.set_defaults(func = nrf5x.memwr)

def _add_program_command(subparsers):
    """
    Adds the program sub-command and it's command-line arguments to our top-level parser.

    """
    program_parser = subparsers.add_parser('program', help = 'Programs the device.')
    _add_clockspeed_option(program_parser)
    _add_file_option(program_parser)
    _add_erase_group(program_parser)
    _add_quiet_option(program_parser)
    _add_verify_option(program_parser)
    _add_reset_group(program_parser)
    _add_snr_option(program_parser)
    program_parser.set_defaults(func = nrf5x.program)

def _add_readregs_command(subparsers):
    """
    Adds the readregs sub-command and it's command-line arguments to our top-level parser.

    """
    readregs_parser = subparsers.add_parser('readregs', help = 'Reads the CPU register.')
    _add_quiet_option(readregs_parser)
    _add_snr_option(readregs_parser)
    readregs_parser.set_defaults(func = nrf5x.readregs)

def _add_readtofile_command(subparsers):
    """
    Adds the readtofile sub-command and it's command-line arguments to our top-level parser.

    """
    readtofile_parser = subparsers.add_parser('readtofile', help = 'Reads the CPU register.')
    _add_file_option(readtofile_parser)
    _add_quiet_option(readtofile_parser)
    readtofile_parser.add_argument('--readcode', action = 'store_true', help = 'If this option is specified we will read code FLASH and store in FILE.')
    readtofile_parser.add_argument('--readram', action = 'store_true', help = 'If this option is specified we will read RAM FLASH and store in FILE.')
    readtofile_parser.add_argument('--readuicr', action = 'store_true', help = 'If this option is specified we will read UICR FLASH and store in FILE.')
    _add_snr_option(readtofile_parser)
    readtofile_parser.set_defaults(func = nrf5x.readtofile)

def _add_recover_command(subparsers):
    """
    Adds the recover sub-command to our top-level parser.

    """
    recover_parser = subparsers.add_parser('recover', help = 'Erases all user FLASH and RAM and disables any readback protection mechanisms that are enabled.')
    _add_clockspeed_option(recover_parser)
    _add_quiet_option(recover_parser)
    _add_snr_option(recover_parser)
    recover_parser.set_defaults(func = nrf5x.recover)

def _add_reset_command(subparsers):
    """
    Adds the reset sub-command and it's command-line arguments to our top-level parser.

    """
    reset_parser = subparsers.add_parser('reset', help = 'Resets the device.')
    _add_quiet_option(reset_parser)
    _add_reset_group(reset_parser)
    _add_snr_option(reset_parser)
    reset_parser.set_defaults(func = nrf5x.reset)

def _add_run_command(subparsers):
    """
    Adds the run sub-command to our top-level parser.

    """
    run_parser = subparsers.add_parser('run', help = 'Runs the CPU.')
    _add_quiet_option(run_parser)
    _add_snr_option(run_parser)
    run_parser.set_defaults(func = nrf5x.run)

def _add_verify_command(subparsers):
    """
    Adds the verify command and it's command-line arguments to our top-level parser.

    """
    verify_parser = subparsers.add_parser('verify', help = 'Verifies that memory contains the correct data.')
    _add_clockspeed_option(verify_parser)
    _add_quiet_option(verify_parser)
    _add_snr_option(verify_parser)
    _add_file_option(verify_parser)
    verify_parser.set_defaults(func = nrf5x.verify)

def _add_version_command(subparsers):
    """
    Adds the version command to our top-level parser.

    """
    version_parser = subparsers.add_parser('version', help = 'Display the nrfjprog and JLinkARM DLL versions.')
    version_parser.set_defaults(func = nrf5x.version)

def _add_erase_group(sub_parsers):
    """
    Adds the mutually exclusive group of erase options to our command.

    """
    erase_group = sub_parsers.add_mutually_exclusive_group()
    erase_group.add_argument('-e', '--eraseall', action = 'store_true', help = 'Erase all user flash, including UICR, before programming the device.')
    erase_group.add_argument('-s', '--sectorserase', action = 'store_true', help = 'Erase all sectors that FILE writes before programming.')
    erase_group.add_argument('-u', '--sectorsanduicrerase', action = 'store_true', help = 'Erase all sectors that FILE writes and the UICR before programming.')

def _add_reset_group(sub_parsers):
    """
    Adds the mutually exclusive group of reset options to our command.

    """
    reset_group = sub_parsers.add_mutually_exclusive_group()
    reset_group.add_argument('-d', '--debugreset', action = 'store_true', help = 'Executes a debug reset.')
    reset_group.add_argument('-p', '--pinreset', action = 'store_true', help = 'Executes a pin reset.')
    reset_group.add_argument('-r', '--systemreset', action = 'store_true', help = 'Executes a system reset.')

def _add_addr_option(sub_parsers):
    """
    Adds the required addr option to our command.

    """
    sub_parsers.add_argument('-a', '--addr', type = int, help = 'The address in memory to be read/write.', required = True)

def _add_bytes_option(sub_parsers):
    """
    Adds the bytes option to our command.

    """
    sub_parsers.add_argument('-b', '--bytes', type = int, help = 'The number of bytes to be read. By default 4, one word.', default = 4)

def _add_clockspeed_option(sub_parsers):
    """
    Adds the clockspeed option to our command.

    """
    sub_parsers.add_argument('-c', '--clockspeed', type = int, help = 'Sets the debugger SWD clock speed in kHz.')

def _add_file_option(sub_parsers):
    """
    Adds the required file option to our command.

    """
    sub_parsers.add_argument('-f', '--file', type = file, help = 'The hex file to be programmed to the device.', required = True)

def _add_flash_option(sub_parsers):
    """
    Adds the flash option to our command.

    """
    sub_parsers.add_argument('--flash', action = 'store_true', help = 'If this option is specified we will write to FLASH. If not we will write to RAM.')

def _add_quiet_option(sub_parsers):
    """
    Adds the quiet option to our command.

    """
    sub_parsers.add_argument('-q', '--quiet', action =  'store_true', help = 'Will not print to terminal.' )

def _add_snr_option(sub_parsers):
    """
    Adds the snr option to our command.

    """
    sub_parsers.add_argument('--snr', type = int, help = 'Selects the debugger with the given serial number among all those connected to the PC for the operation.')

def _add_val_option(sub_parsers):
    """
    Adds the value option to our command.

    """
    sub_parsers.add_argument('--val', type = int, help = 'The data word to be written to memory.', required = True)

def _add_verify_option(sub_parsers):
    """
    Adds the verify option to our command.

    """
    sub_parsers.add_argument('-v', '--verify', action = 'store_true', help = 'Read back memory after programming and verify that FILE was correctly written.')

def main(argv):
    parser = argparse.ArgumentParser(description='nrfjprog is a command line tool used for programming nRF5x devices.')
    subparsers = parser.add_subparsers()
    _add_erase_command(subparsers)
    _add_halt_command(subparsers)
    _add_ids_command(subparsers)
    _add_memrd_command(subparsers)
    _add_memwr_command(subparsers)
    _add_program_command(subparsers)
    _add_readregs_command(subparsers)
    _add_readtofile_command(subparsers)
    _add_recover_command(subparsers)
    _add_reset_command(subparsers)
    _add_run_command(subparsers)
    _add_verify_command(subparsers)
    _add_version_command(subparsers)

    args = parser.parse_args()
    args.func(args)  # call the default function

if __name__ == '__main__':
    main(sys.argv)
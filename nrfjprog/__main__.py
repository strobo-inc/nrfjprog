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

from device import nrf5x

NRFJPROG_DESCRIPTION = "nrfjprog is a command line tool used for programming nRF5x devices. It is implemented in Python and utilizes pynrfjprog, a Python wrapper for the nrfjprog DLL. Both nrfjprog and pynrfjprog are open source and can be found on Nordic's GitHub. To report an issue, request a feature, or contribute please see: https://github.com/mjdietzx/nrfjprog."
NRFJPROG_EPILOG = "Just like any standard command line tool, one positional command can be specified, followed by it's specific arguments. To see arguments for a specific command type: python nrfjprog COMMAND -h (i.e. python nrfjprog erase -h)."

"""
The top-level positional commands of our command-line interface. These then contain their own unique and shared options.

"""

def _add_erase_command(subparsers):
    erase_parser = subparsers.add_parser('erase', help = "Erases the device's FLASH.")
    _add_clockspeed_argument(erase_parser)
    _add_erase_group(erase_parser)
    _add_quiet_argument(erase_parser)
    _add_snr_argument(erase_parser)
    erase_parser.set_defaults(func = nrf5x.erase)

def _add_halt_command(subparsers):
    halt_parser = subparsers.add_parser('halt', help = "Halts the device's CPU.")
    _add_quiet_argument(halt_parser)
    _add_snr_argument(halt_parser)
    halt_parser.set_defaults(func = nrf5x.halt)

def _add_ids_command(subparsers): # This is the only command that doesn't have the snr and quiet option.
    ids_parser = subparsers.add_parser('ids', help = 'Displays the serial numbers of all debuggers connected to the PC.')
    ids_parser.set_defaults(func = nrf5x.ids)

def _add_memrd_command(subparsers):
    memrd_parser = subparsers.add_parser('memrd', help = "Reads the device's memory.")
    _add_addr_argument(memrd_parser)
    _add_length_argument(memrd_parser)
    _add_quiet_argument(memrd_parser)
    _add_snr_argument(memrd_parser)
    memrd_parser.set_defaults(func = nrf5x.memrd)

def _add_memwr_command(subparsers):
    memwr_parser = subparsers.add_parser('memwr', help = "Writes one word in the device's memory.")
    _add_addr_argument(memwr_parser)
    _add_flash_argument(memwr_parser)
    _add_quiet_argument(memwr_parser)
    _add_snr_argument(memwr_parser)
    _add_val_argument(memwr_parser)
    memwr_parser.set_defaults(func = nrf5x.memwr)

def _add_program_command(subparsers):
    program_parser = subparsers.add_parser('program', help = 'Programs the device.')
    _add_clockspeed_argument(program_parser)
    _add_file_argument(program_parser)
    _add_erase_before_flash_group(program_parser)
    _add_quiet_argument(program_parser)
    _add_verify_argument(program_parser)
    _add_reset_group(program_parser)
    _add_snr_argument(program_parser)
    program_parser.set_defaults(func = nrf5x.program)

def _add_readregs_command(subparsers):
    readregs_parser = subparsers.add_parser('readregs', help = 'Reads the CPU registers.')
    _add_quiet_argument(readregs_parser)
    _add_snr_argument(readregs_parser)
    readregs_parser.set_defaults(func = nrf5x.readregs)

def _add_readtofile_command(subparsers):
    readtofile_parser = subparsers.add_parser('readtofile', help = "Reads and stores the device's memory.")
    _add_file_argument(readtofile_parser)
    _add_quiet_argument(readtofile_parser)
    _add_readcode_argument(readtofile_parser)
    _add_readram_argument(readtofile_parser)
    _add_readuicr_argument(readtofile_parser)
    _add_snr_argument(readtofile_parser)
    readtofile_parser.set_defaults(func = nrf5x.readtofile)

def _add_recover_command(subparsers):
    recover_parser = subparsers.add_parser('recover', help = 'Erases all user FLASH and RAM and disables any readback protection mechanisms that are enabled.')
    _add_clockspeed_argument(recover_parser)
    _add_quiet_argument(recover_parser)
    _add_snr_argument(recover_parser)
    recover_parser.set_defaults(func = nrf5x.recover)

def _add_reset_command(subparsers):
    reset_parser = subparsers.add_parser('reset', help = 'Resets the device.')
    _add_quiet_argument(reset_parser)
    _add_reset_group(reset_parser)
    _add_snr_argument(reset_parser)
    reset_parser.set_defaults(func = nrf5x.reset)

def _add_run_command(subparsers):
    run_parser = subparsers.add_parser('run', help = "Runs the device's CPU.")
    _add_quiet_argument(run_parser)
    _add_snr_argument(run_parser)
    run_parser.set_defaults(func = nrf5x.run)

def _add_verify_command(subparsers):
    verify_parser = subparsers.add_parser('verify', help = "Verifies that the device's memory contains the correct data.")
    _add_clockspeed_argument(verify_parser)
    _add_quiet_argument(verify_parser)
    _add_snr_argument(verify_parser)
    _add_file_argument(verify_parser)
    verify_parser.set_defaults(func = nrf5x.verify)

def _add_version_command(subparsers):
    version_parser = subparsers.add_parser('version', help = 'Display the nrfjprog and JLinkARM DLL versions.')
    version_parser.set_defaults(func = nrf5x.version)

"""
Mutually exclusive groups. argparse will make sure one of the arguments in a mutually exclusive group was present on the command-line.

"""

def _add_erase_group(subparsers):
    erase_group = subparsers.add_mutually_exclusive_group()
    _add_eraseall_argument(erase_group)
    _add_erasepage_argument(erase_group)
    _add_eraseuicr_argument(erase_group)

def _add_erase_before_flash_group(subparsers):
    erase_before_flash_group = subparsers.add_mutually_exclusive_group()
    _add_eraseall_argument(erase_before_flash_group)
    _add_sectors_erase(erase_before_flash_group)
    _add_sectorsuicr_erase(erase_before_flash_group)

def _add_reset_group(subparsers):
    reset_group = subparsers.add_mutually_exclusive_group()
    _add_debugreset_argument(reset_group)
    _add_pinreset_argument(reset_group)
    _add_sysreset_argument(reset_group)

"""
The add_argument helper functions. They define how a single command-line argument should be parsed. These are all options.

"""

def auto_int(x):
    """
    Needed in order to accomodate base 16 (hex) and base 10 (decimal) parameters we can enable auto base detection.

    """
    return int(x, 0)

def _add_addr_argument(subparsers):
    subparsers.add_argument('-a', '--addr', type = auto_int, help = 'The address in memory to be read/written.', required = True)

def _add_clockspeed_argument(subparsers):
    subparsers.add_argument('-c', '--clockspeed', type = int, metavar = 'CLOCKSPEEDKHZ', help = 'Sets the debugger SWD clock speed in kHz for the operation.')

def _add_debugreset_argument(subparsers):
    subparsers.add_argument('-d', '--debugreset', action = 'store_true', help = 'Executes a debug reset.')

def _add_eraseall_argument(subparsers):
    subparsers.add_argument('-e', '--eraseall', action = 'store_true', help = 'Erase all user FLASH including UICR.')

def _add_erasepage_argument(subparsers):
    subparsers.add_argument('--erasepage', type = auto_int, metavar = 'PAGESTARTADDR', help = 'Erase the page starting at the address PAGESTARTADDR.')

def _add_eraseuicr_argument(subparsers):
    subparsers.add_argument('--eraseuicr', action = 'store_true', help = 'Erase the UICR page in FLASH.')

def _add_file_argument(subparsers):
    subparsers.add_argument('-f', '--file', type = file, help = 'The hex file to be used in this operation.', required = True)

def _add_flash_argument(subparsers):
    subparsers.add_argument('--flash', action = 'store_true', help = 'If this argument is specified write to FLASH using the NVMC. Else write to RAM.')

def _add_length_argument(subparsers):
    subparsers.add_argument('-l', '--length', type = auto_int, help = 'The number of bytes to be read. 4 (one word) by default.', default = 4)

def _add_pinreset_argument(subparsers):
    subparsers.add_argument('-p', '--pinreset', action = 'store_true', help = 'Executes a pin reset.')

def _add_quiet_argument(subparsers):
    subparsers.add_argument('-q', '--quiet', action =  'store_true', help = 'Nothing will be printed to terminal during the operation.' )

def _add_readcode_argument(subparsers):
    subparsers.add_argument('--readcode', action = 'store_true', help = 'If this argument is specified read code FLASH and store in FILE.')

def _add_readram_argument(subparsers):
    subparsers.add_argument('--readram', action = 'store_true', help = 'If this argument is specified read RAM and store in FILE.')

def _add_readuicr_argument(subparsers):
    subparsers.add_argument('--readuicr', action = 'store_true', help = 'If this argument is specified read UICR FLASH and store in FILE.')

def _add_sectors_erase(subparsers):
    subparsers.add_argument('-se', '--sectorserase', action = 'store_true', help = 'Erase all sectors that FILE contains data in before programming.')

def _add_sectorsuicr_erase(subparsers):
    subparsers.add_argument('-u', '--sectorsanduicrerase', action = 'store_true', help = 'Erase all sectors that FILE contains data in and the UICR (unconditionally) before programming.')

def _add_snr_argument(subparsers):
    subparsers.add_argument('-s', '--snr', type = int, help = 'Selects the debugger with the given serial number among all those connected to the PC for the operation.')

def _add_sysreset_argument(subparsers):
    subparsers.add_argument('-r', '--systemreset', action = 'store_true', help = 'Executes a system reset.')

def _add_val_argument(subparsers):
    subparsers.add_argument('--val', type = auto_int, help = 'The 32 bit word to be written to memory.', required = True)

def _add_verify_argument(subparsers):
    subparsers.add_argument('-v', '--verify', action = 'store_true', help = 'Read back memory and verify that it matches FILE.')

"""
The top-level functionality of our command-line application.

"""

def _add_commands(subparsers):
    """
    Split up the functionality of nrfjprog into multiple sub-commands because nrfjprog performs several different functions which require different command-line arguments.
    
    :param Special Action Object subparsers: https://docs.python.org/3/library/argparse.html#sub-commands
    """
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

def main(argv):
    """
    Set up a command line interface using the argparse module.

    Above we will define what arguments our program requires and argparse will figure out how to parse those from sys.argv.
    For info on argparse see: https://docs.python.org/3/library/argparse.html.
    """
    parser = argparse.ArgumentParser(description = NRFJPROG_DESCRIPTION, epilog = NRFJPROG_EPILOG)
    subparsers = parser.add_subparsers()

    _add_commands(subparsers)

    args = parser.parse_args()
    args.func(args)  # Call the default function. (i.e. nRF5x.erase() in the erase command).

if __name__ == '__main__':
    main(sys.argv)
 
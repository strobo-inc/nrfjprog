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
This module sets up and runs the command-line-interface for nrfjprog.

It receives the command and options from the user and passes it to model/perform_command.py.
"""

import argparse

from .model import perform_command


class Nrfjprog(object):
    """
    Class that handles the command-line interface.

    """

    nrfjprog_description = "nrfjprog is a command line tool used for programming nRF5x devices. It is implemented in Python and utilizes pynrfjprog, a Python wrapper for the nrfjprog DLL. Both nrfjprog and pynrfjprog are open source and can be found on Nordic's GitHub. To report an issue, request a feature, or contribute please see: https://github.com/mjdietzx/nrfjprog."
    nrfjprog_epilog = "Just like any standard command line tool, one positional command can be specified, followed by it's specific arguments. To see arguments for a specific command type: python nrfjprog COMMAND -h (i.e. python nrfjprog erase -h)."

    def __init__(self):
        """
        Initializes the command-line interface.

        """
        self.parser = argparse.ArgumentParser(description=self.nrfjprog_description, epilog=self.nrfjprog_epilog)
        self.subparsers = self.parser.add_subparsers()
        self.args = None

        self._add_commands()

    def add_common_properties_to_command(self, parser, callback, connects=True):
        """
        Adds the common arguments each command shares and specifies the callback that will perform the requested functionality.
        All commands except the 'ids' and 'version' command share these arguments.

        @param ArgumentParser parser:   The top-level positional command to add the shared arguments to.
        @param func           callback: Function that performs operation for given command.
        @param boolean        connects: If this command connects to the emulator (debugger) and should have the option to set the clock speed/serial number.
        """
        self._add_quiet_argument(parser)

        if connects:
            self._add_clockspeed_argument(parser)
            self._add_snr_argument(parser)

        parser.set_defaults(func=callback)

    def run(self):
        """
        Parse user input and execute the requested functionality.

        """
        self.args = self.parser.parse_args()
        self.args.func(self.args)

    def _add_commands(self):
        """
        Split up the functionality of nrfjprog into multiple sub-commands.

        :param Object subparsers: https://docs.python.org/3/library/argparse.html#sub-commands.
        """
        self._add_erase_command()
        self._add_halt_command()
        self._add_ids_command()
        self._add_memrd_command()
        self._add_memwr_command()
        self._add_pinresetenable_command()
        self._add_program_command()
        self._add_readback_command()
        self._add_readregs_command()
        self._add_readtofile_command()
        self._add_recover_command()
        self._add_reset_command()
        self._add_run_command()
        self._add_verify_command()
        self._add_version_command()

    # The top-level positional commands of our command-line interface.

    def _add_erase_command(self):
        erase_parser = self.subparsers.add_parser('erase', help="Erases the device's FLASH.")
        self.add_common_properties_to_command(erase_parser, perform_command.erase)

        self._add_erase_group(erase_parser)

    def _add_halt_command(self):
        halt_parser = self.subparsers.add_parser('halt', help="Halts the device's CPU.")
        self.add_common_properties_to_command(halt_parser, perform_command.halt)

    def _add_ids_command(self):
        ids_parser = self.subparsers.add_parser('ids', help='Displays the serial numbers of all debuggers connected to the PC.')
        self.add_common_properties_to_command(ids_parser, perform_command.ids, connects=False)

    def _add_memrd_command(self):
        memrd_parser = self.subparsers.add_parser('memrd', help="Reads the device's memory.")
        self.add_common_properties_to_command(memrd_parser, perform_command.memrd)

        self._add_addr_argument(memrd_parser)
        self._add_length_argument(memrd_parser)

    def _add_memwr_command(self):
        memwr_parser = self.subparsers.add_parser('memwr', help="Writes one word in the device's memory.")
        self.add_common_properties_to_command(memwr_parser, perform_command.memwr)

        self._add_addr_argument(memwr_parser)
        self._add_val_argument(memwr_parser)

    def _add_pinresetenable_command(self):
        pinresetenable_parser = self.subparsers.add_parser('pinresetenable', help="Enable the pin reset (GPIO 21) on nRF52 devices. Invalid command on nRF51 devices.")
        self.add_common_properties_to_command(pinresetenable_parser, perform_command.pinresetenable)

    def _add_program_command(self):
        program_parser = self.subparsers.add_parser('program', help='Programs the device.')
        self.add_common_properties_to_command(program_parser, perform_command.program)

        self._add_file_argument(program_parser)
        self._add_erase_before_flash_group(program_parser)
        self._add_verify_argument(program_parser)
        self._add_reset_group(program_parser)

    def _add_readback_command(self):
        readback_parser = self.subparsers.add_parser('rbp', help='Enables the readback protection mechanism.')
        self.add_common_properties_to_command(readback_parser, perform_command.readback)

        self._add_rbplevel_argument(readback_parser)

    def _add_readregs_command(self):
        readregs_parser = self.subparsers.add_parser('readregs', help='Reads the CPU registers.')
        self.add_common_properties_to_command(readregs_parser, perform_command.readregs)

    def _add_readtofile_command(self):
        readtofile_parser = self.subparsers.add_parser('readtofile', help="Reads and stores the device's memory.")
        self.add_common_properties_to_command(readtofile_parser, perform_command.readtofile)

        self._add_file_argument(readtofile_parser)
        self._add_readcode_argument(readtofile_parser)
        self._add_readram_argument(readtofile_parser)
        self._add_readuicr_argument(readtofile_parser)

    def _add_recover_command(self):
        recover_parser = self.subparsers.add_parser('recover', help='Erases all user FLASH and RAM and disables any readback protection mechanisms that are enabled.')
        self.add_common_properties_to_command(recover_parser, perform_command.recover)

        self._add_family_argument(recover_parser)

    def _add_reset_command(self):
        reset_parser = self.subparsers.add_parser('reset', help='Resets the device.')
        self.add_common_properties_to_command(reset_parser, perform_command.reset)

        self._add_reset_group(reset_parser)

    def _add_run_command(self):
        run_parser = self.subparsers.add_parser('run', help="Runs the device's CPU.")
        self.add_common_properties_to_command(run_parser, perform_command.run)

        self._add_pc_argument(run_parser)
        self._add_sp_argument(run_parser)

    def _add_verify_command(self):
        verify_parser = self.subparsers.add_parser('verify', help="Verifies that the device's memory contains the correct data.")
        self.add_common_properties_to_command(verify_parser, perform_command.verify)

        self._add_file_argument(verify_parser)

    def _add_version_command(self):
        version_parser = self.subparsers.add_parser('version', help='Display the nrfjprog and JLinkARM DLL versions.')
        self.add_common_properties_to_command(version_parser, perform_command.version, connects=False)

    # Mutually exclusive groups. argparse will make sure only one of the arguments in a mutually exclusive group was present on the command-line.

    def _add_erase_group(self, parser):
        erase_group = parser.add_mutually_exclusive_group()
        self._add_eraseall_argument(erase_group)
        self._add_erasepage_argument(erase_group)
        self._add_eraseuicr_argument(erase_group)

    def _add_erase_before_flash_group(self, parser):
        erase_before_flash_group = parser.add_mutually_exclusive_group()
        self._add_eraseall_argument(erase_before_flash_group)
        self._add_sectors_erase_argument(erase_before_flash_group)
        self._add_sectorsuicr_erase_argument(erase_before_flash_group)

    def _add_reset_group(self, parser):
        reset_group = parser.add_mutually_exclusive_group()
        self._add_debugreset_argument(reset_group)
        self._add_pinreset_argument(reset_group)
        self._add_sysreset_argument(reset_group)

    # The add_argument helper functions. They define how a single command-line argument should be parsed. These are all options.

    def _add_addr_argument(self, parser):
        parser.add_argument('-a', '--addr', type=self.auto_int, help='The address in memory to be read/written.', required=True)

    def _add_clockspeed_argument(self, parser):
        parser.add_argument('-c', '--clockspeed', type=int, metavar='CLOCKSPEEDKHZ', help='Sets the debugger SWD clock speed in kHz for the operation.')

    def _add_debugreset_argument(self, parser):
        parser.add_argument('-d', '--debugreset', action='store_true', help='Executes a debug reset.')

    def _add_eraseall_argument(self, parser):
        parser.add_argument('-e', '--eraseall', action='store_true', help='Erase all user FLASH including UICR.')

    def _add_erasepage_argument(self, parser):
        parser.add_argument('--erasepage', type=self.auto_int, metavar='PAGESTARTADDR', help='Erase the page starting at the address PAGESTARTADDR.')

    def _add_eraseuicr_argument(self, parser):
        parser.add_argument('--eraseuicr', action='store_true', help='Erase the UICR page in FLASH.')

    def _add_family_argument(self, parser):
        parser.add_argument('--family', type=str, help='The family of the target device.', required=True, choices=['NRF51', 'NRF52'])

    def _add_file_argument(self, parser):
        parser.add_argument('-f', '--file', help='The hex file to be used in this operation.', required=True)

    def _add_length_argument(self, parser):
        parser.add_argument('-l', '--length', type=self.auto_int, help='The number of bytes to be read. 4 (one word) by default.', default=4)

    def _add_pc_argument(self, parser):
        parser.add_argument('--pc', type=self.auto_int, metavar='PC_ADDR', help='Initial program counter to start the CPU running from.')

    def _add_pinreset_argument(self, parser):
        parser.add_argument('-p', '--pinreset', action='store_true', help='Executes a pin reset.')

    def _add_quiet_argument(self, parser):
        parser.add_argument('-q', '--quiet', action='store_true', help='Nothing will be printed to terminal during the operation.')

    def _add_rbplevel_argument(self, parser):
        parser.add_argument('--rbplevel', help='Specify the read back protection level (NRF51 only).', choices=['CR0', 'ALL'])

    def _add_readcode_argument(self, parser):
        parser.add_argument('--readcode', action='store_true', help='If this argument is specified read code FLASH and store in FILE.')

    def _add_readram_argument(self, parser):
        parser.add_argument('--readram', action='store_true', help='If this argument is specified read RAM and store in FILE.')

    def _add_readuicr_argument(self, parser):
        parser.add_argument('--readuicr', action='store_true', help='If this argument is specified read UICR FLASH and store in FILE.')

    def _add_sectors_erase_argument(self, parser):
        parser.add_argument('-se', '--sectorserase', action='store_true', help='Erase all sectors that FILE contains data in before programming.')

    def _add_sectorsuicr_erase_argument(self, parser):
        parser.add_argument('-u', '--sectorsanduicrerase', action='store_true', help='Erase all sectors that FILE contains data in and the UICR (unconditionally) before programming.')

    def _add_snr_argument(self, parser):
        parser.add_argument('-s', '--snr', type=int, help='Selects the debugger with the given serial number among all those connected to the PC for the operation.')

    def _add_sp_argument(self, parser):
        parser.add_argument('--sp', type=self.auto_int, metavar='SP_ADDR', help='Initial stack pointer.')

    def _add_sysreset_argument(self, parser):
        parser.add_argument('-r', '--systemreset', action='store_true', help='Executes a system reset.')

    def _add_val_argument(self, parser):
        parser.add_argument('--val', type=self.auto_int, help='The 32 bit word to be written to memory.', required=True)

    def _add_verify_argument(self, parser):
        parser.add_argument('-v', '--verify', action='store_true', help='Read back memory and verify that it matches FILE.')


    # Helpers.

    @staticmethod
    def auto_int(number):
        """
        Needed in order to accommodate base 16 (hex) and base 10 (decimal) parameters we can enable auto base detection.

        """
        return int(number, 0)


def main():
    """
    Set up a command line interface using the argparse module.

    Above we will define what arguments our program requires and argparse will figure out how to parse those from sys.argv.
    For info on argparse see: https://docs.python.org/3/library/argparse.html.
    """
    cli = Nrfjprog()
    cli.run()


if __name__ == '__main__':
    main()

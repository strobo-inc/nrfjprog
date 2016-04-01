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
Test nrfjprog.exe that was built from our repo.

Must add tests/dist on system running this script where dist/ contains the built exe and all it's dependencies.
"""

import subprocess
import sys
import unittest

from pynrfjprog import API


if sys.platform.lower().startswith('win'):
    PATH_TO_EXE = "dist\\windows_64\\nrfjprog.exe"
elif sys.platform.lower().startswith('linux'):
    PATH_TO_EXE = "dist\\linux_64\\nrfjprog"
elif sys.platform.lower().startswith('dar'):
    PATH_TO_EXE = "dist\\mac_osx_64\\nrfjprog"


def run_exe(cmd):
    """
    Run nrfjprog with the given commands.

    :param List cmd: Commands to run nrfjprog with.
    """
    command = []
    command.append(PATH_TO_EXE)
    command.extend(cmd)
    return subprocess.call(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def setup_api():
    """
    Initialize api and connect to the target device.

    :return Object api: Instance of API that is initialized and connected to the target device.
    """
    api = API.API('NRF52')
    api.open()
    api.connect_to_emu_without_snr()
    return api

class TestHelpScreens(unittest.TestCase):
    """


    """
    def test_help(self):
        self.assertTrue(run_exe(["-h"]) == 0)

    def test_command_help(self):
        self.assertTrue(run_exe(["program", "-h"]) == 0)

class TestEraseCommand(unittest.TestCase):
    """


    """
    def test_erase_help(self):
        self.assertTrue(run_exe(["erase", "-h"]) == 0)

    def test_erase(self):
        api = setup_api()
        
        api.write_u32(0x0, 0x0, True)

        run_exe(["erase"])

        self.assertTrue(api.read_u32(0x0) == 0xFFFFFFFF)

if __name__ == '__main__':
    """


    """
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEraseCommand)
    unittest.TextTestRunner(verbosity=2).run(suite)

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

from pynrfjprog import API, Hex

MAX_UNSIGNED_32_BIT = 0xFFFFFFFF

"""
Device specific info.

"""

FLASH_SIZE = {'NRF52_FP1'   : 0x80000,
              'NRF51_XLR3P' : 0x40000}

RAM_SIZE = {'NRF52_FP1'   : 0x10000,
            'NRF51_XLR3P' : 0x8000}

PAGE_SIZE = {'NRF52_FP1'   : 0x1000,
             'NRF51_XLR3P' : 0x400}

class NRF5xDevice:
    """
    Class representing an nRF5x device.

    """
    FLASH_START = 0x0
    RAM_START = 0x20000000
    FICR_START = 0x10000000
    UICR_START = 0x10001000

    def __init__(self, device_version):
        """
        Initialize the device specific specs.

        """
        self.FLASH_END = self.FLASH_START + FLASH_SIZE[device_version]
        self.RAM_END = self.RAM_START + RAM_SIZE[device_version]

        self.PAGE_SIZE = PAGE_SIZE[device_version]

        self.FICR_END = self.FICR_START + self.PAGE_SIZE
        self.UICR_END = self.UICR_START + self.PAGE_SIZE

        self.FLASH_SIZE = self.FLASH_END - self.FLASH_START
        self.RAM_SIZE = self.RAM_END - self.RAM_START

        self.NUMBER_OF_FLASH_PAGES_IN_CODE = self.FLASH_SIZE / self.PAGE_SIZE

    def error_check(self, args):
        """
        We need to check all CUSTOM user input to the command-line interface for errors.

        :param Object  args:                  The arguments the command was called with.
        """
        self._in_args(args)

        if self.erasepage != None:
            page_number = self.erasepage % self.PAGE_SIZE
            self._assert(page_number == 0 and (self.erasepage / self.PAGE_SIZE) < self.NUMBER_OF_FLASH_PAGES_IN_CODE)
        if self.length != None:
            self._assert(self.length > 0)
        if self.val != None:
            self._assert(self.val >= 0 and self.val <= MAX_UNSIGNED_32_BIT)

    def _assert(self, condition):
        """
        How do we want to return errors?

        """
        assert(condition), 'ERROR!'

    def _in_args(self, args):
        """
        Check which arguments exist in the args Namespace store the ones that do as properties (although they may be None).

        """
        try:
            self.addr = args.addr
        except:
            self.addr = None
        try:
            self.erasepage = args.erasepage
        except:
            self.erasepage = None
        try:
            self.file = args.file
        except:
            self.file = None
        try:
            self.length = args.length
        except:
            self.length = None
        try:
            self.pc = args.pc
        except:
            self.pc = None
        try:
            self.sp = args.sp
        except:
            self.sp = None
        try:
            self.val = args.val
        except:
            self.val = None
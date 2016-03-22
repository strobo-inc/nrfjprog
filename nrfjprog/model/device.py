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

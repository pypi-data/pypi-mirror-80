#   Copyright (c) 2017, Xilinx, Inc.
#   All rights reserved.
#
#   Redistribution and use in source and binary forms, with or without
#   modification, are permitted provided that the following conditions are met:
#
#   1.  Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#   2.  Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
#   3.  Neither the name of the copyright holder nor the names of its
#       contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
#
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#   AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#   THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#   PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
#   CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#   EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#   OR BUSINESS INTERRUPTION). HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
#   WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
#   OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
#   ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import pynq
from pynq import GPIO
import pynq.lib
import pynq.lib.video
import pynq.lib.audio
from .constants import *

__author__ = "Peter Ogden, Yun Rock Qu"
__copyright__ = "Copyright 2017, Xilinx"
__email__ = "pynq_support@xilinx.com"


class BaseOverlay(pynq.Overlay):
    """ The Base overlay for the Pynq-atk

    This overlay is designed to interact with all of the on board peripherals
    and external interfaces of the Pynq-atk board. It exposes the following
    attributes:

    Attributes
    ----------
    iop_arduino : IOP
         IO processor connected to the Arduino interface
    leds : AxiGPIO
         3-bit output GPIO for interacting with the LEDs LD0-2
    buttons : AxiGPIO
         2-bit input GPIO for interacting with the buttons BTN0-2
    tpad : AxiGPIO
         1-bit input GPIO for interacting with the tpad
    rgbleds : [pynq.board.RGBLED]
         Wrapper for GPIO for LD4 and LD5 multicolour LEDs
    video : pynq.lib.video.HDMIWrapper
         HDMI input and output interfaces
    audio : pynq.lib.audio.Audio
         Headphone jack and on-board microphone

    """

    def __init__(self, bitfile, **kwargs):
        super().__init__(bitfile, **kwargs)
        if self.is_loaded():
            self.iop_arduino.mbtype = "Arduino"

            self.ARDUINO = self.iop_arduino.mb_info

#            self.audio = self.audio_codec_ctrl_0

            self.leds = self.leds_gpio.channel1
            self.buttons = self.btns_gpio.channel1
            self.tpad = self.touch_gpio.channel1
            self.beep = self.beep_gpio.channel1
            self.leds.setlength(3)
            self.tpad.setlength(1)
            self.buttons.setlength(2)
            self.beep.setlength(1)
            self.leds.setdirection("out")
            self.beep.setdirection("out")
            self.tpad.setdirection("in")
            self.buttons.setdirection("in")

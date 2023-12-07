#!/usr/bin/env python3
#

import sys
import os
import time
from enum import IntEnum
import numpy as np

from tango import AttrQuality, AttrWriteType, DispLevel, DevState, DebugIt
from tango.server import Device, attribute, command, pipe, device_property

from PMT1002 import Photomultiplier

class PMT1002(Device):

    # -----------------
    # Device Properties
    # -----------------

    serial = device_property(dtype='DevString', default_value = 'L2730020')

    # ----------
    # Attributes
    # ----------

    lpfilter = attribute(dtype = 'DevEnum',
        label = 'lowpass filter frequency',
        enum_labels = ['250 kHz', '2.5 MHz', '80 MHz'],
        access = AttrWriteType.READ_WRITE,)

    voltage = attribute(
        dtype='DevFloat',
        access=AttrWriteType.READ_WRITE,
        label="Voltage",
        unit="V",
        format="%3.2f",
        min_value = 0.5,
        max_value = 1.09,
        doc="Applied voltage; must be between 0.5V and 1.09V",
    )

    output = attribute(
        dtype='DevBoolean',
        access=AttrWriteType.READ_WRITE,
        label="Active",
        doc="is on?",
    )


    # ---------------
    # General methods
    # ---------------

    def init_device(self):
        Device.init_device(self)
        self.device = Photomultiplier(self.serial)
        self.device.Off()
        self.FREQUENCIES = [250000, 2500000, 80000000]

    # ------------------
    # Attributes methods
    # ------------------
    
    ### READ COMMANDS ###
   
    def read_lpfilter(self):
        ret = int(self.device.get_FilterFreq()[:-2])
        if ret == 250000:
            return 0
        elif ret == 2500000:
            return 1
        elif ret == 80000000:
            return 2

    def read_voltage(self):
        ret = float(self.device.get_Voltage()[:-1])
        return ret

    def read_output(self):
        ret = int(self.device.Status())
        if ret == 1:
            self.set_state(DevState.ON)
            return True
        else:
            self.set_state(DevState.OFF)
            return False

    ### WRITE COMMANDS ###

    def write_lpfilter(self,value):
        return self.device.set_FilterFreq(self.FREQUENCIES[value])

    def write_voltage(self,value):
        return self.device.set_Voltage(value)

    def write_output(self,value):
        if value:
            self.device.On()
            time.sleep(0.1)
            return self.read_output()
        else:
            self.device.Off()
            time.sleep(0.1)
            return self.read_output()

if __name__ == "__main__":
    PMT1002.run_server()


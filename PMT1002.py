#!/usr/bin/env python3
#

import pyvisa
import easy_scpi as scpi
import time

class Photomultiplier():
    def __init__(self, serial):
        __rm = pyvisa.ResourceManager()
        __devs = __rm.list_resources('USB')
        for dev in __devs:
            if serial in dev:
                self.inst = scpi.Instrument(dev)
                print('Serial number '+serial+' found at address '+dev[:4])
        self.inst.connect()
        self.inst.init()

    def connect(self):
        self.inst.connect()

    def disconnect(self):
        self.inst.disconnect()

    def Status(self):
        self.inst.query('SENS:FUNC:STAT? H10721')
        time.sleep(0.1)
        return self.inst.read()

    def On(self):
        self.inst.query('SENS:FUNC:ON H10721')
        self.Status()
        return self.inst.read()

    def Off(self):
        self.inst.query('SENS:FUNC:OFF H10721')
        self.Status()
        return self.inst.read()

    def get_FilterFreq(self):
        self.inst.query('SENS:FILT:LPAS:FREQ?')
        time.sleep(0.1)
        return self.inst.read()

    def set_FilterFreq(self, f):
        #f = 250_000, 2_500_000, or 80_000_000
        comm = 'SENS:FILT:LPAS:FREQ '+str(f)
        self.inst.query(comm)
        time.sleep(0.1)
        return self.get_FilterFreq()

    def get_Voltage(self):
        self.inst.query('SOUR:VOLT?')
        time.sleep(0.1)
        return self.inst.read()

    def set_Voltage(self, V):
        #V must be between 0.5 and 1.09 (measured in Volt).
        if V>1.09:
            V = 1.09
            print('WARNING: set voltage exceeds maximum of 1.09 V. Setting Voltage to 1.09 V')
        if V<0.5:
            V = 0.5
            print('WARNING: set voltage below minimum of 0.5 V. Setting Voltage to 0.5 V')
        comm = 'SOUR:VOLT '+str(V)
        self.inst.query(comm)
        time.sleep(0.1)
        return self.get_Voltage()
        

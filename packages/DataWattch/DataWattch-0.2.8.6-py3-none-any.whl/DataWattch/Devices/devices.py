# Release 0.2/
# Author D. Driessen
# Copyright (c) 2020  Ascos
# Python 3

import time
from typing import List
from .. import stm_communication as GPIO
import RPi.GPIO as GPIOi

# function to send new inits to stm
def send_init(strings: List[str]):
    try:
        for string in strings:

            if string == 'input':
                GPIO.set_inputs()
            elif string == 'output':
                GPIO.set_outputs()
            elif string == 'interrupt':
                GPIO.set_interrupts()
            elif string == 'pupd':
                GPIO.set_pupd()
            time.sleep(0.1)
    except Exception as e:
        return str(e)


# std. device class for storing data etc.
class Device(object):
    def __init__(self, idx, HWType, Stype):
        self.idx = idx
        self.HWType = HWType
        self.Stype = Stype


# Counter device
class DeviceCounter(object):

    def __init__(self, idx: int, hwtype: str, stype: str, name: str, link: int, flank='both'):
        self.idx = idx
        self.hw_type = hwtype
        self.s_type = stype
        self.name = name + '_' + str(link)
        self.value = 0
        self.update = False
        self.__prevvalue = 0
        GPIO.input_enable(link)
        GPIO.interrupt_enable(link, flank)
        GPIO.pupd_enable(link, 'pull-up')

    def get_counter_value(self):
        try:
            val = GPIO.get_single_pulse_counter(int(self.name[-1]))
            if val == 0xFFFF:
                raise ValueError('Value is {}'.format(val))
        except Exception as e:
            return str(e)

        self.value += val
        if self.value is not self.__prevvalue:
            self.update = self.value - self.__prevvalue
            self.__prevvalue = self.value
        pass

    def set_value(self, val: int):
        self.value = val
        self.__prevvalue = val


class DeviceOutputSimple(object):

    def __init__(self, link: int = 0, value: int = 0):
        self.link = link
        self.value = value
        GPIO.output_enable(link)
        if value == 1:
            GPIO.set_single_output(link)

    def set_level(self, level: int):
        return GPIO.write_output(self.link, level)




class DevicePt100(object):

    def __init__(self, idx: int, hwtype: str, stype: str, alpha: int):
        self.idx = idx
        self.hw_type = hwtype
        self.s_type = stype
        self.aplhavalue = alpha
        self.update = False
        GPIO.set_analog()


class DeviceThermocouple(object):

    def __init__(self, idx: int, HWType: str, Stype:str, alpha: int):
        self.idx = idx
        self.HWType = HWType
        self.Stype = Stype
        self.alphavalue = alpha
        self.update = False






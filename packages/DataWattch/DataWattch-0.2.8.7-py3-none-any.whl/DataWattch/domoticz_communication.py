# Release 0.2/
# Author D. Driessen
# Copyright (c) 2020  Ascos
# Python 3

from typing import List
import json
import urllib
import urllib.request
import re
from .Devices import *


class domoticz(object):
    # Settings for the domoticz server
    __domoticzserver = "localhost:8080"
    __domoticzusername = ""
    __domoticzpassword = ""

    def __init__(self):
        self.url = 'http://' + self.__domoticzserver + '/json.htm?'

    def _reset_url(self):
        self.url = 'http://' + self.__domoticzserver + '/json.htm?'

    def _append_url(self, string: str):
        self.url += string

    def request(self):
        request = urllib.request.urlopen(self.url)
        html_read = request.read()
        return html_read

    def command(self):
        command = urllib.request.urlopen(self.url)
        html_read = command.read()
        return html_read

    def add_log(self, message: str):
        message = urllib.parse.quote_plus(message)
        self._append_url("type=command&param=addlogmessage&message=" + message)
        check = json.loads(self.command())
        self._reset_url()
        print(check["status"])
        return check

    def request_hardware(self):
        self._append_url("type=hardware")
        parsed_data = json.loads(self.request())
        self._reset_url()
        print(parsed_data["status"])
        return parsed_data

    def request_devices(self):
        self._append_url("type=devices&used=true&displayhidden=1")
        parsed_data = json.loads(self.request())
        self._reset_url()
        print(parsed_data["status"])
        return parsed_data

    def request_uservars(self):
        self._append_url("type=command&param=getuservariables")
        parsed_data = json.loads(self.request())
        self._reset_url()
        print(parsed_data["status"])
        return parsed_data

    # will increment the counter value by 1
    def increment_single_counter(self, idx):
        if type(idx) == int:
            idx = str(idx)
        self._append_url("type=command&param=udevice&idx=" + idx + "&nvalue=0&svalue=1")
        check = json.loads(self.command())
        self._reset_url()
        print(check["status"])
        return check

    def set_counter(self, idx, value):
        if type(value) == int or type(value) == float:
            value = str(value)
        if type(idx) == int:
            idx = str(idx)
        self._append_url("type=command&param=udevice&idx=" + idx + "&svalue=" + value)
        check = json.loads(self.command())
        self._reset_url()
        print(check["status"])
        return check

    def get_settings(self):
        counter_buffer = []
        other_buffer = []
        devices = self.request_devices()
        index = 0
        # uservars = self.request_uservars()
        for dev in devices["result"]:
            # Filter out Hardwaretypes and subtypes
            p_type = dev["HardwareType"]
            s_type = dev["SubType"]
            name = dev["Name"]
            print(dev)
            # if a Incremental(pulse) counter has been found
            if s_type == 'Counter Incremental':
                # create new device class in list
                counter_buffer.append(DeviceCounter(dev["idx"], p_type, s_type, name, index, flank='falling'))
                index += 1
            else:
                other_buffer.append(Device(dev["idx"], p_type, s_type))
            # ADD OTHER s_type's LATER
        # Send every command to I2C bus
        if send_init(["input", "output", "interrupt", "pupd"]):
            self.add_log('Something went wrong at setting up the devices - Reboot advised&loglevel=4')
        return counter_buffer, other_buffer  # , other stypes

    def get_P1_init(self):
        Voltage_buffer = []
        Electric_buffer = []
        Gas_buffer = []
        devices = self.request_devices()
        for dev in devices["result"]:
            # Filter out Hardwaretypes and subtypes
            p_type = dev["HardwareType"]
            s_type = dev["SubType"]
            name = dev["Name"]
            print(dev)
            if s_type == 'Voltage':
                Voltage_buffer.append(DeviceVoltageP1(dev['idx'], name))
            if s_type == 'Electric':
                Electric_buffer.append(DeviceElectricP1(dev['idx'], name))
            if s_type == 'Gas':
                Gas_buffer.append(DeviceGasP1(dev['idx'], name))

        return Voltage_buffer, Electric_buffer, Gas_buffer #or others

    def get_data(self, idx:int):
        devices = self.request_devices()
        for dev in devices["result"]:
            # do something
            if idx == dev["idx"]:
                # should remove Unit from string
                data = re.findall(r'\d', dev["Data"])
                data = "".join(map(str, data))

        return data

    def init_counter_values(self, counterlist: List[DeviceCounter]):
        devices = self.request_devices()
        for dev in devices["result"]:
            # do something
            idx = dev["idx"]
            for x in counterlist:
                if x.idx == idx:
                    # should remove Unit from string
                    data = re.findall(r'\d', dev["Data"])
                    data = "".join(map(str, data))
                    x.set_value(int(data))
        pass

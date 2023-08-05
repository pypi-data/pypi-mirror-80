# Release 0.2/
# Author D. Driessen
# Copyright (c) 2020  Ascos
# Python 3

from smbus2 import SMBus, i2c_msg

bus = SMBus(1)

address = 0x48
# create buffer for  gpio pins with states and values
gpio = {
    "input0": {"value": '0', "pupd": 'no_pupd', "state": 'off', "interrupt": 'disabled'},
    "input1": {"value": '0', "pupd": 'no_pupd', "state": 'off', "interrupt": 'disabled'},
    "input2": {"value": '0', "pupd": 'no_pupd', "state": 'off', "interrupt": 'disabled'},
    "input3": {"value": '0', "pupd": 'no_pupd', "state": 'off', "interrupt": 'disabled'},

    "output0": {"value": '0', "pupd": 'no_pupd', "state": 'off'},
    "output1": {"value": '0', "pupd": 'no_pupd', "state": 'off'},
    "output2": {"value": '0', "pupd": 'no_pupd', "state": 'off'},
    "output3": {"value": '0', "pupd": 'no_pupd', "state": 'off'},

    "io0": {"value": '0', "pupd": 'no_pupd', "state": 'off', "function": 'input', "interrupt": 'disabled'},
    "io1": {"value": '0', "pupd": 'no_pupd', "state": 'off', "function": 'input', "interrupt": 'disabled'},
    "io2": {"value": '0', "pupd": 'no_pupd', "state": 'off', "function": 'input', "interrupt": 'disabled'},
    "io3": {"value": '0', "pupd": 'no_pupd', "state": 'off', "function": 'input', "interrupt": 'disabled'}
}

analog = {
    "AN1": {"value": 0, "state": "off", "function": "Thermocouple"},
    "AN2": {"value": 0, "state": "off", "function": "PT100"},
    "AN3": {"value": 0, "state": "off", "function": "0-10V"},
    "AN4": {"value": 0, "state": "off", "function": "0-10V"}
}


# enable gpio input
# pin is pin number from 0..4(+4I/O combined)
def input_enable(pin, send=0):
    # set correct pin to on-state in gpio dict
    try:
        # if pin >3 then I/O pins are set (I/0 are 4..8)
        if pin > 3:
            pin_name = str(pin - 4)
            gpio["io" + pin_name]["state"] = 'on'
            gpio["io" + pin_name]["function"] = 'input'
        else:
            pin_name = str(pin)
            gpio["input" + pin_name]["state"] = 'on'
        # if you want to send new input values immediately
        if send == 1:
            try:
                set_inputs()
            except Exception as e:
                return str(e)
        pass
    # wrong pin number set
    except KeyError:
        return str('Pin number incorrect. Pin: {}'.format(pin))


# enable gpio output
# pin is pin number from 0..4(+4I/o combined)
def output_enable(pin, send=0):
    # set correct pin to on-state in gpio dict
    try:
        # if pin >3 then I/O pins are set (I/O are 4..8)
        if pin > 3:
            pin_name = str(pin - 4)
            gpio["io" + pin_name]["state"] = 'on'
            gpio["io" + pin_name]["state"] = 'output'
            if gpio["io" + pin_name]["interrupt"] != 'disabled':
                gpio["io" + pin_name]["interrupt"] = 'disabled'
        else:
            pin_name = str(pin)
            gpio["output" + pin_name]["state"] = 'on'
        # if you want to send new output values immediately
        if send == 1:
            try:
                set_outputs()
            except Exception as e:
                return str(e)
        pass
    # wrong pin number
    except KeyError:
        return str('Pin number incorrect. Pin: {}'.format(pin))


# enable pin interrupt
# pin is pin number from 0..4(+4I/O combined)
# flank can be up/down flank (type: string 'rising'/'falling'/'both')
def interrupt_enable(pin, flank, send=0):
    # set correct pin to interrupt enabled, pin should be in 'on' state
    pin_name = 'none'
    try:
        if pin > 3:
            pin_name = str(pin - 4)
            # check if I/O is set to input
            # otherwise throw exception
            if gpio["io" + pin_name].get("function") != 'input':
                raise TypeError
            # enable interrupt
            gpio["io" + pin_name]["interrupt"] = flank
        else:
            pin_name = str(pin)
            gpio["input" + pin_name]["interrupt"] = flank
        # if you want to sent new interrupts immediately
        if send == 1:
            try:
                set_interrupts()
            except Exception as e:
                return str(e)
        pass
    # wrong pin number set
    except KeyError:
        return str('Pin number incorrect. Pin: {}'.format(pin))
    except TypeError:
        return str("I/O not defined as input. I/O: {}".format(pin_name))


# disable pin interrupt
# pin is pin number from 0..4(+4I/O combined)
def interrupt_disable(pin, send=0):
    # set correct pin to interrupt enabled, pin should be in 'on' state
    try:
        if pin > 3:
            pin_name = str(pin - 4)
            # check if I/O is set to input
            # otherwise throw exception
            if gpio["io" + pin_name].get("function") != 'input':
                raise TypeError
            # enable interrupt
            gpio["io" + pin_name]["interrupt"] = 'disabled'
        else:
            pin_name = str(pin)
            gpio["input" + pin_name]["interrupt"] = 'disabled'
        # if you want to sent new interrupts immediately
        if send == 1:
            try:
                set_interrupts()
            except Exception as e:
                return str(e)
        pass
    # wrong pin number set
    except KeyError:
        return str('Pin number incorrect. Pin: {}'.format(pin))
    except TypeError:
        return str("I/O not defined as input. I/O: {}".format(pin_name))


# set pin pull-up/pull-down
# io is string ("input","output" or "io")
# pupd is string "pull-up" or "pull-down"
def pupd_enable(pin: int, pupd: str, send: int = 0, io: str = 'input'):
    # set correct pin to pull-state in gpio dict
    try:
        gpio[str(io) + str(pin)]["pupd"] = pupd
        if send == 1:
            try:
                set_pupd()
            except Exception as e:
                return str(e)
        pass
    # wrong io number/name
    except KeyError:
        return str('IO {} {} Does not exist.'.format(io, pin))


def analog_enable(ch: int, function: str, send: int = 0):
    # enable correct analog channel
    try:
        analog['AN' + str(ch)]["state"] = 'on'
        analog['AN' + str(ch)]["function"] = function
        if send == 1:
            try:
                set_analog()
            except Exception as e:
                return str(e)
        pass
    except KeyError:
        return str("Analog input number {} does not exsist.".format(ch))


def write_output(pin: int, level: int, send: int = 1):
    val = str(level)
    # set correct pin value to '1'
    try:
        if pin > 3:
            pin_name = str(pin - 4)
            # check if I/O is set to output
            # otherwise throw exception
            if gpio["io" + pin_name].get("function") != 'output':
                raise TypeError
            # enable output
            gpio["io" + pin_name]["value"] = val
        else:
            pin_name = str(pin)
            gpio["output" + pin_name]["value"] = val

        if send == 1:
            buffer = 0
            for i in range(0, 4):
                if gpio["io" + str(i)].get("value") == '1':
                    buffer |= (0x01 << i << 4)
                if gpio["output" + str(i)].get("value") == '1':
                    buffer |= (0x01 << i)
            write = i2c_msg.write(0x48, [0x16, 0x00, buffer & 0xff])
            bus.i2c_rdwr(write)
    except TypeError:
        return str("I/O not defined as output. I/O: {}".format(pin_name))
    except KeyError:
        return str('Pin number incorrect. Pin: {}'.format(pin))
    except Exception as e:
        return str(e)
    pass


# send input command to I2C bus
def set_inputs():
    buffer = 0
    for i in range(0, 3):
        if gpio["input" + str(i)]["state"] == 'on':
            buffer |= (0x01 << i)
        else:
            buffer &= ~(0x01 << i)
        if gpio["io" + str(i)]["state"] == 'on' and gpio["io" + str(i)]["function"] == 'input':
            buffer |= (0x01 << i << 4)
        else:
            buffer &= ~(0x01 << i << 4)

    bus.write_byte_data(address, 0x10, buffer)
    pass


# send output command to I2C bus
def set_outputs():
    buffer = 0
    for i in range(0, 3):
        if gpio["output" + str(i)]["state"] == 'on':
            buffer |= (0x01 << i)
        else:
            buffer &= ~(0x01 << i)
        if gpio["io" + str(i)]["state"] == 'on' and gpio["io" + str(i)]["function"] == 'output':
            buffer |= (0x01 << i << 4)
        else:
            buffer &= ~(0x01 << i << 4)

    bus.write_byte_data(address, 0x11, buffer)
    pass


# send interrupt command to I2C bus
def set_interrupts():
    buffer = 0
    for i in range(0, 4):
        # fill buffer with correct input data
        if gpio["input" + str(i)].get("interrupt") == 'rising':
            buffer |= (0x01 << (i * 2))
        elif gpio["input" + str(i)].get("interrupt") == 'falling':
            buffer |= (0x02 << (i * 2))
        elif gpio["input" + str(i)].get("interrupt") == 'both':
            buffer |= (0x03 << (i * 2))

        # fill buffer with correct io data
        if gpio["io" + str(i)].get("interrupt") == 'rising':
            buffer |= (0x01 << (i * 2) << 4)
        elif gpio["io" + str(i)].get("interrupt") == 'falling':
            buffer |= (0x02 << (i * 2) << 4)
        elif gpio["io" + str(i)].get("interrupt") == 'both':
            buffer |= (0x03 << (i * 2) << 4)

    # send i2c data
    write = i2c_msg.write(address, [0x18, buffer & 0xff, buffer >> 8 & 0xff])
    bus.i2c_rdwr(write)
    pass


def set_pupd():
    buffer0 = 0
    buffer1 = 0
    for i in range(0, 4):
        # fill buffer with correct data
        if gpio["input" + str(i)].get("pupd") == 'pull-up':
            buffer0 |= (0x01 << (i * 2))
        elif gpio["input" + str(i)].get("pupd") == 'pull-down':
            buffer0 |= (0x02 << (i * 2))

        if gpio["io" + str(i)].get("function") == 'input':
            if gpio["io" + str(i)].get("pupd") == 'pull-up':
                buffer0 |= (0x01 << (i * 2) << 4)
            elif gpio["io" + str(i)].get("pupd") == 'pull-down':
                buffer0 |= (0x02 << (i * 2) << 4)

        if gpio["output" + str(i)].get("pupd") == 'pull-up':
            buffer1 |= (0x01 << (i * 2))
        elif gpio["output" + str(i)].get("pupd") == 'pull-down':
            buffer1 |= (0x02 << (i * 2))

        if gpio["io" + str(i)].get("function") == 'output':
            if gpio["io" + str(i)].get("pupd") == 'pull-up':
                buffer1 |= (0x01 << (i * 2) << 4)
            elif gpio["io" + str(i)].get("pupd") == 'pull-down':
                buffer1 |= (0x02 << (i * 2) << 4)

    write = i2c_msg.write(address, [0x12, buffer0 & 0xff, buffer0 >> 8 & 0xff, buffer1 & 0xff, buffer1 >> 8 & 0xff])
    bus.i2c_rdwr(write)
    pass


def set_analog():
    pass

# retrieve pulse counter value from certain pin
# this function does not check if pin is set as an pulse counter
# if pin is no pulse counter a 0 will always be returned
def get_single_pulse_counter(pin: int):
    write = i2c_msg.write(address, [(0x1A + 2 * pin)])
    read = i2c_msg.read(address, 2)
    bus.i2c_rdwr(write, read)
    return U8toU16(list(read))


# retrieve all pulse counter values
# this function does not check if pin is set as an pulse counter
# if pin is no pulse counter a 0 will always be returned
def get_pulse_counter():
    write = i2c_msg.write(address, [0x1A])
    read = i2c_msg.read(address, 16)
    bus.i2c_rdwr(write, read)
    return list(read)


def get_analog_value(ch: int):
    write = i2c_msg.write(address, [0x52 + 2 * ch])
    read = i2c_msg.read(address, 2)
    bus.i2c_rdwr(write, read)
    return U8toU16(list(read))

def get_input(pin):
    return bus.read_byte_data(address, 0x16)


def U8toU16(number: list) -> int:
    return number[0] | number[1] << 8

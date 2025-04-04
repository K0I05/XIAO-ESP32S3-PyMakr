# DFRobot SEN0540 LTR390 UV Sensor library
# by Toby Corkindale https://github.com/TJC/
# Released under the Apache 2.0 license.
#
# This library is for the DFRobot LTR390 UV Sensor.
# It is NOT compatible with regular LTR390 chips -- I don't know why it is
# different.
# Most notably, when writing to a register, it has to be sent with a +5 offset
# to the address. The data written must be two bytes, with the second byte
# being zero.

import time

import struct, uctypes

from micropython import const

from .ltr390_configuration import LTR390Configuration


class ControlRegister(uctypes.BIG_ENDIAN):
    _fields_ = [
        ("reserved1", uctypes.UINT8, 1),                # reserved - default is 0 (bit:0)   
        ("sensor_enabled", uctypes.UINT8, 1),           # ltr390uv light sensor (ALS/UVS) standby when false and active when true (bit:1)
        ("reserved2", uctypes.UINT8, 1),                # reserved - default is 0 (bit:2)
        ("operation_mode", uctypes.UINT8, 1),           # ltr390uv operation mode (ALS or UVS) (bit:3)
        ("software_reset_enabled", uctypes.UINT8, 1),   # ltr390uv software reset triggered when true (bit:4)
        ("reserved3", uctypes.UINT8, 3),                # reserved - default is 0 (bit:5-7)
    ]


#DEV_ADDRESS = const(0x1C)
DEV_ADDRESS = const(0x53)

# Input Register
REG_PID = const(0x00)  # Device PID
REG_VID = const(0x01)  # Device VID, fixed to 0x3343
REG_ADDR = const(0x02)  # Device address of module
REG_BAUDRATE = const(0x03)  # Serial baud rate
REG_STOPBIT = const(0x04)  # Serial check bit and stop bit
REG_VERSION = const(0x05)  # Firmware version
REG_PART_ID = const(0x06)  # Device ID of sensor

REG_ALS_DATA_LOW = const(0x0D)  # The low byte of ambient light intensity
REG_ALS_DATA_HIGH = const(0x0F)  # The high byte of ambient light intensity

REG_UVS_DATA_LOW = const(0x10)  # The low bit of UV intensity
REG_UVS_DATA_HIGH = const(0x12)  # The high bit of UV intensity

#REG_MAIN_CTRL = const(0x0E)  # Sensor mode select
REG_MAIN_CTRL = const(0x00)  # Sensor mode select
REG_MEASURE_RATE = const(0x04)  # Resolution and sampling time setting
REG_GAIN = const(0x05)  # Gain adjustment

REG_INT_CFG = const(0x07)  # Interrupt config

# The lower bit of upper threshold of UV or ambient light
REG_THRESH_UP_DATA_LOW = const(0x08)
REG_THRESH_UP_DATA_HIGH = const(0x09)

# The low bit of lower threshold of UV or ambient light
REG_THRESH_LOW_DATA_LOW = const(0x0A)
REG_THRESH_LOW_DATA_HIGH = const(0x0B)

# Threshold of UV or ambient light data change counts
REG_THRESH_VAR_DATA = const(0x0C)

eGain1 = const(0)  # Gain of 1
eGain3 = const(1)  # Gain of 3
eGain6 = const(2)  # Gain of 6
eGain9 = const(3)  # Gain of 9
eGain18 = const(4)  # Gain of 18

# Note when selecting resolution and time frames -- the higher the
# resolution, the longer the minimum latency.
e20bit = const(0)  # 20-bit data, min time 400ms
e19bit = const(16)  # 19-bit data, min time 200ms
e18bit = const(32)  # 18-bit data, min time 100ms
e17bit = const(48)  # 17-bit data, min time 50ms
e16bit = const(64)  # 16-bit data, min time 25ms

e25ms = const(0)  # Sampling time of 25ms
e50ms = const(1)  # Sampling time of 50ms
e100ms = const(2)  # Sampling time of 100ms
e200ms = const(3)  # Sampling time of 200ms
e500ms = const(4)  # Sampling time of 500ms
e1000ms = const(5)  # Sampling time of 1000ms
e2000ms = const(6)  # Sampling time of 2000ms


class LTR390:
    # Pass in an initialized I2C object, eg
    # i2c = I2C(0, scl=Pin(39), sda=Pin(40), freq=100_000)
    # ltr = LTR390(i2c)
    # ltr.set_uvs()
    # print(ltr.uvs())
    # If you have issues, try sleeping for 100ms first to let the system stabilize
    def __init__(self, address, i2c, configuration=LTR390Configuration()):
        self._address = address
        self._i2c = i2c
        self.configuration = configuration
        if self.configuration.mode == self.configuration.MEASUREMENT_MODE_ALS:
            self.enable_als_mode()
        else:
            self.enable_uvs_mode()
        self.set_measure_rate(self.configuration.resolution, self.configuration.rate)
        self.set_gain(self.configuration.gain)
        
    @property
    def configuration(self) -> LTR390Configuration:
        """Get configuration"""
        return self._configuration
    
    
    @configuration.setter
    def configuration(self, configuration: LTR390Configuration):
        """Set configuration
        """
        self._configuration = configuration
        self._gain = configuration.gain
        self._resolution = configuration.resolution
        self._rate = configuration.rate
        self._mode = configuration.mode


    def enable_als_mode(self):
        self._i2c.writeto(self._address, bytes([REG_MAIN_CTRL, 0x00]), False)

    def enable_uvs_mode(self):
        self._i2c.writeto(self._address, bytes([REG_MAIN_CTRL, 0x01]), False)
    
    def set_measure_rate(self, resolution, rate):
        self._i2c.writeto(self._address, bytes([REG_MEASURE_RATE, resolution + rate]), False)

    def set_gain(self, gain):
        self._i2c.writeto(self._address, bytes([REG_GAIN, gain]), False)

    @property
    def uvs(self) -> int:
        #buffer = self._i2c.readfrom_mem(self._address, REG_UVS_DATA_LOW, 4)
        #return (buffer[3] << 24) + (buffer[2] << 16) + (buffer[1] << 8) + buffer[0]
        #buffer = self._i2c.readfrom_mem(self._address, REG_UVS_DATA_LOW, 3)
        #buffer = bytearray(3)
        #self._i2c.writeto_then_readfrom(self._address, bytes([REG_UVS_DATA_LOW]), buffer)
        
        buffer = self._i2c.readfrom_mem(self._address, REG_UVS_DATA_LOW, 3)
        return (buffer[2] << 16) + (buffer[1] << 8) + buffer[0]

    @property
    def als(self) -> int:
        #buffer = self._i2c.readfrom_mem(self._address, REG_ALS_DATA_LOW, 4)
        #return (buffer[3] << 24) + (buffer[2] << 16) + (buffer[1] << 8) + buffer[0]
        #self._i2c.write(self._address)
        #self._i2c.writeto(self._address, bytes([REG_ALS_DATA_LOW]), False)
        #time.sleep(0.01)
        #buffer = self._i2c.readfrom(self._address, 3)
        buffer = self._i2c.readfrom_mem(self._address, REG_ALS_DATA_LOW, 3)
        return (buffer[2] << 16) + (buffer[1] << 8) + buffer[0]
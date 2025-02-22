"""Configuration File
This file is where you keep secret settings, passwords, and tokens! If you put them in the code 
you risk committing that info or sharing it you need to upload that file also on the Pico, even 
if you are just testing your scripts.
"""

# Copyright (c) 2024 Eric Gionet (gionet.c.eric@gmail.com)
# Released under the MIT License (MIT) - see LICENSE file

from bmp280 import BMP280Configuration # https://github.com/flrrth/pico-bmp280
from sht4x import SHT4XConfiguration 
from timezone import TimeOffset, DSTAdjust, DSTSchedule, TimezoneInfo




## Wifi ##
# Wifi Connection Settings
wifi_ssid       = "APOLLO"
wifi_pwd        = "42F43DA525D7"
wifi_hostname   = "rp2040-zero"
wifi_country    = "CA"

## NTP Time ##
# NTP Settings
ntp_host          = "ca.pool.ntp.org"
ntp_timeout_ms    = 5 * 1000
ntp_timezone_info = TimezoneInfo(TimeOffset(-4, 0), DSTSchedule(3, 9, 2, 0), DSTSchedule(11, 2, 2, 0), DSTAdjust(1, 0))


## I2C Bus 0 ##
# Initialize I2C bus 0 configuration settings
i2c0_bus_id  = 0            # I2C0 bus number
i2c0_freq_hz = 100000       # I2C0 clock frequency in hertz
i2c0_sda_io  = 5            # I2C0 SDA GPIO number
i2c0_scl_io  = 6            # I2C0 SCL GPIO number
i2c0_smp_ms  = 10 * 1000    # I2C0 sampling interval in milliseconds


## BME280 Sensor ##
# Initialize BME280 I2C configuration settings
bmp280_addr  = 0x77         # BMP280 I2C address

# Instantiate BMP280 configuration object & initialize parameters
bmp280_config = BMP280Configuration()
bmp280_config.power_mode               = BMP280Configuration.POWER_MODE_NORMAL
bmp280_config.pressure_oversampling    = BMP280Configuration.PRESSURE_OVERSAMPLING_4X
bmp280_config.temperature_oversampling = BMP280Configuration.TEMPERATURE_OVERSAMPLING_4X
bmp280_config.filter_coefficient       = BMP280Configuration.FILTER_COEFFICIENT_OFF
bmp280_config.standby_time             = BMP280Configuration.STANDBY_TIME_250_MS


## SHT4X Sensor ##
# Initialize SHT4X I2C configuration settings
sht4x_addr = 0x44   # SHT4X I2C address

# Instantiate SHT4X configuration object & initialize parameters
sht4x_config = SHT4XConfiguration()
sht4x_config.temperature_precision = SHT4XConfiguration.HIGH_PRECISION
sht4x_config.heater_power          = SHT4XConfiguration.HEATER_POWER_20MW
sht4x_config.heater_timespan       = SHT4XConfiguration.HEATER_TIMESPAN_1SEC




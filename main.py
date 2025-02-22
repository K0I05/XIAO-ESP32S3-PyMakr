"""Seeed Studio XIAO ESP32S3

On-chip 8M PSRAM & 8MB Flash

XIAO-ESP32S3_I2C_20250216
"""

# Copyright (c) 2024 Eric Gionet (gionet.c.eric@gmail.com)
# Released under the MIT License (MIT) - see LICENSE file

import asyncio, config

from machine import Pin, I2C
from scheduler import Scheduler
from bmp280 import BMP280I2C # https://github.com/flrrth/pico-bmp280
from sht4x import SHT4X # https://github.com/jposada202020/MicroPython_SHT4X
from net_if import connect_wifi, disconnect_wifi, synch_ntp_time, format_localtime


# Instantiate scheduler object
scheduler = Scheduler()

# Instantiate I2C bus object
i2c0_bus = I2C(config.i2c0_bus_id, sda=Pin(config.i2c0_sda_io), scl=Pin(config.i2c0_scl_io), freq=config.i2c0_freq_hz)

# Instantiate BMP280 I2C object
bmp280_i2c = BMP280I2C(config.bmp280_addr, i2c0_bus, config.bmp280_config)

# Instantiate SHT4X I2C object
sht4x_i2c = SHT4X(config.sht4x_addr, i2c0_bus, config.sht4x_config)



async def poll_i2c0_devices(txt) -> None:
    """Poll I2C0 Devices
    Polls I2C devices on bus 0.
    """
    try:
        # Read BMP280 measurements
        readout = bmp280_i2c.measurements

        # Read SHT4X measurements
        temperature, relative_humidity = sht4x_i2c.measurements
        
        # Print results
        print(f"{format_localtime()} Temperature: {temperature:.2f} C | Humidity: {relative_humidity:.2f} % | Pressure: {readout['p']:.2f} hPa.")
        
        await asyncio.sleep(0)
    except RuntimeError as error:
        print('Runtime Error: ', error.args[0])
    except OSError as e:
        print('OS Error: ', e.args[0])


async def main() -> None:
    """Main subroutine"""
    # Connect system to wifi network
    await connect_wifi()
    
    # Synchronize system clock with ntp time server
    await synch_ntp_time()
    
    # Disconnect system from wifi network
    await disconnect_wifi()

    # Create scheduled tasks
    asyncio.create_task(scheduler.create_schedule(poll_i2c0_devices, "", hrs=None, mins=range(0, 60, 1)))  # poll i2c device(s) every minute
    
    while True:
        try:
            await asyncio.sleep(1)
        except RuntimeError as error:
            print('Runtime Error: ', error.args[0])
            break
        except OSError as e:
            print('OS Error: ', e.args[0])
            break
        except KeyboardInterrupt:
            print('Keyboard Interrupt')
            break


"""Application entry point"""
if __name__ == '__main__':
    try:
        asyncio.run(main())
    finally:
        _ = asyncio.new_event_loop()


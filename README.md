# XIAO ESP32-S3 MicroPython + Visual Studio Code with PyMkr Extension
A `XIAO ESP32-S3` MicroPython example showcasing I2C sensor interfacing, WiFi connectivity, NTP and RTC time synchronization with time-zone support, and task scheduling.  The development environment leverages `Visual Studio Code` with `PyMakr` extension and the `Code Completion` extension for MicroPython is recommended.  The example's execution flow is as follows:
1. Connect system to WiFi network
2. Synchronize system RTC with NTP host
3. Disconnect system from WiFi network
4. Poll devices on I2C bus 0 once a minute

```
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
```
The example interfaces the `Bosch BMP280` and `Sensirion SHT4X` sensors over I2C.  Task scheduling is handled by `asyncio.create_task` and the `scheduler` module.  WiFi connectivity and NTP time synchronization is handled by the `net_if` module, and time-zone is handled by the `timezone` module.  The example's configuration is handled by the `config` module.



## Repository
This example is hosted on github and is located here:




Copyright (c) 2024 Eric Gionet (gionet.c.eric@gmail.com)
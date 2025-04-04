# XIAO ESP32-S3 MicroPython + Visual Studio Code with PyMkr Extension

[![K0I05](https://img.shields.io/badge/K0I05-a9a9a9?logo=data:image/svg%2bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxODgiIGhlaWdodD0iMTg3Ij48cGF0aCBmaWxsPSIjNDU0QjU0IiBkPSJNMTU1LjU1NSAyMS45M2MxOS4yNzMgMTUuOTggMjkuNDcyIDM5LjM0NSAzMi4xNjggNjMuNzg5IDEuOTM3IDIyLjkxOC00LjU1MyA0Ni42Ni0xOC44NDggNjQuNzgxQTUwOS40NzggNTA5LjQ3OCAwIDAgMSAxNjUgMTU1bC0xLjQ4NCAxLjg4M2MtMTMuMTk2IDE2LjUzMS0zNS41NTUgMjcuMjE1LTU2LjMzOSAyOS45MDItMjguMzEyIDIuOC01Mi4yNTUtNC43MzctNzQuNzMyLTIxLjcxNUMxMy4xNzIgMTQ5LjA5IDIuOTczIDEyNS43MjUuMjc3IDEwMS4yODEtMS42NiA3OC4zNjMgNC44MyA1NC42MjEgMTkuMTI1IDM2LjVBNTA5LjQ3OCA1MDkuNDc4IDAgMCAxIDIzIDMybDEuNDg0LTEuODgzQzM3LjY4IDEzLjU4NiA2MC4wNCAyLjkwMiA4MC44MjMuMjE1YzI4LjMxMi0yLjggNTIuMjU1IDQuNzM3IDc0LjczMiAyMS43MTVaIi8+PHBhdGggZmlsbD0iI0ZERkRGRCIgZD0iTTExOS44NjcgNDUuMjdDMTI4LjkzMiA1Mi4yNiAxMzMuODIgNjMgMTM2IDc0Yy42MyA0Ljk3Mi44NDIgOS45NTMuOTUzIDE0Ljk2LjA0NCAxLjkxMS4xMjIgMy44MjIuMjAzIDUuNzMxLjM0IDEyLjIxLjM0IDEyLjIxLTMuMTU2IDE3LjMwOWE5NS42MDQgOTUuNjA0IDAgMCAxLTQuMTg4IDMuNjI1Yy00LjUgMy43MTctNi45NzQgNy42ODgtOS43MTcgMTIuODAzQzEwNi45NCAxNTIuNzkyIDEwNi45NCAxNTIuNzkyIDk3IDE1N2MtMy40MjMuNTkyLTUuODAxLjY4NS04Ljg3OS0xLjA3NC05LjgyNi03Ljg4LTE2LjAzNi0xOS41OS0yMS44NTgtMzAuNTEyLTIuNTM0LTQuNTc1LTUuMDA2LTcuMjEtOS40NjYtMTAuMDItMy43MTQtMi44ODItNS40NS02Ljk4Ni02Ljc5Ny0xMS4zOTQtLjU1LTQuODg5LS41NjEtOS4zMTYgMS0xNCAuMDkzLTEuNzYzLjE4Mi0zLjUyNy4yMzktNS4yOTIuNDkxLTEzLjg4NCAzLjg2Ni0yNy4wNTcgMTQuMTU2LTM3LjAyOCAxNy4yMTgtMTQuMzM2IDM1Ljg1OC0xNS4wNjYgNTQuNDcyLTIuNDFaIi8+PHBhdGggZmlsbD0iI0M2RDVFMCIgZD0iTTEwOSAzOWMxMS43MDMgNS4yNTUgMTkuMjA2IDEzLjE4NiAyNC4yOTMgMjUuMDA0IDIuODU3IDguMjQgMy40NyAxNi4zMTYgMy42NiAyNC45NTYuMDQ0IDEuOTExLjEyMiAzLjgyMi4yMDMgNS43MzEuMzQgMTIuMjEuMzQgMTIuMjEtMy4xNTYgMTcuMzA5YTk1LjYwNCA5NS42MDQgMCAwIDEtNC4xODggMy42MjVjLTQuNSAzLjcxNy02Ljk3NCA3LjY4OC05LjcxNyAxMi44MDNDMTA2LjgwNCAxNTMuMDQxIDEwNi44MDQgMTUzLjA0MSA5NyAxNTdjLTIuMzMyLjA3OC00LjY2OC4wOS03IDBsMi4xMjUtMS44NzVjNS40My01LjQ0NSA4Ljc0NC0xMi41NzcgMTEuNzU0LTE5LjU1OWEzNDkuNzc1IDM0OS43NzUgMCAwIDEgNC40OTYtOS44NzlsMS42NDgtMy41NWMyLjI0LTMuNTU1IDQuNDEtNC45OTYgNy45NzctNy4xMzcgMi4zMjMtMi42MSAyLjMyMy0yLjYxIDQtNWwtMyAxYy0yLjY4LjE0OC01LjMxOS4yMy04IC4yNWwtMi4xOTUuMDYzYy01LjI4Ny4wMzktNS4yODcuMDM5LTcuNzc4LTEuNjUzLTEuNjY2LTIuNjkyLTEuNDUzLTQuNTYtMS4wMjctNy42NiAyLjM5NS00LjM2MiA0LjkyNC04LjA0IDkuODI4LTkuNTcgMi4zNjQtLjQ2OCA0LjUxNC0uNTI4IDYuOTIyLS40OTNsMi40MjIuMDI4TDEyMSA5MmwtMS0yYTkyLjc1OCA5Mi43NTggMCAwIDEtLjM2LTQuNTg2QzExOC42IDY5LjYzMiAxMTYuNTE3IDU2LjA5NCAxMDQgNDVjLTUuOTA0LTQuNjY0LTExLjYtNi4wODgtMTktNyA3LjU5NC00LjI2NCAxNi4yMjMtMS44MSAyNCAxWiIvPjxwYXRoIGZpbGw9IiM0OTUwNTgiIGQ9Ik03NyA5MmM0LjYxMyAxLjY3MSA3LjI2IDMuOTQ1IDEwLjA2MyA3LjkzOCAxLjA3OCAzLjUyMy45NzYgNS41NDYtLjA2MyA5LjA2Mi0yLjk4NCAyLjk4NC02LjI1NiAyLjM2OC0xMC4yNSAyLjM3NWwtMi4yNzcuMDc0Yy01LjI5OC4wMjgtOC4yNTQtLjk4My0xMi40NzMtNC40NDktMi44MjYtMy41OTctMi40MTYtNy42MzQtMi0xMiA0LjUwMi00LjcyOCAxMC45OS0zLjc2IDE3LTNaIi8+PHBhdGggZmlsbD0iIzQ4NEY1NyIgZD0ibTExOCA5MS43NSAzLjEyNS0uMDc4YzMuMjU0LjM3MSA0LjU5NyAxLjAwMiA2Ljg3NSAzLjMyOC42MzkgNC4yMzEuMjkgNi40NDItMS42ODggMTAuMjUtMy40MjggNC4wNzgtNS44MjcgNS41OTgtMTEuMTk1IDYuMTQ4LTEuNDE0LjAwOC0yLjgyOCAwLTQuMjQyLS4wMjNsLTIuMTY4LjAzNWMtMi45OTgtLjAxNy01LjE1Ny0uMDMzLTcuNjcyLTEuNzU4LTEuNjgxLTIuNjg0LTEuNDYtNC41NTItMS4wMzUtNy42NTIgMi4zNzUtNC4zMjUgNC44OTQtOC4wMDkgOS43NS05LjU1OSAyLjc3Ny0uNTQ0IDUuNDItLjY0OSA4LjI1LS42OTFaIi8+PHBhdGggZmlsbD0iIzUyNTg2MCIgZD0iTTg2IDEzNGgxNmwxIDRjLTIgMi0yIDItNS4xODggMi4yNjZMOTQgMTQwLjI1bC0zLjgxMy4wMTZDODcgMTQwIDg3IDE0MCA4NSAxMzhsMS00WiIvPjwvc3ZnPg==)](https://github.com/K0I05)
[![License: MIT](https://cdn.prod.website-files.com/5e0f1144930a8bc8aace526c/65dd9eb5aaca434fac4f1c34_License-MIT-blue.svg)](/LICENSE)
[![MicroPython](https://img.shields.io/badge/MicroPython-orange?logo=micropython&logoColor=0a0a0a)](https://micropython.org/)
[![Edited with VS Code](https://badgen.net/badge/icon/VS%20Code?icon=visualstudio&label=edited%20with)](https://code.visualstudio.com/)
[![PyMakr](https://img.shields.io/badge/build_with-PyMakr-red.svg)](https://docs.pycom.io/)

A `XIAO ESP32-S3` MicroPython example showcasing I2C sensor interfacing, WiFi connectivity, NTP and RTC time synchronization with time-zone support, and task scheduling.  The development environment leverages `Visual Studio Code` with `PyMakr` extension and the `Code Completion` extension for MicroPython is recommended.  The example's execution flow is as follows:

1. Connects system to WiFi network
2. Synchronizes system RTC with NTP host
3. Disconnects system from WiFi network
4. Poll's devices on I2C bus 0 once a minute

```c
async def main() -> None:
    """Main subroutine"""
    # Connect system to wifi network
    await connect_wifi()
    
    # Synchronize system clock with ntp time server
    await synch_ntp_time()
    
    # Disconnect system from wifi network
    await disconnect_wifi()

    # Create scheduled tasks
    asyncio.create_task(scheduler.create_schedule(poll_i2c0_devices_task, "tsk1", hrs=None, mins=range(0, 60, 1)))  # poll i2c device(s) every minute
    
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

The example interfaces the `Bosch BMP280` and `Sensirion SHT4X` sensors over I2C.  The I2C drivers for the `Bosch BMP280` and `Sensirion SHT4X` sensors are random drivers that found online and seem to work fine for the purposes of this example.  Task scheduling is handled by `asyncio.create_task` function and the `scheduler` module.  WiFi connectivity and NTP time synchronization are handled by the `net_if` module, and time-zone is handled by the `timezone` module.  The example's configuration is handled by the `config` module.

The master branch of the code base for the `schedule` module is located here: <https://github.com/peterhinch/micropython-async/tree/197c2b5d72cc7633e4b3176eabdeef532ea09ffd/v3/as_drivers/sched>.  The readme files are amazing and the `schedule` readme is available here: <https://github.com/peterhinch/micropython-async/blob/197c2b5d72cc7633e4b3176eabdeef532ea09ffd/v3/docs/SCHEDULE.md>.

## Time-Zone Support

The `timezone` module is a lightweight implementation to support time-zone functionality in MicroPython.  The system synchronizes its `RTC` with an NTP host once the system connects to a WiFi network and sets the system time to UTC by default.  The time can be converted to local-time by specifying a time-zone information object as an argument for the `localtime` function.

```c
# Instantiate timezone information object for Atlantic Canada with daylight saving start and end schedules.
tz_info = TimezoneInfo(TimeOffset(-4, 0), DSTSchedule(3, 9, 2, 0), DSTSchedule(11, 2, 2, 0), DSTAdjust(1, 0))

# Get local-time parts from system clock
(year, month, day, hrs, mins, secs, wday, yday) = timezone.localtime(tz_info)
```

## Time-Into-Interval Scheduler

The `time_into_interval` module is a lightweight implementation to support time-into-interval scheduling in MicroPython.  The time-into-interval module synchronizes a MicroPython task with the system clock with user-defined time interval for temporal conditional scenarios.  The shortest interval supported is 1-second and the longest interval supported is 28-days.

```c
import asyncio

from scheduler import TimeIntoInterval, TimeIntoIntervalTypes

async def do_work_task(task_id: str) -> None:
    """Do Work Task.

    A task to simulate work.

    Args:
        task_id (str): Task unique identifier.
    """
    # Instantiate time-into-interval objects
    tii_1_0min = TimeIntoInterval(TimeIntoIntervalTypes.TIME_INTO_INTERVAL_MIN, 1, 0) # 1-minute interval with no offset
    tii_5_0min = TimeIntoInterval(TimeIntoIntervalTypes.TIME_INTO_INTERVAL_MIN, 5, 0) # 5-minute interval with no offset
    tii_5_1min = TimeIntoInterval(TimeIntoIntervalTypes.TIME_INTO_INTERVAL_MIN, 5, 1) # 5-minute interval with 1-minute offset
    
    # Loop forever
    while True:
        try:
            # interval will elapse every 5-minutes (12:00:00, 12:05:00, 12:10:00, etc)
            if tii_5_0min.interval_elapsed():
                print(f"{task_id}: tii_5_0min.interval_elapsed: {format_localtime()}")
                
            # interval will elapse every 5-minutes with a 1-minute offset (12:01:00, 12:06:00, 12:11:00, etc) 
            if tii_5_1min.interval_elapsed():
                print(f"{task_id}: tii_5_1min.interval_elapsed: {format_localtime()}")
            
            # interval will sleep for 1-minute (12:00:00, 12:01:00, 12:02:00, etc)
            print(f"{task_id}: tii_1_0min.interval_sleep: {format_localtime()}")
            await tii_1_0min.interval_sleep()
        except RuntimeError as error:
            print(f'{task_id}: Runtime Error: ', error.args[0])
            break
        except OSError as e:
            print(f'{task_id}: OS Error: ', e.args[0])
            break
        except KeyboardInterrupt:
            print(f'{task_id}: Keyboard Interrupt')
            break


async def main() -> None:
    # Create scheduled tasks
    asyncio.create_task(do_work_task("tsk0"))
    
    # Loop forever
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
```

The above snippet example prints the following information over the serial port.

```c
tsk0: tii_1_0min.interval_sleep: 2025-02-22 10:37
tsk0: tii_1_0min.interval_sleep: 2025-02-22 10:38
tsk0: tii_1_0min.interval_sleep: 2025-02-22 10:39
tsk0: tii_5_0min.interval_elapsed: 2025-02-22 10:40
tsk0: tii_1_0min.interval_sleep: 2025-02-22 10:40
tsk0: tii_5_1min.interval_elapsed: 2025-02-22 10:41
tsk0: tii_1_0min.interval_sleep: 2025-02-22 10:41
tsk0: tii_1_0min.interval_sleep: 2025-02-22 10:42
tsk0: tii_1_0min.interval_sleep: 2025-02-22 10:43
tsk0: tii_1_0min.interval_sleep: 2025-02-22 10:44
tsk0: tii_5_0min.interval_elapsed: 2025-02-22 10:45
tsk0: tii_1_0min.interval_sleep: 2025-02-22 10:45
tsk0: tii_5_1min.interval_elapsed: 2025-02-22 10:46
tsk0: tii_1_0min.interval_sleep: 2025-02-22 10:46
tsk0: tii_1_0min.interval_sleep: 2025-02-22 10:47
tsk0: tii_1_0min.interval_sleep: 2025-02-22 10:48
tsk0: tii_1_0min.interval_sleep: 2025-02-22 10:49
tsk0: tii_5_0min.interval_elapsed: 2025-02-22 10:50
tsk0: tii_1_0min.interval_sleep: 2025-02-22 10:50
```

## Repository

This example is hosted on github and is located here: <https://github.com/K0I05/XIAO-ESP32S3-PyMakr>

Copyright (c) 2024 Eric Gionet (<gionet.c.eric@gmail.com>)

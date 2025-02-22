# XIAO ESP32-S3 MicroPython + Visual Studio Code with PyMkr Extension
A `XIAO ESP32-S3` MicroPython example showcasing I2C sensor interfacing, WiFi connectivity, NTP and RTC time synchronization with time-zone support, and task scheduling.  The development environment leverages `Visual Studio Code` with `PyMakr` extension and the `Code Completion` extension for MicroPython is recommended.  The example's execution flow is as follows:
1. Connects system to WiFi network
2. Synchronizes system RTC with NTP host
3. Disconnects system from WiFi network
4. Poll's devices on I2C bus 0 once a minute

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

The master branch of the code base for the `schedule` module is located here: https://github.com/peterhinch/micropython-async/tree/197c2b5d72cc7633e4b3176eabdeef532ea09ffd/v3/as_drivers/sched.  The readme files are amazing and the `schedule` readme is available here: https://github.com/peterhinch/micropython-async/blob/197c2b5d72cc7633e4b3176eabdeef532ea09ffd/v3/docs/SCHEDULE.md.

## Time-Zone Support
The `timezone` module is a lightweight implementation to support time-zone functionality in MicroPython.  The system synchronizes its `RTC` with an NTP host once the system connects to a WiFi network and sets the system time to UTC by default.  The time can be converted to local-time by specifying a time-zone information object as an argument for the `localtime` function.
```
# Instantiate timezone information object for Atlantic Canada with daylight saving start and end schedules.
tz_info = TimezoneInfo(TimeOffset(-4, 0), DSTSchedule(3, 9, 2, 0), DSTSchedule(11, 2, 2, 0), DSTAdjust(1, 0))

# Get local-time parts from system clock
(year, month, day, hrs, mins, secs, wday, yday) = timezone.localtime(tz_info)
```

## Time-Into-Interval Scheduler
The `time_into_interval` module is a lightweight implementation to support time-into-interval scheduling in MicroPython.  The time-into-interval module synchronizes a MicroPython task with the system clock with user-defined time interval for temporal conditional scenarios.  The shortest interval supported is 1-second and the longest interval supported is 28-days.
```
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
```
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
This example is hosted on github and is located here: https://github.com/K0I05/XIAO-ESP32S3-PyMakr




Copyright (c) 2024 Eric Gionet (gionet.c.eric@gmail.com)
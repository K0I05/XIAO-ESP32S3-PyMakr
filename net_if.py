"""Network Interface Module
Connecting Wifi, disconnecting Wifi and Wifi status
Synchronizing system time with NTP server
"""
# Copyright (c) 2024 Eric Gionet (gionet.c.eric@gmail.com)
# Released under the MIT License (MIT) - see LICENSE file

import asyncio, config, network, ntptime, timezone
from machine import reset, RTC


# Instantiate RTC object
rtc = RTC()

# Instantiate WLAN station interface object
wlan = network.WLAN(network.STA_IF)



def format_localtime() -> str:
    """
    # format_locatime
    
    Gets formatted local-time as a string (yyyy-mm-dd HH:MM).
    
    """
    # Get date-time parts from internal RTC
    (year, month, day, hrs, mins, secs, wday, yday) = timezone.localtime(config.ntp_timezone_info)
    
    # Format the current date-time as a string "yyyy-mm-dd HH:MM"
    return "{:02d}-{:02d}-{} {:02d}:{:02d}".format(year, month, day, hrs, mins)


def format_utctime() -> str:
    """
    # format_utctime
    
    Gets formatted utc-time as a string (yyyy-mm-dd HH:MM).
    
    """
    # Get utc date-time parts
    (year, month, day, hrs, mins, secs, wday, yday) = timezone.gmtime()
    
    # Format the current utc date-time as a string "yyyy-mm-dd HH:MM"
    return "{:02d}-{:02d}-{} {:02d}:{:02d}".format(year, month, day, hrs, mins)
    
    
async def synch_ntp_time() -> None:
    """
    # synch_ntp_time
    
    Synchronizes system time with NTP time server and initializes RTC to UTC time.
    
    """
    # validate network connectivity
    if not wlan.isconnected():
        raise RuntimeError('no wifi connection')
        reset()
    
    # Set configured NTP host and timeout
    ntptime.host    = config.ntp_host
    ntptime.timeout = config.ntp_timeout_ms
    
    # Get UTC time from NTP host (this function will set the system RTC to UTC)
    ntptime.settime()
    
    # Print local and utc timestamps
    print(f"System local date-time: {format_localtime()}  |  System UTC date-time: {format_utctime()}")
    
    await asyncio.sleep(0)


async def connect_wifi() -> None:
    """
    # connect_wifi
    
    Connects system to wifi network.
    
    """
    # Activate wifi
    wlan.active(True)
    
    # Set network credentials
    wlan.connect(config.wifi_ssid, config.wifi_pwd)
    
    # Wait for connect or fail
    print('waiting for wifi connection ...')
    max_wait = 30
    while max_wait > 0:
        if wlan.isconnected() == True:
            break
        print('connecting...')
        max_wait -= 1
        await asyncio.sleep(0.5)

    # Handle connection error
    if not wlan.isconnected():
        raise RuntimeError('wifi connection failed')
        reset()
    else:
        print('wifi connected: ' + wifi_status())
        status = wlan.ifconfig()
        print('ip = ' + status[0])
        
    await asyncio.sleep(0)


async def disconnect_wifi() -> None:
    """
    # disconnect_wifi
    
    Disconnects system from wifi network.
    """
    # Disconnect from wifi network
    if wlan.isconnected():
        wlan.disconnect()
    
    # deactivate wifi interface
    if wlan.active():
        wlan.active(False)
        
    # validate wifi connection status
    if not wlan.isconnected():
        network.STAT_GOT_IP
        print('wifi disconnected: ' + wifi_status())
        
    await asyncio.sleep(0)


def wifi_status() -> str:
    """
    # wifi_status
    
    Gets wifi network status.
    
    """
    if wlan.status() == network.STAT_IDLE:
        return "idle"
    elif wlan.status() == network.STAT_CONNECTING:
        return "connecting"
    elif wlan.status() == network.STAT_WRONG_PASSWORD:
        return "wrong password"
    elif wlan.status() == network.STAT_NO_AP_FOUND:
        return "no ap found"
    elif wlan.status() == network.STAT_GOT_IP:
        return "got ip"
    else:
        return "unknown"


def is_wifi_connected() -> bool:
    """
    # is_wifi_connected
    
    Checks if the system is connected to a wifi network.
    
    """
    return wlan.isconnected()
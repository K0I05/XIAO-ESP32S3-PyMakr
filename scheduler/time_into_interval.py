# Copyright (c) 2024 Eric Gionet (gionet.c.eric@gmail.com)
# Released under the MIT License (MIT) - see LICENSE file

import asyncio, time

from micropython import const





class TimeIntoIntervalTypes:
    """TimeIntoIntervalTypes enum"""
    TIME_INTO_INTERVAL_SEC = const(0)
    """Time into interval precision type is seconds."""
    TIME_INTO_INTERVAL_MIN = const(1)
    """Time into interval precision type is minutes."""
    TIME_INTO_INTERVAL_HR  = const(2)
    """Time into interval precision type is hours."""
    



class TimeIntoInterval:
    MAXT_MSEC = const(100)
    """uasyncio can't handle long delays so split into 100msec segments"""
    
    def __init__(self, interval_type: TimeIntoIntervalTypes, interval_period: int, interval_offset: int) -> None:
        """
        # TimeIntoInterval
        
        Constructor to initialize time-zone interval class parameters.
        
        A time-into-interval is used within a MicroPython task subroutine for conditional or task delay 
        based on the configured interval type, period, and offset that is synchronized to the system clock.

        As an example, if a 5-second interval is configured, the `interval_elapsed` function will return 
        true every 5-seconds based on the system clock i.e. 12:00:00, 12:00:05, 12:00:10, etc.  The `interval_sleep` 
        puts a task to sleep for 5-seconds and behaves like a task scheduler that is synchronized to the system clock.
        
        The interval offset is used to offset the start of the interval period. As an example, if a 5-minute 
        interval with 1-minute offset is configured, the `interval_elapsed` function will return true every 
        5-minutes at 1-minute into the interval based on the system clock i.e. 12:01:00, 12:06:00, 12:11:00, etc.
 
        Args:
            interval_type (TimeIntoIntervalTypes): Interval precision type (seconds, minutes, hours).
            interval_period (int): Interval period for interval precision type (seconds, minutes, or hours).
            interval_offset (int): Interval offset for interval precision type (seconds, minutes, or hours).
            
        """
        self._interval_type        = interval_type
        self._interval_period      = interval_period
        self._interval_offset      = interval_offset
        self._next_epoch_time_msec = self.epoch_time_next_event_msec(interval_type, interval_period, interval_offset)
    
    
    async def _long_sleep_msec(self, t) -> None:  # Sleep with no bounds. Immediate return if t < 0.
        while t > 0:
            await asyncio.sleep_ms(min(t, TimeIntoInterval.MAXT_MSEC))
            t -= TimeIntoInterval.MAXT_MSEC
        
    
    def normalize_interval_to_msec(self, interval_type: TimeIntoIntervalTypes, interval_period: int) -> int:
        """
        # normalize_interval_to_msec
        
        Calculates normalized interval in milli-seconds from interval type and period.

        Args:
            interval_type (TimeIntoIntervalTypes): Interval precision type (seconds, minutes, hours).
            interval_period (int): Interval period per interval precision type (seconds, minutes, or hours).

        Returns:
            int: Interval in milli-seconds.
            
        """
        interval_msec = 0
        if(interval_type == TimeIntoIntervalTypes.TIME_INTO_INTERVAL_SEC):
            interval_msec = interval_period * 1000
        elif(interval_type == TimeIntoIntervalTypes.TIME_INTO_INTERVAL_MIN):
            interval_msec = interval_period * 60 * 1000
        elif(interval_type == TimeIntoIntervalTypes.TIME_INTO_INTERVAL_HR):
            interval_msec = interval_period * 60 * 60 * 1000
        return interval_msec
    
    
    def epoch_time_next_event_msec(self, interval_type: TimeIntoIntervalTypes, interval_period: int, interval_offset: int, epoch_time_last_event_msec: int = 0) -> int:
        """
        # epoch_time_next_event_msec
        
        Calculates epoch time of the next event in milli-seconds from system clock based on the time interval type, period, and offset, and epoch 
        time of the last event in milli-seconds.
        
        The interval should be divisible by 60 i.e. no remainder if the interval type and period is every 10-seconds with no offset, the event 
        will trigger on-time with the system clock i.e. 09:00:00, 09:00:10, 09:00:20, etc.
        
        The interval offset is used to offset the start of the interval period.  If the interval type and period is every 5-minutes 
        with a 1-minute offset, the event will trigger on-time with the system clock i.e. 09:01:00, 09:06:00, 09:11:00, etc.

        Args:
            interval_type (TimeIntoIntervalTypes): Interval precision type (seconds, minutes, hours).
            interval_period (int): Interval period for interval precision type (seconds, minutes, or hours).
            interval_offset (int): Interval offset for interval precision type (seconds, minutes, or hours).
            epoch_time_last_event_msec (int, optional): Epoch time of the last event in milli-seconds. Defaults to 0.


        Returns:
            int: Epoch time of the next event in milli-seconds.
            
        """
        # Validate interval period argument
        if not interval_period > 0:
            raise ValueError("Interval period cannot be 0, time-into-interval epoch time event failed")
        
        # Normalize interval period and offset to milli-seconds
        interval_period_msec = self.normalize_interval_to_msec(interval_type, interval_period)
        interval_offset_msec = self.normalize_interval_to_msec(interval_type, interval_offset)
        
        # Validate interval period argument on total days
        if interval_period_msec >= (28 * 24 * 60 * 60 * 1000):
            raise ValueError("Interval period cannot be greater than 28-days, time-into-interval epoch time event failed")
        
        # Validate period and offset intervals
        if (interval_period_msec - interval_offset_msec) < 0:
            raise ValueError("Interval period must be larger than the interval offset, time-into-interval epoch time event failed")

        # Get now system unix epoch time parts
        (now_year, now_month, now_day, now_h, now_m, now_s, now_dow, now_doy) = time.gmtime()
        
        # Define next system unix epoch time parts
        next_year  = 0
        next_month = 0
        next_day   = 0
        next_h     = 0
        next_m     = 0
        next_s     = 0
        next_dow   = 0
        next_doy   = 0
        
        # Initialize next time-parts localtime based on interval-type
        if interval_type == TimeIntoIntervalTypes.TIME_INTO_INTERVAL_SEC:
            next_year  = now_year
            next_month = now_month
            next_day   = now_day
            next_h     = now_h
            next_m     = now_m
            next_s     = 0
        elif interval_type == TimeIntoIntervalTypes.TIME_INTO_INTERVAL_MIN:
            next_year  = now_year
            next_month = now_month
            next_day   = now_day
            next_h     = now_h
            next_m     = 0
            next_s     = 0
        elif interval_type == TimeIntoIntervalTypes.TIME_INTO_INTERVAL_HR:
            next_year  = now_year
            next_month = now_month
            next_day  = now_day
            next_h    = 0
            next_m    = 0
            next_s    = 0
        
        # Handle interval period by time-parts time-span exceedance
        if interval_period_msec > 60 * 1000:
            # Over 60-seconds, set minute time-part to 0
            next_m = 0
            next_s = 0
        elif interval_period_msec > 60 * 60 * 1000:
            # Over 60-minutes, set hour time-part to 0
            next_h = 0
            next_m = 0
            next_s = 0
        elif interval_period_msec > 24 * 60 * 60 * 1000:
            # Over 24-hours, set day time-part to 0
            next_day = 0
            next_h   = 0
            next_m   = 0
            next_s   = 0
        
        # Initialize next epoch time event.
        epoch_time_next_event_msec = 0
        
        # Validate if the last task event was computed.
        if epoch_time_last_event_msec > 0:
            # Add task interval to last task event epoch to 
            # compute next task event epoch.
            epoch_time_next_event_msec = epoch_time_last_event_msec + interval_period_msec
            
            # Compute the delta between now and next unix times.
            delta_time_msec = epoch_time_next_event_msec - self.epoch_time_msec
            
            # Ensure next task event is ahead in time, otherwise,
            # recompute the next task event time.
            if delta_time_msec < 0:
                # Next task event is not ahead in time, set next 
                # task event to 0, and regenerate next time event.
                epoch_time_next_event_msec = 0
        
        # Validate if the next task event was computed.    
        if epoch_time_next_event_msec == 0:
            # Convert next time parts to unix epoch time in milli-seconds
            epoch_time_next_event_msec = int(round(time.mktime((next_year, next_month, next_day, next_h, next_m, next_s, next_dow, next_doy)) * 1000))
            
            # Initialize next unix time by adding the task event interval period and offset
            epoch_time_next_event_msec = epoch_time_next_event_msec + interval_period_msec + interval_offset_msec
            
            # Compute the delta between now and next unix times
            delta_time_msec = epoch_time_next_event_msec - self.epoch_time_msec
            
            # Ensure next task event is ahead in time
            if delta_time_msec <= 0:
                # Next task event is not ahead in time
                while delta_time_msec < 0:
                    # Keep adding task event intervals until next task event is ahead in time
                    epoch_time_next_event_msec = epoch_time_next_event_msec + interval_period_msec
                    
                    # Compute the delta between now and next unix times
                    delta_time_msec = epoch_time_next_event_msec - self.epoch_time_msec
        
        # Return next task event epoch time
        return epoch_time_next_event_msec
    
    
    def epoch_time_last_event_msec(self, interval_type: TimeIntoIntervalTypes, interval_period: int, next_epoch_time_msec: int) -> int:
        """
        # epoch_time_last_event_msec
        
        Calculates epoch time of the last event in milli-seconds from interval type and period, and the next epoch time in milli-seconds.

        Args:
            interval_type (TimeIntoIntervalTypes): Interval precision type (seconds, minutes, hours).
            interval_period (int): Interval period for interval precision type (seconds, minutes, or hours).
            next_epoch_time_msec (int): Next epoch time in milli-seconds.

        Returns:
            int: Epoch time of the last event in milli-seconds.
            
        """
        # Convert interval into msec
        interval_msec = self.normalize_interval_to_msec(interval_type, interval_period)
        
        # Set last event epoch timestamp
        return next_epoch_time_msec - interval_msec
    
    
    def interval_elapsed(self) -> bool:
        """
        # interval_elapsed
        
        Validates interval-elapsed condition based on the configured interval type, period, 
        and offset arguments that is synchronized to the system clock and returns true when 
        the interval has elapsed.

        Returns:
            bool: Interval has elapsed when true, otherwise, false
            
        """
        state = False
        
        # Compute time delta until next time into interval condition
        delta_msec = self._next_epoch_time_msec - self.epoch_time_msec
        
        # Validate time delta, when delta is <= 0, time has elapsed
        if delta_msec <= 0:
            # Set time-into-interval state to true - intervale has lapsed
            state = True
            
            # Set next event timestamp (UTC)
            self._next_epoch_time_msec = self.epoch_time_next_event_msec(self._interval_type, self._interval_period, self._interval_offset, self._next_epoch_time_msec)
        
        return state
    
    
    async def interval_sleep(self) -> None:
        """
        # interval_sleep
        
        The task goes to sleep until the next scheduled task event.  This function should be 
        placed after the `while True:` syntax to delay the task based on the configured interval 
        type, period, and offset arguments that is synchronized to the system clock.
        
        """
        # Compute time delta until next scan event
        delta_msec = self._next_epoch_time_msec - self.epoch_time_msec
        
        # Validate time is into the future, otherwise, reset next epoch time
        if delta_msec <= 0:
            # Set epoch timestamp of the next scheduled task
            self._next_epoch_time_msec = self.epoch_time_next_event_msec(self._interval_type, self._interval_period, self._interval_offset, self._next_epoch_time_msec)
            
            # Compute time delta for next event
            delta_msec = self._next_epoch_time_msec - self.epoch_time_msec
        
        # delay the tacks
        await self._long_sleep_msec(delta_msec)
        
        # Set epoch timestamp of the next scheduled task
        self._next_epoch_time_msec = self.epoch_time_next_event_msec(self._interval_type, self._interval_period, self._interval_offset, self._next_epoch_time_msec)
        
        
    @property
    def epoch_time_msec(self) -> int:
        """
        # epoch_time_msec
        
        Gets epoch time in milli-seconds from the system clock.

        Returns:
            int: Epoch time in milli-seconds.
            
        """
        return int(round(time.time() * 1000))
    
    
    @property
    def interval_type(self) -> TimeIntoIntervalTypes:
        """
        # interval_type
        
        Gets interval precision type (seconds, minutes, hours).

        Returns:
            TimeIntoIntervalTypes: Interval precision type (seconds, minutes, hours).
            
        """
        return self._interval_type
    
    
    @property
    def interval_period(self) -> int:
        """
        # interval_period
        
        Gets interval period for interval precision type (seconds, minutes, or hours).

        Returns:
            int: Interval period for interval precision type (seconds, minutes, or hours).
            
        """
        return self._interval_period
    
    
    @property
    def interval_offset(self) -> int:
        """
        # interval_offset
        
        Gets interval offset for interval precision type (seconds, minutes, or hours).

        Returns:
            int: Interval offset for interval precision type (seconds, minutes, or hours).
            
        """
        return self._interval_offset
    
    
    @property
    def next_epoch_time_msec(self) -> int:
        """
        # next_epoch_time_msec
        
        Gets next epoch time event in milli-seconds.

        Returns:
            int: Next epoch time event in milli-seconds.
            
        """
        return self._next_epoch_time_msec
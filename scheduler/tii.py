import asyncio, time

from micropython import const





class TimeIntoIntervalTypes:
    """Time into interval types
    """
    TIME_INTO_INTERVAL_SEC = const(0)
    TIME_INTO_INTERVAL_MIN = const(1)
    TIME_INTO_INTERVAL_HR  = const(2)


class TimeIntoInterval:
    # uasyncio can't handle long delays so split into 100msec segments
    MAXT_MSEC = const(100)
    
    def __init__(self, interval_type: TimeIntoIntervalTypes, interval_period: int, interval_offset: int) -> None:
        self._interval_type        = interval_type
        self._interval_period      = interval_period
        self._interval_offset      = interval_offset
        self._next_epoch_time_msec = self.epoch_time_next_event_msec(interval_type, interval_period, interval_offset)
    
    
    async def _long_sleep_msec(self, t) -> None:  # Sleep with no bounds. Immediate return if t < 0.
        while t > 0:
            await asyncio.sleep_ms(min(t, TimeIntoInterval.MAXT_MSEC))
            t -= TimeIntoInterval.MAXT_MSEC
        
    
    def _normalize_interval_to_msec(self, interval_type: TimeIntoIntervalTypes, interval_period: int) -> int:
        """Normalize interval to milli-seconds
        Gets interval in milli-seconds from interval type and period.

        Args:
            interval_type (TimeIntoIntervalTypes): Interval type (seconds, minutes, hours).
            interval_period (int): Interval period per interval type (seconds, minutes, or hours).

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
        """Epoch time next event milli-seconds
        Gets epoch time of the next event in milli-seconds from interval type, period, and offset.

        Args:
            interval_type (TimeIntoIntervalTypes): Interval type (seconds, minutes, hours).
            interval_period (int): Interval period per interval type (seconds, minutes, or hours).
            interval_offset (int): Interval offset per interval type (seconds, minutes, or hours).
            epoch_time_last_event_msec (int, optional): Epoch time of the last event in milli-seconds. Defaults to 0.


        Returns:
            int: Epoch time of the next event in milli-seconds.
        """
        # Validate interval period argument
        if not interval_period > 0:
            raise ValueError("Interval period cannot be 0, time-into-interval epoch time event failed")
        
        # Normalize interval period and offset to milli-seconds
        interval_period_msec = self._normalize_interval_to_msec(interval_type, interval_period)
        interval_offset_msec = self._normalize_interval_to_msec(interval_type, interval_offset)
        
        # Validate interval period argument on total days
        if interval_period_msec >= (28 * 24 * 60 * 60 * 1000):
            raise ValueError("Interval period cannot be greater than 28-days, time-into-interval epoch time event failed")
        
        # Validate period and offset intervals
        if (interval_period_msec - interval_offset_msec) < 0:
            raise ValueError("Interval period must be larger than the interval offset, time-into-interval epoch time event failed")
        
        # Get system unix epoch times (seconds and milli-seconds)
        now_epoch_time_msec = self.epoch_time_msec()

        # Get now system unix epoch time parts
        now_year, now_month, now_day, now_h, now_m, now_s, now_dow, now_doy = time.gmtime()
        
        # Define next system unix epoch time parts
        next_year  = 0
        next_month = 0
        next_day   = 0
        next_h     = 0
        next_m     = 0
        next_s     = 0
        next_dow   = 0
        next_doy   = 0
        
        # Initialize next tm structure time-parts localtime based on interval-type
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
        
        # Handle interval period by tm structure time-part timespan exceedance
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
            
        # Initialize next epoch time event
        epoch_time_next_event_msec = epoch_time_last_event_msec
        
        # Validate if the next task event was computed
        if epoch_time_next_event_msec != 0:
            # Add task interval to next task event epoch to compute next task event epoch
            epoch_time_next_event_msec = epoch_time_next_event_msec + interval_period_msec + interval_offset_msec
        else:
            # Convert next time parts to unix epoch time in milli-seconds
            epoch_time_next_event_msec = int(round(time.mktime((next_year, next_month, next_day, next_h, next_m, next_s, next_dow, next_doy)) * 1000))
            
            # Initialize next unix time by adding the task event interval period and offset
            epoch_time_next_event_msec = epoch_time_next_event_msec + interval_period_msec + interval_offset_msec
            
            # Compute the delta between now and next unix times
            delta_time_msec = epoch_time_next_event_msec - now_epoch_time_msec
            
            # Ensure next task event is ahead in time
            if delta_time_msec <= 0:
                # Next task event is not ahead in time
                while delta_time_msec < 0:
                    # Keep adding task event intervals until next task event is ahead in time
                    epoch_time_next_event_msec = epoch_time_next_event_msec + interval_period_msec + interval_offset_msec
                    
                    # Compute the delta between now and next unix times
                    delta_time_msec = epoch_time_next_event_msec - now_epoch_time_msec
        
        # Return next task event epoch time
        return epoch_time_next_event_msec
    
    
    def epoch_time_msec(self) -> int:
        """Epoch time milli-seconds
        Gets epoch time in milli-seconds.

        Returns:
            int: Epoch time in milli-seconds.
        """
        return int(round(time.time() * 1000))
    
    
    def epoch_time_last_event_msec(self, interval_type: TimeIntoIntervalTypes, interval_period: int, next_epoch_time_msec: int) -> int:
        """Epoch time last event milli-seconds
        Gets epoch time of the last event in milli-seconds.

        Args:
            interval_type (TimeIntoIntervalTypes): Interval type (seconds, minutes, hours).
            interval_period (int): Interval period per interval type (seconds, minutes, or hours).
            next_epoch_time_msec (int): Next epoch time in milli-seconds.

        Returns:
            int: Epoch time of the last event in milli-seconds.
        """
        # Convert interval into msec
        interval_msec = self._normalize_interval_to_msec(interval_type, interval_period)
        
        # Set last event epoch timestamp
        return next_epoch_time_msec - interval_msec
    
    
    def interval_elapsed(self) -> bool:
        """Interval Elapsed
        Validates if interval has elapsed.

        Returns:
            bool: Interval has elapsed when true, otherwise, false
        """
        state = False
        
        # Get system unix epoch timestamp (UTC) in milliseconds
        now_epoch_time_msec = self.epoch_time_msec()
        
        # Compute time delta until next time into interval condition
        delta_msec = self._next_epoch_time_msec - now_epoch_time_msec
        
        # Validate time delta, when delta is <= 0, time has elapsed
        if delta_msec <= 0:
            # Set time-into-interval state to true - intervale has lapsed
            state = True
            
            # Set next event timestamp (UTC)
            self._next_epoch_time_msec = self.epoch_time_next_event_msec(self._interval_type, self._interval_period, self._interval_offset, self._next_epoch_time_msec)
        
        return state
    
    async def interval_sleep(self) -> None:
        """Interval Sleep
        Goes to sleep per interval configuration.
        """
        # Get system unix epoch times (milli-seconds)
        now_epoch_time_msec = self.epoch_time_msec()
        
        # Compute time delta until next scan event
        delta_msec = self._next_epoch_time_msec - now_epoch_time_msec
        
        # Validate time is into the future, otherwise, reset next epoch time
        if delta_msec <= 0:
            # Set epoch timestamp of the next scheduled task
            self._next_epoch_time_msec = self.epoch_time_next_event_msec(self._interval_type, self._interval_period, self._interval_offset, self._next_epoch_time_msec)
            
            # Compute time delta for next event
            delta_msec = self._next_epoch_time_msec - now_epoch_time_msec
        
        # delay the tacks
        await self._long_sleep_msec(delta_msec)
        
        # Set epoch timestamp of the next scheduled task
        self._next_epoch_time_msec = self.epoch_time_next_event_msec(self._interval_type, self._interval_period, self._interval_offset, self._next_epoch_time_msec)
# Copyright (c) 2024 Eric Gionet (gionet.c.eric@gmail.com)
# Released under the MIT License (MIT) - see LICENSE file

import time

"""
inspired by:
    https://forums.raspberrypi.com/viewtopic.php?t=350488


the to_list property converts parameters to a list.

tz = [ [        -8,0,0 ], # Time offset  [      H,M,S] -8, PST
        [  3,12,  2,0,0 ], # Start of DST [ M,D, H,M,S] Mar 12  2nd Sunday
        [ 11, 5,  2,0,0 ], # End   of DST [ M,D, H,M,S] Nov 5   1st Sunday
        [         1,0,0 ]  # DST Adjust   [      H,M,S] +1 hour
    ]
"""



class TimeOffset:
    """
    # TimeOffset
    
    This class configures UTC time offset.
    
    """
    def __init__(self, hour = 0, minute = 0):
        """
        # TimeOffset
        
        Constructor to initialize time-zone offset class parameters.

        Args:
            hour (int, optional): Time-zone hour offset from UTC. Defaults to 0.
            minute (int, optional): Time-zone minute offset from UTC. Defaults to 0.
            
        """
        self._hour   = hour
        self._minute = minute

    @property
    def hour(self) -> int:
        """
        # hour
        
        Gets time hour offset.

        Returns:
            int: Time hour offset.
            
        """
        return self._hour

    @property
    def minute(self) -> int:
        """
        # minute
        
        Gets time minute offset.

        Returns:
            int: Time minute offset.
            
        """
        return self._minute
    
    @property
    def offset(self) -> int:
        """
        # offset
        
        Gets time offset in seconds.

        Returns:
            int: Time offset in seconds.
            
        """
        return (self._minute * 60) + (self._hour * 60 * 60)
    
    @property
    def to_list(self) -> list:
        """
        # to_list
        
        Converts time offset parameters (e.g. hour, minute) to a list.

        Returns:
            list: Time offset parameters as a list.
            
        """
        lst = []
        lst.append(self._hour)
        lst.append(self._minute)
        return lst


class DSTAdjust:
    """
    # DSTAdjust
    
    Daylight saving time adjust class.
    
    This class configures the daylight saving time adjustment.
    
    """
    def __init__(self, hour = 0, minute = 0):
        """
        # DSTAdjust
        
        Constructor to initialize daylight saving adjust class parameters.

        Args:
            hour (int, optional): Daylight saving time hour adjustment. Defaults to 0.
            minute (int, optional): Daylight saving time minute adjustment. Defaults to 0.
            
        """
        self._hour   = hour
        self._minute = minute

    @property
    def hour(self) -> int:
        """
        # hour
        
        Gets DST adjust hour.

        Returns:
            int: DST adjust hour.
            
        """
        return self._hour

    @property
    def minute(self) -> int:
        """
        # minute
        
        Gets DST adjust minute.

        Returns:
            int: DST adjust minute.
            
        """
        return self._minute
    
    @property
    def adjust(self) -> int:
        """
        # adjust
        
        Gets DST adjust in seconds.

        Returns:
            int: DST adjust in seconds.
            
        """
        return (self._minute * 60) + (self._hour * 60 * 60)
    
    @property
    def to_list(self) -> list:
        """
        # to_list
        
        Converts DST adjust parameters (e.g. hour, minute) to a list.

        Returns:
            list: DST adjust parameters as a list.
            
        """
        lst = []
        lst.append(self._hour)
        lst.append(self._minute)
        return lst



class DSTSchedule:
    """
    # DSTSchedule
    
    Daylight saving time schedule class.
    
    This class configures daylight saving time start and end schedules.
    
    """
    def __init__(self, month = 0, day = 0, hour = 0, minute = 0):
        """
        # DSTSchedule
        
        Constructor to initialize daylight saving time schedule class parameters.

        Args:
            month (int, optional): Daylight saving time schedule hour. Defaults to 0.
            day (int, optional): Daylight saving time schedule day. Defaults to 0.
            hour (int, optional): Daylight saving time schedule hour. Defaults to 0.
            minute (int, optional): Daylight saving time schedule minute. Defaults to 0.
            
        """
        self._month  = month
        self._day    = day
        self._hour   = hour
        self._minute = minute

    @property
    def month(self) -> int:
        """
        # month
        
        Gets DST schedule month.

        Returns:
            int: DST schedule month.
            
        """
        return self._month
    
    @property
    def day(self) -> int:
        """
        # day
        
        Gets DST schedule day.

        Returns:
            int: DST schedule day.
            
        """
        return self._day
    
    @property
    def hour(self) -> int:
        """
        # hour
        
        Gets DST schedule hour.

        Returns:
            int: DST schedule hour.
            
        """
        return self._hour

    @property
    def minute(self) -> int:
        """
        # minute
        
        Gets DST schedule minute.

        Returns:
            int: DST schedule minute.
            
        """
        return self._minute
    
    @property
    def to_list(self) -> list:
        """
        # to_list
        
        Converts DST schedule parameters (e.g. hour, minute) to a list.

        Returns:
            list: DST schedule parameters as a list.
            
        """
        lst = []
        lst.append(self._month)
        lst.append(self._day)
        lst.append(self._hour)
        lst.append(self._minute)
        return lst


class TimezoneInfo:
    """
    # TimezoneInfo
    
    This class configures time-zone offset, DST start, DST end, and DST adjust parameters.
    
    """
    def __init__(self, timeoffset: TimeOffset, dststart: DSTSchedule, dstend: DSTSchedule, dstadjust: DSTAdjust):
        """
        # TimezoneInfo
        
        Constructor to initialize time-zone information class parameters.
        
        Examples:
            Instantiate timezone information object for ``Atlantic Canada`` with
            daylight saving start and end schedules, and daylight saving adjustment::
        
                tz_info = TimezoneInfo(TimeOffset(-4, 0), DSTSchedule(3, 9, 2, 0), DSTSchedule(11, 2, 2, 0), DSTAdjust(1, 0))

        Args:
            timeoffset (TimeOffset): Time-zone offset object.
            dststart (DSTSchedule): Daylight saving time start schedule object.
            dstend (DSTSchedule): Daylight saving time end schedule object.
            dstadjust (DSTAdjust): Daylight saving time adjustment object.
            
        """
        self._timeoffset = timeoffset
        self._dststart   = dststart
        self._dstend     = dstend
        self._dstadjust  = dstadjust
    
    @property
    def timezone(self) -> str:
        """
        # timezone
        
        Gets timezone from offset.

        Returns:
            str: Timezone as a formatted string (i.e. GMT+4, GMT-05:30, etc.).
            
        """
        tz = "GMT"
        if self._timeoffset.hour > 0:
            tz += "+"
        if self._timeoffset.minute == 0 and self._timeoffset.hour != 0:
            tz += str(self._timeoffset.hour)
        if(self._timeoffset.minute > 0):
            tz += "{:02d}{:02d}".format(self._timeoffset.hour, self._timeoffset.minute)
        return tz
    
    @property
    def timeoffset(self) -> TimeOffset:
        """
        # timeoffset
        
        Gets time offset object.

        Returns:
            TimeOffset: Time offset object.
            
        """
        return self._timeoffset
    
    @property
    def dststart(self) -> DSTSchedule:
        """
        # dststart
        
        Gets DST start schedule object.

        Returns:
            DSTSchedule: DST start schedule object.
            
        """
        return self._dststart
    
    @property
    def dstend(self) -> DSTSchedule:
        """
        # dstend
        
        Gets DST end schedule object.

        Returns:
            DSTSchedule: DST end schedule object.
            
        """
        return self._dstend
    
    @property
    def dstadjust(self) -> DSTAdjust:
        """
        # dstadjust
        
        Gets DST adjust object.

        Returns:
            DSTAdjust: DST adjust object.
            
        """
        return self._dstadjust
    
    @property
    def to_list(self) -> list:
        """
        # to_list
        
        Converts time-zone parameters to a list.

        Returns:
            list: time-zone parameters as a list.
            
        """
        lst = []
        lst.append(self._timeoffset.to_list)
        lst.append(self._dststart.to_list)
        lst.append(self._dstend.to_list)
        lst.append(self._dstadjust.to_list)
        return lst
    




def gmtime() -> tuple:
    """
    # gmtime
    
    Gets UTC-time as a tuple.

    Returns:
        tuple: UTC-time as a tuple (year, month, day, h, m, s, dow, doy).
        
    """
    utc = time.gmtime()
    if len(utc) <= 8:
        return utc
    lst = []
    for this in utc[:8]:
        lst.append(this)
    return tuple(lst)


def is_leap_year(year: int) -> bool:
    """
    # is_leap_year
    
    Checks if a year is a leap year.

    Args:
        year (int): Year to check.

    Returns:
        bool: True when the year is a leap year, otherwise False.
        
    """
    if (year % 400) == 0 : return True
    if (year % 100) == 0 : return False
    if (year %   4) == 0 : return True
    else                 : return False


def days_in_month(year: int, month: int) -> int:
    """
    # days_in_month
    
    Gets number of days in a month for a given year.

    Args:
        year (int): Year, for leap year validation.
        month (int): Month to get days for.

    Returns:
        int: Number of days in the month.
        
    """
    dif = 28 + is_leap_year(year)
    #       Jan Feb  Mar Apr May Jun Jul Aug Sep Oct Nov Dec
    return [31, dif, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month-1]


def localtime(tz: TimezoneInfo) -> tuple:
    """
    # localtime
    
    Gets local-time as a tuple from UTC by time-zone.
    
    Examples:
        Instantiate time-zone information object for ``Atlantic Canada`` with
        daylight saving start and end schedules, and daylight saving adjustment::
        
            tz_info = TimezoneInfo(TimeOffset(-4, 0), DSTSchedule(3, 9, 2, 0), DSTSchedule(11, 2, 2, 0), DSTAdjust(1, 0))

    Args:
        tz (TimezoneInfo): Time-zone information object.

    Returns:
        tuple: Local-time as a tuple (year, month, day, h, m, s, dow, doy).
    
    """
    #   0 1 2  3 4 5  6    7
    # ( Y,M,D, H,M,S, DOW, DOY )
    (year, month, day, h, m, s, dow, doy) = gmtime()
    
    # Use as is when before DST start
    if  month <  tz.dststart.month \
    or (month == tz.dststart.month and day == tz.dststart.day and h <  tz.dststart.hour and m <  tz.dststart.minute):
        pass
    # Use as is when after DST ends
    elif month >  tz.dstend.month \
    or  (month == tz.dstend.month and day == tz.dstend.day and h <  tz.dstend.hour and m <  tz.dstend.minute):
        pass
    # Otherwise apply the DST adjustment
    else:
        m += tz.dstadjust.minute
        h += tz.dstadjust.hour  
    # Apply the time zone offset
    m += tz.timeoffset.minute + int(s / 60)
    h += tz.timeoffset.hour + int(m / 60)
    s  = s % 60
    m  = m % 60
    # Update Y,M,D
    while h >= 24:
        h -= 24
        day += 1
        if day > days_in_month(year, month):
            month += 1
            day = 1
        dow = (dow + 1) % 7
        doy += 1
    while h < 0:
        h += 24
        day -= 1
        if day <= 0:
            month -= 1
            day = days_in_month(year, month)
        dow = (dow + 8) % 7
        doy -= 1
    return (year, month, day, h, m, s, dow, doy)



# cron.py

# Copyright (c) 2020-2023 Peter Hinch
# Released under the MIT License (MIT) - see LICENSE file

# A cron is instantiated with sequence specifier args. An instance accepts an integer time
# value (in secs since epoch) and returns the number of seconds to wait for a matching time.
# It holds no state.
# See docs for restrictions and limitations.

from time import mktime, localtime

class Cron:
    def __init__(self):
        # Validation
        self._valid = ((0, 59, 'secs'), (0, 59, 'mins'), (0, 23, 'hrs'),
                (1, 31, 'mday'), (1, 12, 'month'), (0, 6, 'wday'))
        self._mdays = {2:28, 4:30, 6:30, 9:30, 11:30}

    # Given an arg and current value, return offset between arg and cv
    # If arg is iterable return offset of next arg +ve for future -ve for past (add modulo)
    @staticmethod
    def _do_arg(a, cv) -> int:  # Arg, current value
        if a is None:
            return 0
        elif isinstance(a, int):
            return a - cv
        try:
            return min(x for x in a if x >= cv) - cv
        except ValueError:  # wrap-round
            return min(a) - cv  # -ve
        except TypeError:
            raise ValueError('Invalid argument type', type(a))
            
            
    # A call to the inner function takes 270-520μs on Pyboard depending on args
    def get_job_event_time(self, *, secs=0, mins=0, hrs=3, mday=None, month=None, wday=None) -> int:
        """Get job event time
        Returns the amount of time the job has to wait in seconds since epoch.
        
        cron1 = cron.get_job_event_time(hrs=None, mins=range(0, 60, 15))  # Every 15 minutes of every day
        
        Valid numbers are shown as inclusive ranges.
            secs=0 Seconds (0..59).
            mins=0 Minutes (0..59).
            hrs=3 Hours (0..23).
            mday=None Day of month (1..31).
            month=None Months (1..12).
            wday=None Weekday (0..6 Mon..Sun).
        
        """
        self._secs = secs
        self._mins = mins
        self._hrs = hrs
        self._mday = mday
        self._month = month
        self._wday = wday
        
        if self._secs is None:  # Special validation for seconds
            raise ValueError('Invalid None value for secs')
        if not isinstance(self._secs, int) and len(self._secs) > 1:  # It's an iterable
            ss = sorted(self._secs)
            if min((a[1] - a[0] for a in zip(ss, ss[1:]))) < 10:
                raise ValueError("Seconds values must be >= 10s apart.")
        args = (self._secs, self._mins, self._hrs, self._mday, self._month, self._wday)  # Validation for all args
        valid = iter(self._valid)
        vestr = 'Argument {} out of range'
        vmstr = 'Invalid no. of days for month'
        for arg in args:  # Check for illegal arg values
            lower, upper, errtxt = next(valid)
            if isinstance(arg, int):
                if not lower <= arg <= upper:
                    raise ValueError(vestr.format(errtxt))
            elif arg is not None:  # Must be an iterable
                if any(v for v in arg if not lower <= v <= upper):
                    raise ValueError(vestr.format(errtxt))
        if self._mday is not None and self._month is not None:  # Check mday against month
            max_md = self._mday if isinstance(self._mday, int) else max(self._mday)
            if isinstance(self._month, int):
                if max_md > self._mdays.get(month, 31):
                    raise ValueError(vmstr)
            elif sum((m for m in self._month if max_md > self._mdays.get(m, 31))):
                raise ValueError(vmstr)
        if self._mday is not None and self._wday is not None and self.do_arg(self._mday, 23) > 0:
            raise ValueError('mday must be <= 22 if wday also specified.')

        def inner(tnow) -> int:
            tev = tnow  # Time of next event: work forward from time now
            yr, mo, md, h, m, s, wd = localtime(tev)[:7]
            init_mo = mo  # Month now
            toff = self._do_arg(self._secs, s)
            tev += toff if toff >= 0 else 60 + toff

            yr, mo, md, h, m, s, wd = localtime(tev)[:7]
            toff = self._do_arg(self._mins, m)
            tev += 60 * (toff if toff >= 0 else 60 + toff)

            yr, mo, md, h, m, s, wd = localtime(tev)[:7]
            toff = self._do_arg(self._hrs, h)
            tev += 3600 * (toff if toff >= 0 else 24 + toff)

            yr, mo, md, h, m, s, wd = localtime(tev)[:7]
            toff = self._do_arg(self._month, mo)
            mo += toff
            md = md if mo == init_mo else 1
            if toff < 0:
                yr += 1
            tev = mktime((yr, mo, md, h, m, s, wd, 0))
            yr, mo, md, h, m, s, wd = localtime(tev)[:7]
            if self._mday is not None:
                if mo == init_mo:  # Month has not rolled over or been changed
                    toff = self._do_arg(self._mday, md)  # see if mday causes rollover
                    md += toff
                    if toff < 0:
                        toff = self._do_arg(self._month, mo + 1)  # Get next valid month
                        mo += toff + 1  # Offset is relative to next month
                        if toff < 0:
                            yr += 1
                else:  # Month has rolled over: day is absolute
                    md = self._do_arg(self._mday, 0)

            if self._wday is not None:
                if mo == init_mo:
                    toff = self._do_arg(self._wday, wd)
                    md += toff % 7  # mktime handles md > 31 but month may increment
                    tev = mktime((yr, mo, md, h, m, s, wd, 0))
                    cur_mo = mo
                    mo = localtime(tev)[1]  # get month
                    if mo != cur_mo:
                        toff = self._do_arg(self._month, mo)  # Get next valid month
                        mo += toff  # Offset is relative to new, incremented month
                        if toff < 0:
                            yr += 1
                        tev = mktime((yr, mo, 1, h, m, s, wd, 0))  # 1st of new month
                        yr, mo, md, h, m, s, wd = localtime(tev)[:7]  # get day of week
                        toff = self._do_arg(self._wday, wd)
                        md += toff % 7
                else:
                    md = 1 if self._mday is None else md
                    tev = mktime((yr, mo, md, h, m, s, wd, 0))  # 1st of new month
                    yr, mo, md, h, m, s, wd = localtime(tev)[:7]  # get day of week
                    md += (self._do_arg(self._wday, 0) - wd) % 7

            return mktime((yr, mo, md, h, m, s, wd, 0)) - tnow
        return inner
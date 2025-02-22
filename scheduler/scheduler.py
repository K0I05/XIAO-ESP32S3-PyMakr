# sched.py

# https://github.com/peterhinch/micropython-async/tree/master/v3/as_drivers/sched
# https://github.com/peterhinch/micropython-async/blob/master/v3/docs/SCHEDULE.md

# Copyright (c) 2020-2023 Peter Hinch
# Released under the MIT License (MIT) - see LICENSE file

import asyncio
from time import time, mktime, localtime
from scheduler.cron import Cron
from scheduler.sequence import Sequence
from micropython import const


class Scheduler:  # Enable asynchronous iterator interface
    # uasyncio can't handle long delays so split into 1000s (1e6 ms) segments
    MAXT = const(1000)
    
    # Wait prior to a sequence start: see
    # https://github.com/peterhinch/micropython-async/blob/master/v3/docs/SCHEDULE.md#71-initialisation
    PAUSE = const(2)
    
    def __init__(self) -> None:
        self._evt = asyncio.Event()
        self._type_coro = type(self._g())


    def __aiter__(self):
        return self


    async def __anext__(self):
        await self._evt.wait()
        self._evt.clear()
        return self._args
    

    async def _g(self) -> None:
        pass


    async def _long_sleep(self, t) -> None:  # Sleep with no bounds. Immediate return if t < 0.
        while t > 0:
            await asyncio.sleep(min(t, Scheduler.MAXT))
            t -= Scheduler.MAXT
        
        
    # If a callback is passed, run it and return.
    # If a coroutine is passed initiate it and return.
    # coroutines are passed by name i.e. not using function call syntax.
    def _launch_job(self, func, tup_args) -> any:
        res = func(*tup_args)
        if isinstance(res, self._type_coro):
            res = asyncio.create_task(res)
        return res

    
    async def create_schedule(self, func, *args, times=None, **kwargs) -> any:
        """Create schedule.
        
        Creates a schedule to trigger a user defined function at a user defined date-time.
        
        asyncio.create_task(scheduler.create_schedule(foo, 'every 4 mins', hrs=None, mins=range(0, 60, 4)))

        Args:
            func (function): This may be a callable (callback or coroutine) to run, a user defined Event or an instance of a Sequence.
            *args (any): secs=0 Seconds (0..59), mins=0 Minutes (0..59), hrs=3 Hours (0..23), mday=None Day of month (1..31), month=None Months (1..12), wday=None Weekday (0..6 Mon..Sun).
            times (int, optional): If an integer n is passed the callable will be run at the next n scheduled times. Hence a value of 1 specifies a one-shot event.. Defaults to None.
            **kwargs (_type_): _description_

        Returns:
            any: task or function handle.
        """
        
        tim = mktime(localtime()[:3] + (0, 0, 0, 0, 0))  # Midnight last night
        now = round(time())  # round() is for Unix
        cron = Cron() # Instantiate cron object
        fcron = cron.get_job_event_time(**kwargs)  # Cron instance for search.
        while tim < now:  # Find first future trigger in sequence
            # Defensive. fcron should never return 0, but if it did the loop would never quit
            tim += max(fcron(tim), 1)
        # Wait until just before the first future trigger
        await self._long_sleep(tim - now - Scheduler.PAUSE)  # Time to wait (can be < 0)

        while times is None or times > 0:  # Until all repeats are done (or forever).
            tw = fcron(round(time()))  # Time to wait (s) (fcron is stateless).
            await self._long_sleep(tw)
            res = None
            if isinstance(func, asyncio.Event):
                func.set()
            elif isinstance(func, Sequence):
                func.trigger(args)
            else:
                res = self._launch_job(func, args)
            if times is not None:
                times -= 1
            await asyncio.sleep_ms(1200)  # ensure we're into next second
        return res
    
    
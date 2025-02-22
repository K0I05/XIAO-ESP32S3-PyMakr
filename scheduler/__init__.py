# __init__.py Common functions for uasyncio primitives

# Copyright (c) 2018-2020 Peter Hinch
# Released under the MIT License (MIT) - see LICENSE file


from scheduler.cron import Cron
from scheduler.scheduler import Scheduler
from scheduler.time_into_interval import TimeIntoInterval
from scheduler.time_into_interval import TimeIntoIntervalTypes


import asyncio

def set_global_exception():
    def _handle_exception(loop, context):
        import sys

        sys.print_exception(context["exception"])
        sys.exit()

    loop = asyncio.get_event_loop()
    loop.set_exception_handler(_handle_exception)







from micropython import const

"""
from enum import IntEnum

class SHT4XPrecision(IntEnum):
    HIGH_PRECISION   = const(0)
    MEDIUM_PRECISION = const(1)
    LOW_PRECISION    = const(2)

class SHT4XHeaterPower(IntEnum):
    HEATER_POWER_200MW = const(0)
    HEATER_POWER_110MW = const(1)
    HEATER_POWER_20MW  = const(2)

class SHT4XHeaterTimespan(IntEnum):
    HEATER_TIMESPAN_1SEC = const(0)
    HEATER_TIMESPAN_1MS  = const(1)
"""

class SHT4XConfiguration:
    
    HIGH_PRECISION   = const(0)
    MEDIUM_PRECISION = const(1)
    LOW_PRECISION    = const(2)
    
    HEATER_POWER_200MW = const(0)
    HEATER_POWER_110MW = const(1)
    HEATER_POWER_20MW  = const(2)
    
    HEATER_TIMESPAN_1SEC = const(0)
    HEATER_TIMESPAN_1MS  = const(1)
    
    
    def __init__(self):
        self._temperature_precision: int = SHT4XConfiguration.HIGH_PRECISION
        self._heater_power: int = SHT4XConfiguration.HEATER_POWER_20MW
        self._heater_timespan: int = SHT4XConfiguration.HEATER_TIMESPAN_1SEC
        
        
    @property
    def config(self) -> bytearray:
        """Get config

        This returns the temperature precision, heater power, heater timespan configuration as stored in an instance of this class. It
        may differ from that stored on the chip. The information is returned in a format that can be written to the
        chip.
        """
        array = bytearray(1)
        array[0] = self._temperature_precision << 5 | self._heater_power << 2 | self._heater_timespan
        return array
    
    
    @property
    def temperature_precision(self) -> int:
        """Get temperature_precision"""
        return self._temperature_precision
    
    
    @temperature_precision.setter
    def temperature_precision(self, temperature_precision: int):
        """Set temperature_precision"""
        self._temperature_precision = temperature_precision
    
    
    @property
    def heater_power(self) -> int:
        """Get heater_power"""
        return self._heater_power
    
    
    @heater_power.setter
    def heater_power(self, heater_power: int):
        """Set heater_power"""
        self._heater_power = heater_power
        
    
    @property
    def heater_timespan(self) -> int:
        """Get heater_timespan"""
        return self._heater_timespan
    
    
    @heater_timespan.setter
    def heater_timespan(self, heater_timespan: int):
        """Set heater_timespan"""
        self._heater_timespan = heater_timespan
    
    
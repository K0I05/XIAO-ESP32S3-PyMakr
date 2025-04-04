from micropython import const

class LTR390Configuration:
    MEASUREMENT_GAIN_X1 = const(0)  # Gain of 1
    MEASUREMENT_GAIN_X3 = const(1)  # Gain of 3
    MEASUREMENT_GAIN_X6 = const(2)  # Gain of 6
    MEASUREMENT_GAIN_X9 = const(3)  # Gain of 9
    MEASUREMENT_GAIN_X18 = const(4)  # Gain of 18

    # Note when selecting resolution and time frames -- the higher the
    # resolution, the longer the minimum latency.
    MEASUREMENT_RESOLUTION_20BIT = const(0)  # 20-bit data, min time 400ms
    MEASUREMENT_RESOLUTION_19BIT = const(16)  # 19-bit data, min time 200ms
    MEASUREMENT_RESOLUTION_18BIT = const(32)  # 18-bit data, min time 100ms
    MEASUREMENT_RESOLUTION_17BIT = const(48)  # 17-bit data, min time 50ms
    MEASUREMENT_RESOLUTION_16BIT = const(64)  # 16-bit data, min time 25ms

    MEASUREMENT_RATE_25MS = const(0)  # Sampling time of 25ms
    MEASUREMENT_RATE_50MS = const(1)  # Sampling time of 50ms
    MEASUREMENT_RATE_100MS = const(2)  # Sampling time of 100ms
    MEASUREMENT_RATE_200MS = const(3)  # Sampling time of 200ms
    MEASUREMENT_RATE_500MS = const(4)  # Sampling time of 500ms
    MEASUREMENT_RATE_1000MS = const(5)  # Sampling time of 1000ms
    MEASUREMENT_RATE_2000MS = const(6)  # Sampling time of 2000ms
    
    MEASUREMENT_MODE_ALS = const(0)
    MEASUREMENT_MODE_UVS = const(1)

    
    def __init__(self):
        self._gain: int = LTR390Configuration.MEASUREMENT_GAIN_X3
        self._resolution: int = LTR390Configuration.MEASUREMENT_RESOLUTION_18BIT
        self._rate: int = LTR390Configuration.MEASUREMENT_RATE_100MS
        self._mode: int = LTR390Configuration.MEASUREMENT_MODE_ALS
    
    @property
    def config(self) -> bytearray:
        """Get config

        This returns the measurement gain, resolution, rate, mode configuration as stored in an instance of this class. It
        may differ from that stored on the chip. The information is returned in a format that can be written to the
        chip.
        """
        array = bytearray(1)
        array[0] = self._gain << 7 | self._resolution << 5 | self._rate << 2 | self._mode
        return array
    
    @property
    def gain(self) -> int:
        """Get measurement gain"""
        return self._gain
    
    
    @gain.setter
    def gain(self, gain: int):
        """Set measurement gain"""
        self._gain = gain
    
    
    @property
    def resolution(self) -> int:
        """Get measurement resolution"""
        return self._resolution
    
    
    @resolution.setter
    def resolution(self, resolution: int):
        """Set measurement resolution"""
        self._resolution = resolution
        
        
    @property
    def rate(self) -> int:
        """Get measurement rate"""
        return self._rate
    
    
    @rate.setter
    def rate(self, rate: int):
        """Set measurement rate"""
        self._rate = rate
        
    
    @property
    def mode(self) -> int:
        """Get measurement mode"""
        return self._mode
    
    
    @mode.setter
    def mode(self, mode: int):
        """Set measurement mode"""
        self._mode = mode
        
    
import rev.color._rev_color
import typing
import ColorSensorV3
import wpilib._wpilib
import wpilib._wpilib.I2C

__all__ = [
    "CIEColor",
    "ColorMatch",
    "ColorSensorV3"
]


class CIEColor():
    def __init__(self, X: float, Y: float, Z: float) -> None: ...
    def getX(self) -> float: 
        """
        Get the X component of the color

        :returns: CIE X
        """
    def getY(self) -> float: 
        """
        Get the Y component of the color

        :returns: CIE Y
        """
    def getYx(self) -> float: 
        """
        Get the x calculated coordinate
        of the CIE 19313 color space

        https://en.wikipedia.org/wiki/CIE_1931_color_space

        :returns: CIE Yx
        """
    def getYy(self) -> float: 
        """
        Get the y calculated coordinate
        of the CIE 19313 color space

        https://en.wikipedia.org/wiki/CIE_1931_color_space

        :returns: CIE Yy
        """
    def getZ(self) -> float: 
        """
        Get the Z component of the color

        :returns: CIE Z
        """
    pass
class ColorMatch():
    """
    REV Robotics Color Sensor V3.

    This class allows access to a REV Robotics color sensor V3 on an I2C bus.
    """
    def __init__(self) -> None: ...
    def addColorMatch(self, color: wpilib._wpilib.Color) -> None: 
        """
        Add color to match object

        :param color: color to add to matching
        """
    def matchClosestColor(self, colorToMatch: wpilib._wpilib.Color, confidence: float) -> wpilib._wpilib.Color: 
        """
        MatchColor uses euclidean distance to compare a given normalized RGB
        vector against stored values

        :param colorToMatch: color to compare against stored colors

        :param confidence: The confidence value for this match, this is
                    simply 1 - euclidean distance of the two color vectors

        :returns: Closest matching color
        """
    @typing.overload
    def matchColor(self, colorToMatch: wpilib._wpilib.Color) -> typing.Optional[wpilib._wpilib.Color]: 
        """
        MatchColor uses euclidean distance to compare a given normalized RGB
        vector against stored values

        :param colorToMatch: color to compare against stored colors

        :returns: Matched color if detected

        MatchColor uses euclidean distance to compare a given normalized RGB
        vector against stored values

        :param colorToMatch: color to compare against stored colors

        :param confidence: The confidence value for this match, this is
                    simply 1 - euclidean distance of the two color vectors

        :returns: Matched color if detected
        """
    @typing.overload
    def matchColor(self, colorToMatch: wpilib._wpilib.Color, confidence: float) -> typing.Optional[wpilib._wpilib.Color]: ...
    def setConfidenceThreshold(self, confidence: float) -> None: 
        """
        Set the confidence interval for determining color. Defaults to 0.95

        :param confidence: A value between 0 and 1
        """
    pass
class ColorSensorV3():
    """
    REV Robotics Color Sensor V3.

    This class allows access to a REV Robotics color sensor V3 on an I2C bus.
    """
    class ColorMeasurementRate():
        """
        Members:

          k25ms

          k50ms

          k100ms

          k200ms

          k500ms

          k1000ms

          k2000ms
        """
        def __eq__(self, arg0: object) -> bool: ...
        def __getstate__(self) -> int: ...
        def __hash__(self) -> int: ...
        def __init__(self, arg0: int) -> None: ...
        def __int__(self) -> int: ...
        def __ne__(self, arg0: object) -> bool: ...
        def __repr__(self) -> str: ...
        def __setstate__(self, arg0: int) -> None: ...
        @property
        def name(self) -> None:
            """
            :type: None
            """
        __members__: dict # value = {'k25ms': ColorMeasurementRate.k25ms, 'k50ms': ColorMeasurementRate.k50ms, 'k100ms': ColorMeasurementRate.k100ms, 'k200ms': ColorMeasurementRate.k200ms, 'k500ms': ColorMeasurementRate.k500ms, 'k1000ms': ColorMeasurementRate.k1000ms, 'k2000ms': ColorMeasurementRate.k2000ms}
        k1000ms: rev.color._rev_color.ColorSensorV3.ColorMeasurementRate # value = ColorMeasurementRate.k1000ms
        k100ms: rev.color._rev_color.ColorSensorV3.ColorMeasurementRate # value = ColorMeasurementRate.k100ms
        k2000ms: rev.color._rev_color.ColorSensorV3.ColorMeasurementRate # value = ColorMeasurementRate.k2000ms
        k200ms: rev.color._rev_color.ColorSensorV3.ColorMeasurementRate # value = ColorMeasurementRate.k200ms
        k25ms: rev.color._rev_color.ColorSensorV3.ColorMeasurementRate # value = ColorMeasurementRate.k25ms
        k500ms: rev.color._rev_color.ColorSensorV3.ColorMeasurementRate # value = ColorMeasurementRate.k500ms
        k50ms: rev.color._rev_color.ColorSensorV3.ColorMeasurementRate # value = ColorMeasurementRate.k50ms
        pass
    class ColorResolution():
        """
        Members:

          k20bit

          k19bit

          k18bit

          k17bit

          k16bit

          k13bit
        """
        def __eq__(self, arg0: object) -> bool: ...
        def __getstate__(self) -> int: ...
        def __hash__(self) -> int: ...
        def __init__(self, arg0: int) -> None: ...
        def __int__(self) -> int: ...
        def __ne__(self, arg0: object) -> bool: ...
        def __repr__(self) -> str: ...
        def __setstate__(self, arg0: int) -> None: ...
        @property
        def name(self) -> None:
            """
            :type: None
            """
        __members__: dict # value = {'k20bit': ColorResolution.k20bit, 'k19bit': ColorResolution.k19bit, 'k18bit': ColorResolution.k18bit, 'k17bit': ColorResolution.k17bit, 'k16bit': ColorResolution.k16bit, 'k13bit': ColorResolution.k13bit}
        k13bit: rev.color._rev_color.ColorSensorV3.ColorResolution # value = ColorResolution.k13bit
        k16bit: rev.color._rev_color.ColorSensorV3.ColorResolution # value = ColorResolution.k16bit
        k17bit: rev.color._rev_color.ColorSensorV3.ColorResolution # value = ColorResolution.k17bit
        k18bit: rev.color._rev_color.ColorSensorV3.ColorResolution # value = ColorResolution.k18bit
        k19bit: rev.color._rev_color.ColorSensorV3.ColorResolution # value = ColorResolution.k19bit
        k20bit: rev.color._rev_color.ColorSensorV3.ColorResolution # value = ColorResolution.k20bit
        pass
    class GainFactor():
        """
        Members:

          k1x

          k3x

          k6x

          k9x

          k18x
        """
        def __eq__(self, arg0: object) -> bool: ...
        def __getstate__(self) -> int: ...
        def __hash__(self) -> int: ...
        def __init__(self, arg0: int) -> None: ...
        def __int__(self) -> int: ...
        def __ne__(self, arg0: object) -> bool: ...
        def __repr__(self) -> str: ...
        def __setstate__(self, arg0: int) -> None: ...
        @property
        def name(self) -> None:
            """
            :type: None
            """
        __members__: dict # value = {'k1x': GainFactor.k1x, 'k3x': GainFactor.k3x, 'k6x': GainFactor.k6x, 'k9x': GainFactor.k9x, 'k18x': GainFactor.k18x}
        k18x: rev.color._rev_color.ColorSensorV3.GainFactor # value = GainFactor.k18x
        k1x: rev.color._rev_color.ColorSensorV3.GainFactor # value = GainFactor.k1x
        k3x: rev.color._rev_color.ColorSensorV3.GainFactor # value = GainFactor.k3x
        k6x: rev.color._rev_color.ColorSensorV3.GainFactor # value = GainFactor.k6x
        k9x: rev.color._rev_color.ColorSensorV3.GainFactor # value = GainFactor.k9x
        pass
    class LEDCurrent():
        """
        Members:

          kPulse2mA

          kPulse5mA

          kPulse10mA

          kPulse25mA

          kPulse50mA

          kPulse75mA

          kPulse100mA

          kPulse125mA
        """
        def __eq__(self, arg0: object) -> bool: ...
        def __getstate__(self) -> int: ...
        def __hash__(self) -> int: ...
        def __init__(self, arg0: int) -> None: ...
        def __int__(self) -> int: ...
        def __ne__(self, arg0: object) -> bool: ...
        def __repr__(self) -> str: ...
        def __setstate__(self, arg0: int) -> None: ...
        @property
        def name(self) -> None:
            """
            :type: None
            """
        __members__: dict # value = {'kPulse2mA': LEDCurrent.kPulse2mA, 'kPulse5mA': LEDCurrent.kPulse5mA, 'kPulse10mA': LEDCurrent.kPulse10mA, 'kPulse25mA': LEDCurrent.kPulse25mA, 'kPulse50mA': LEDCurrent.kPulse50mA, 'kPulse75mA': LEDCurrent.kPulse75mA, 'kPulse100mA': LEDCurrent.kPulse100mA, 'kPulse125mA': LEDCurrent.kPulse125mA}
        kPulse100mA: rev.color._rev_color.ColorSensorV3.LEDCurrent # value = LEDCurrent.kPulse100mA
        kPulse10mA: rev.color._rev_color.ColorSensorV3.LEDCurrent # value = LEDCurrent.kPulse10mA
        kPulse125mA: rev.color._rev_color.ColorSensorV3.LEDCurrent # value = LEDCurrent.kPulse125mA
        kPulse25mA: rev.color._rev_color.ColorSensorV3.LEDCurrent # value = LEDCurrent.kPulse25mA
        kPulse2mA: rev.color._rev_color.ColorSensorV3.LEDCurrent # value = LEDCurrent.kPulse2mA
        kPulse50mA: rev.color._rev_color.ColorSensorV3.LEDCurrent # value = LEDCurrent.kPulse50mA
        kPulse5mA: rev.color._rev_color.ColorSensorV3.LEDCurrent # value = LEDCurrent.kPulse5mA
        kPulse75mA: rev.color._rev_color.ColorSensorV3.LEDCurrent # value = LEDCurrent.kPulse75mA
        pass
    class LEDPulseFrequency():
        """
        Members:

          k60kHz

          k70kHz

          k80kHz

          k90kHz

          k100kHz
        """
        def __eq__(self, arg0: object) -> bool: ...
        def __getstate__(self) -> int: ...
        def __hash__(self) -> int: ...
        def __init__(self, arg0: int) -> None: ...
        def __int__(self) -> int: ...
        def __ne__(self, arg0: object) -> bool: ...
        def __repr__(self) -> str: ...
        def __setstate__(self, arg0: int) -> None: ...
        @property
        def name(self) -> None:
            """
            :type: None
            """
        __members__: dict # value = {'k60kHz': LEDPulseFrequency.k60kHz, 'k70kHz': LEDPulseFrequency.k70kHz, 'k80kHz': LEDPulseFrequency.k80kHz, 'k90kHz': LEDPulseFrequency.k90kHz, 'k100kHz': LEDPulseFrequency.k100kHz}
        k100kHz: rev.color._rev_color.ColorSensorV3.LEDPulseFrequency # value = LEDPulseFrequency.k100kHz
        k60kHz: rev.color._rev_color.ColorSensorV3.LEDPulseFrequency # value = LEDPulseFrequency.k60kHz
        k70kHz: rev.color._rev_color.ColorSensorV3.LEDPulseFrequency # value = LEDPulseFrequency.k70kHz
        k80kHz: rev.color._rev_color.ColorSensorV3.LEDPulseFrequency # value = LEDPulseFrequency.k80kHz
        k90kHz: rev.color._rev_color.ColorSensorV3.LEDPulseFrequency # value = LEDPulseFrequency.k90kHz
        pass
    class ProximityMeasurementRate():
        """
        Members:

          k6ms

          k12ms

          k25ms

          k50ms

          k100ms

          k200ms

          k400ms
        """
        def __eq__(self, arg0: object) -> bool: ...
        def __getstate__(self) -> int: ...
        def __hash__(self) -> int: ...
        def __init__(self, arg0: int) -> None: ...
        def __int__(self) -> int: ...
        def __ne__(self, arg0: object) -> bool: ...
        def __repr__(self) -> str: ...
        def __setstate__(self, arg0: int) -> None: ...
        @property
        def name(self) -> None:
            """
            :type: None
            """
        __members__: dict # value = {'k6ms': ProximityMeasurementRate.k6ms, 'k12ms': ProximityMeasurementRate.k12ms, 'k25ms': ProximityMeasurementRate.k25ms, 'k50ms': ProximityMeasurementRate.k50ms, 'k100ms': ProximityMeasurementRate.k100ms, 'k200ms': ProximityMeasurementRate.k200ms, 'k400ms': ProximityMeasurementRate.k400ms}
        k100ms: rev.color._rev_color.ColorSensorV3.ProximityMeasurementRate # value = ProximityMeasurementRate.k100ms
        k12ms: rev.color._rev_color.ColorSensorV3.ProximityMeasurementRate # value = ProximityMeasurementRate.k12ms
        k200ms: rev.color._rev_color.ColorSensorV3.ProximityMeasurementRate # value = ProximityMeasurementRate.k200ms
        k25ms: rev.color._rev_color.ColorSensorV3.ProximityMeasurementRate # value = ProximityMeasurementRate.k25ms
        k400ms: rev.color._rev_color.ColorSensorV3.ProximityMeasurementRate # value = ProximityMeasurementRate.k400ms
        k50ms: rev.color._rev_color.ColorSensorV3.ProximityMeasurementRate # value = ProximityMeasurementRate.k50ms
        k6ms: rev.color._rev_color.ColorSensorV3.ProximityMeasurementRate # value = ProximityMeasurementRate.k6ms
        pass
    class ProximityResolution():
        """
        Members:

          k8bit

          k9bit

          k10bit

          k11bit
        """
        def __eq__(self, arg0: object) -> bool: ...
        def __getstate__(self) -> int: ...
        def __hash__(self) -> int: ...
        def __init__(self, arg0: int) -> None: ...
        def __int__(self) -> int: ...
        def __ne__(self, arg0: object) -> bool: ...
        def __repr__(self) -> str: ...
        def __setstate__(self, arg0: int) -> None: ...
        @property
        def name(self) -> None:
            """
            :type: None
            """
        __members__: dict # value = {'k8bit': ProximityResolution.k8bit, 'k9bit': ProximityResolution.k9bit, 'k10bit': ProximityResolution.k10bit, 'k11bit': ProximityResolution.k11bit}
        k10bit: rev.color._rev_color.ColorSensorV3.ProximityResolution # value = ProximityResolution.k10bit
        k11bit: rev.color._rev_color.ColorSensorV3.ProximityResolution # value = ProximityResolution.k11bit
        k8bit: rev.color._rev_color.ColorSensorV3.ProximityResolution # value = ProximityResolution.k8bit
        k9bit: rev.color._rev_color.ColorSensorV3.ProximityResolution # value = ProximityResolution.k9bit
        pass
    class RawColor():
        def __init__(self, r: int, g: int, b: int, _ir: int) -> None: ...
        @property
        def blue(self) -> int:
            """
            :type: int
            """
        @blue.setter
        def blue(self, arg0: int) -> None:
            pass
        @property
        def green(self) -> int:
            """
            :type: int
            """
        @green.setter
        def green(self, arg0: int) -> None:
            pass
        @property
        def ir(self) -> int:
            """
            :type: int
            """
        @ir.setter
        def ir(self, arg0: int) -> None:
            pass
        @property
        def red(self) -> int:
            """
            :type: int
            """
        @red.setter
        def red(self, arg0: int) -> None:
            pass
        pass
    def __init__(self, port: wpilib._wpilib.I2C.Port) -> None: 
        """
        Constructs a ColorSensorV3.

        Note that the REV Color Sensor is really two devices in one package:
        a color sensor providing red, green, blue and IR values, and a proximity
        sensor.

        :param port: The I2C port the color sensor is attached to
        """
    def configureColorSensor(self, res: ColorSensorV3.ColorResolution, rate: ColorSensorV3.ColorMeasurementRate) -> None: 
        """
        Configure the color sensor.

        These settings are only needed for advanced users, the defaults
        will work fine for most teams. Consult the APDS-9151 for more
        information on these configuration settings and how they will affect
        color sensor measurements.

        :param res: Bit resolution output by the respective light sensor ADCs

        :param rate: Measurement rate of the light sensor
        """
    def configureProximitySensor(self, res: ColorSensorV3.ProximityResolution, rate: ColorSensorV3.ProximityMeasurementRate) -> None: 
        """
        Configure the proximity sensor.

        These settings are only needed for advanced users, the defaults
        will work fine for most teams. Consult the APDS-9151 for more
        information on these configuration settings and how they will affect
        proximity sensor measurements.

        :param res: Bit resolution output by the proximity sensor ADC.

        :param rate: Measurement rate of the proximity sensor
        """
    def configureProximitySensorLED(self, freq: ColorSensorV3.LEDPulseFrequency, current: ColorSensorV3.LEDCurrent, pulses: int) -> None: 
        """
        Configure the the IR LED used by the proximity sensor.

        These settings are only needed for advanced users, the defaults
        will work fine for most teams. Consult the APDS-9151 for more
        information on these configuration settings and how they will affect
        proximity sensor measurements.

        :param freq: The pulse modulation frequency for the proximity
              sensor LED

        :param curr: The pulse current for the proximity sensor LED

        :param pulses: The number of pulses per measurement of the
              proximity sensor LED
        """
    def getCIEColor(self) -> CIEColor: 
        """
        Get the color converted to CIE XYZ color space using factory
        calibrated constants.

        https://en.wikipedia.org/wiki/CIE_1931_color_space

        :returns: CIEColor value from sensor
        """
    def getColor(self) -> wpilib._wpilib.Color: 
        """
        Get the normalized RGB color from the sensor (normalized based on
        total R + G + B)

        :returns: frc::Color class with normalized sRGB values
        """
    def getIR(self) -> float: 
        """
        Get the normalzied IR value from the sensor. Works best when within 2 inches and
        perpendicular to surface of interest.

        :returns: Color class with normalized values
        """
    def getProximity(self) -> int: 
        """
        Get the raw proximity value from the sensor ADC. This value is largest
        when an object is close to the sensor and smallest when
        far away.

        :returns: Proximity measurement value, ranging from 0 to 2047 in
                  default configuration
        """
    def getRawColor(self) -> ColorSensorV3.RawColor: 
        """
        Get the raw color value from the sensor.

        :returns: Raw color values from sensopr
        """
    def hasReset(self) -> bool: 
        """
        Indicates if the device reset. Based on the power on status flag in the
        status register. Per the datasheet:

        Part went through a power-up event, either because the part was turned
        on or because there was power supply voltage disturbance (default at
        first register read).

        This flag is self clearing

        :returns: bool indicating if the device was reset
        """
    def setGain(self, gain: ColorSensorV3.GainFactor) -> None: 
        """
        Set the gain factor applied to color ADC measurements.

        By default, the gain is set to 3x.

        :param gain: Gain factor applied to color ADC measurements
            measurements
        """
    pass

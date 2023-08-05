import adis16470._adis16470
import typing
import ADIS16470_IMU
import wpilib._wpilib
import wpilib._wpilib.SPI
import wpilib.interfaces._interfaces

__all__ = [
    "ADIS16470CalibrationTime",
    "ADIS16470_IMU"
]


class ADIS16470CalibrationTime():
    """
    Members:

      _32ms

      _64ms

      _128ms

      _256ms

      _512ms

      _1s

      _2s

      _4s

      _8s

      _16s

      _32s

      _64s
    """
    def __eq__(self, arg0: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
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
    _128ms: adis16470._adis16470.ADIS16470CalibrationTime # value = ADIS16470CalibrationTime._128ms
    _16s: adis16470._adis16470.ADIS16470CalibrationTime # value = ADIS16470CalibrationTime._16s
    _1s: adis16470._adis16470.ADIS16470CalibrationTime # value = ADIS16470CalibrationTime._1s
    _256ms: adis16470._adis16470.ADIS16470CalibrationTime # value = ADIS16470CalibrationTime._256ms
    _2s: adis16470._adis16470.ADIS16470CalibrationTime # value = ADIS16470CalibrationTime._2s
    _32ms: adis16470._adis16470.ADIS16470CalibrationTime # value = ADIS16470CalibrationTime._32ms
    _32s: adis16470._adis16470.ADIS16470CalibrationTime # value = ADIS16470CalibrationTime._32s
    _4s: adis16470._adis16470.ADIS16470CalibrationTime # value = ADIS16470CalibrationTime._4s
    _512ms: adis16470._adis16470.ADIS16470CalibrationTime # value = ADIS16470CalibrationTime._512ms
    _64ms: adis16470._adis16470.ADIS16470CalibrationTime # value = ADIS16470CalibrationTime._64ms
    _64s: adis16470._adis16470.ADIS16470CalibrationTime # value = ADIS16470CalibrationTime._64s
    _8s: adis16470._adis16470.ADIS16470CalibrationTime # value = ADIS16470CalibrationTime._8s
    __members__: dict # value = {'_32ms': ADIS16470CalibrationTime._32ms, '_64ms': ADIS16470CalibrationTime._64ms, '_128ms': ADIS16470CalibrationTime._128ms, '_256ms': ADIS16470CalibrationTime._256ms, '_512ms': ADIS16470CalibrationTime._512ms, '_1s': ADIS16470CalibrationTime._1s, '_2s': ADIS16470CalibrationTime._2s, '_4s': ADIS16470CalibrationTime._4s, '_8s': ADIS16470CalibrationTime._8s, '_16s': ADIS16470CalibrationTime._16s, '_32s': ADIS16470CalibrationTime._32s, '_64s': ADIS16470CalibrationTime._64s}
    pass
class ADIS16470_IMU(wpilib._wpilib.GyroBase, wpilib.interfaces._interfaces.Gyro, wpilib._wpilib.ErrorBase, wpilib.interfaces._interfaces.PIDSource, wpilib._wpilib.Sendable):
    class IMUAxis():
        """
        Members:

          kX

          kY

          kZ
        """
        def __eq__(self, arg0: object) -> bool: ...
        def __getstate__(self) -> int: ...
        def __hash__(self) -> int: ...
        def __index__(self) -> int: ...
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
        __members__: dict # value = {'kX': IMUAxis.kX, 'kY': IMUAxis.kY, 'kZ': IMUAxis.kZ}
        kX: adis16470._adis16470.ADIS16470_IMU.IMUAxis # value = IMUAxis.kX
        kY: adis16470._adis16470.ADIS16470_IMU.IMUAxis # value = IMUAxis.kY
        kZ: adis16470._adis16470.ADIS16470_IMU.IMUAxis # value = IMUAxis.kZ
        pass
    @typing.overload
    def __init__(self) -> None: 
        """
        Default constructor. Uses CS0 on the 10-pin SPI port, the yaw axis is set to the IMU Z axis,
        and calibration time is defaulted to 4 seconds.

        Customizable constructor. Allows the SPI port and CS to be customized, the yaw axis used for GetAngle()
        is adjustable, and initial calibration time can be modified.

        :param yaw_axis: Selects the "default" axis to use for GetAngle() and GetRate()

        :param port: The SPI port and CS where the IMU is connected.

        :param cal_time: The calibration time that should be used on start-up.
        """
    @typing.overload
    def __init__(self, yaw_axis: ADIS16470_IMU.IMUAxis, port: wpilib._wpilib.SPI.Port, cal_time: ADIS16470CalibrationTime) -> None: ...
    def calibrate(self) -> None: 
        """
        Switches the active SPI port to standard SPI mode, writes the command to activate the new null configuration, and re-enables auto SPI.
        """
    def configCalTime(self, new_cal_time: ADIS16470CalibrationTime) -> int: 
        """
        Switches the active SPI port to standard SPI mode, writes a new value to the NULL_CNFG register in the IMU, and re-enables auto SPI.
        """
    def configDecRate(self, reg: int) -> int: ...
    def getAccelInstantX(self) -> float: ...
    def getAccelInstantY(self) -> float: ...
    def getAccelInstantZ(self) -> float: ...
    def getAngle(self) -> float: 
        """
        Returns the current integrated angle for the axis specified.

        The angle is based on the current accumulator value corrected by
        offset calibration and built-in IMU calibration. The angle is continuous,
        that is it will continue from 360->361 degrees. This allows algorithms
        that wouldn't want to see a discontinuity in the gyro output as it sweeps
        from 360 to 0 on the second time around. The axis returned by this
        function is adjusted based on the configured yaw_axis.

        :returns: the current heading of the robot in degrees. This heading is based
                  on integration of the returned rate from the gyro.
        """
    def getGyroInstantX(self) -> float: ...
    def getGyroInstantY(self) -> float: ...
    def getGyroInstantZ(self) -> float: ...
    def getRate(self) -> float: ...
    def getXComplementaryAngle(self) -> float: ...
    def getXFilteredAccelAngle(self) -> float: ...
    def getYComplementaryAngle(self) -> float: ...
    def getYFilteredAccelAngle(self) -> float: ...
    def getYawAxis(self) -> ADIS16470_IMU.IMUAxis: ...
    def initSendable(self, builder: wpilib._wpilib.SendableBuilder) -> None: ...
    def reset(self) -> None: 
        """
        Resets the gyro accumulations to a heading of zero. This can be used if
        the "zero" orientation of the sensor needs to be changed in runtime.
        """
    def setYawAxis(self, yaw_axis: ADIS16470_IMU.IMUAxis) -> int: ...
    @property
    def m_yaw_axis(self) -> ADIS16470_IMU.IMUAxis:
        """
        :type: ADIS16470_IMU.IMUAxis
        """
    @m_yaw_axis.setter
    def m_yaw_axis(self, arg0: ADIS16470_IMU.IMUAxis) -> None:
        pass
    pass

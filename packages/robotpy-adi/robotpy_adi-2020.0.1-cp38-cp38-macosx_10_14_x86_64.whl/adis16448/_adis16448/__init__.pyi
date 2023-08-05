import adis16448._adis16448
import typing
import ADIS16448_IMU
import wpilib._wpilib
import wpilib._wpilib.SPI
import wpilib.interfaces._interfaces

__all__ = [
    "ADIS16448_IMU"
]


class ADIS16448_IMU(wpilib._wpilib.GyroBase, wpilib.interfaces._interfaces.Gyro, wpilib._wpilib.ErrorBase, wpilib.interfaces._interfaces.PIDSource, wpilib._wpilib.Sendable):
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
        kX: adis16448._adis16448.ADIS16448_IMU.IMUAxis # value = IMUAxis.kX
        kY: adis16448._adis16448.ADIS16448_IMU.IMUAxis # value = IMUAxis.kY
        kZ: adis16448._adis16448.ADIS16448_IMU.IMUAxis # value = IMUAxis.kZ
        pass
    @typing.overload
    def __init__(self) -> None: 
        """
        IMU constructor on onboard MXP CS0, Z-up orientation, and complementary AHRS computation.

        IMU constructor on the specified MXP port and orientation.

        :param yaw_axis: The axis where gravity is present. Valid options are kX, kY, and kZ

        :param algorithm: The AHRS algorithm to use. Valid options are kComplementary and kMadgwick

        :param port: The SPI port where the IMU is connected.
        """
    @typing.overload
    def __init__(self, yaw_axis: ADIS16448_IMU.IMUAxis, port: wpilib._wpilib.SPI.Port, cal_time: int) -> None: ...
    def calibrate(self) -> None: 
        """
        Initialize the IMU.

        Perform gyro offset calibration by collecting data for a number of seconds and
        computing the center value. The center value is subtracted from subsequent
        measurements.

        It's important to make sure that the robot is not moving while the
        centering calculations are in progress, this is typically done when the
        robot is first turned on while it's sitting at rest before the match
        starts.

        The calibration routine can be triggered by the user during runtime.
        """
    def configCalTime(self, new_cal_time: int) -> int: ...
    def configDecRate(self, DecimationRate: int) -> int: ...
    def getAccelInstantX(self) -> float: ...
    def getAccelInstantY(self) -> float: ...
    def getAccelInstantZ(self) -> float: ...
    def getAngle(self) -> float: 
        """
        Return the actual angle in degrees that the robot is currently facing.

        The angle is based on the current accumulator value corrected by
        offset calibration and built-in IMU calibration. The angle is continuous,
        that is it will continue from 360->361 degrees. This allows algorithms
        that wouldn't want to see a discontinuity in the gyro output as it sweeps
        from 360 to 0 on the second time around. The axis returned by this
        function is adjusted fased on the configured yaw_axis.

        :returns: the current heading of the robot in degrees. This heading is based
                  on integration of the returned rate from the gyro.
        """
    def getBarometricPressure(self) -> float: ...
    def getGyroAngleX(self) -> float: ...
    def getGyroAngleY(self) -> float: ...
    def getGyroAngleZ(self) -> float: ...
    def getGyroInstantX(self) -> float: ...
    def getGyroInstantY(self) -> float: ...
    def getGyroInstantZ(self) -> float: ...
    def getMagInstantX(self) -> float: ...
    def getMagInstantY(self) -> float: ...
    def getMagInstantZ(self) -> float: ...
    def getRate(self) -> float: 
        """
        Return the rate of rotation of the yaw_axis gyro.

        The rate is based on the most recent reading of the gyro value

        :returns: the current rate in degrees per second
        """
    def getTemperature(self) -> float: ...
    def getXComplementaryAngle(self) -> float: ...
    def getXFilteredAccelAngle(self) -> float: ...
    def getYComplementaryAngle(self) -> float: ...
    def getYFilteredAccelAngle(self) -> float: ...
    def getYawAxis(self) -> ADIS16448_IMU.IMUAxis: ...
    def reset(self) -> None: 
        """
        Reset the gyro.

        Resets the gyro accumulations to a heading of zero. This can be used if
        there is significant drift in the gyro and it needs to be recalibrated
        after running.
        """
    def setYawAxis(self, yaw_axis: ADIS16448_IMU.IMUAxis) -> int: ...
    pass

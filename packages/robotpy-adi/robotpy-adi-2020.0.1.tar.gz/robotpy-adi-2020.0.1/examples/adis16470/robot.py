#!/usr/bin/env python3

import wpilib

from adis16470 import ADIS16470_IMU, ADIS16470CalibrationTime


KYAW_DEFAULT = "Z-Axis"
KYAW_X_AXIS = "X-Axis"
KYAW_Y_AXIS = "Y-Axis"


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):

        self.timer = wpilib.Timer()

        self.m_imu = ADIS16470_IMU()
        self.m_yawSelected = KYAW_DEFAULT
        self.m_runCal = False
        self.m_configCal = False
        self.m_reset = False
        self.m_setYawAxis = False

        self.m_yawActiveAxis = ADIS16470_IMU.IMUAxis.kZ

        self.m_yawChooser = wpilib.SendableChooser()
        self.m_yawChooser.setDefaultOption(KYAW_DEFAULT, KYAW_DEFAULT)
        self.m_yawChooser.addOption(KYAW_X_AXIS, KYAW_X_AXIS)
        self.m_yawChooser.addOption(KYAW_Y_AXIS, KYAW_Y_AXIS)

        wpilib.SmartDashboard.putData("IMUYawAxis", self.m_yawChooser)

        wpilib.SmartDashboard.putBoolean("RunCal", False)
        wpilib.SmartDashboard.putBoolean("ConfigCal", False)
        wpilib.SmartDashboard.putBoolean("Reset", False)
        wpilib.SmartDashboard.putBoolean("SetYawAxis", False)

    def robotPeriodic(self):
        """
        This function is called every robot packet, no matter the mode. Use
        this for items like diagnostics that you want ran during disabled,
        autonomous, teleoperated and test.

        This runs after the mode specific periodic functions, but before
        LiveWindow and SmartDashboard integrated updating.
        """

        wpilib.SmartDashboard.putNumber("YawAngle", self.m_imu.getAngle())
        wpilib.SmartDashboard.putNumber(
            "XCompAngle", self.m_imu.getXComplementaryAngle()
        )
        wpilib.SmartDashboard.putNumber(
            "YCompAngle", self.m_imu.getYComplementaryAngle()
        )
        self.m_runCal = wpilib.SmartDashboard.getBoolean("RunCal", False)
        self.m_configCal = wpilib.SmartDashboard.getBoolean("ConfigCal", False)
        self.m_reset = wpilib.SmartDashboard.getBoolean("Reset", False)
        self.m_setYawAxis = wpilib.SmartDashboard.getBoolean("SetYawAxis", False)
        self.m_yawSelected = self.m_yawChooser.getSelected()

        # Set IMU settings
        if self.m_configCal:
            self.m_imu.configCalTime(ADIS16470CalibrationTime._8s)
            wpilib.SmartDashboard.putBoolean("ConfigCal", False)
            self.m_configCal = False

        if self.m_reset:
            self.m_imu.Reset()
            wpilib.SmartDashboard.putBoolean("Reset", False)
            self.m_reset = False

        if self.m_runCal:
            self.m_imu.Calibrate()
            wpilib.SmartDashboard.putBoolean("RunCal", False)
            self.m_runCal = False

        # Read the desired yaw axis from the dashboard
        if self.m_yawSelected == "X-Axis":
            self.m_yawActiveAxis = ADIS16470_IMU.IMUAxis.kX
        elif self.m_yawSelected == "Y-Axis":
            self.m_yawActiveAxis = ADIS16470_IMU.IMUAxis.kY
        else:
            self.m_yawActiveAxis = ADIS16470_IMU.IMUAxis.kZ

        # Set the desired yaw axis from the dashboard
        if self.m_setYawAxis:
            self.m_imu.SetYawAxis(self.m_yawActiveAxis)
            wpilib.SmartDashboard.putBoolean("SetYawAxis", False)
            self.m_setYawAxis = False


if __name__ == "__main__":
    wpilib.run(MyRobot)

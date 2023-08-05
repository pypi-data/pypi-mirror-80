#!/usr/bin/env python3

from wpilib import run, IterativeRobot, SPI
from adis16448 import ADIS16448_IMU


class MyRobot(IterativeRobot):
    def robotInit(self):
        print("Starting gyro init...")
        self.myGyro = ADIS16448_IMU(ADIS16448_IMU.IMUAxis.kZ, SPI.Port.kMXP, 4)
        print("Gyro init completed.")

    def teleopInit(self):
        """Executed at the start of teleop mode"""
        pass

    def teleopPeriodic(self):
        """Runs frequently during teleop mode"""
        pass


if __name__ == "__main__":
    run(MyRobot)

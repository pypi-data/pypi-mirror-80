#!/usr/bin/env python3

from wpilib import run, IterativeRobot, SPI, Timer
from adis16448 import ADIS16448_IMU


class MyRobot(IterativeRobot):
    def robotInit(self):
        print("Starting gyro init...")
        self.myGyro = ADIS16448_IMU(ADIS16448_IMU.IMUAxis.kZ, SPI.Port.kMXP, 4)
        print("Gyro init completed.")

        self.statusTimer = Timer()
        self.statusTimer.start()

    def robotPeriodic(self):
        if self.statusTimer.get() >= 0.25:
            print(
                "X:",
                str(round(self.myGyro.getGyroAngleX(), 5)).ljust(25),
                "Y:",
                str(round(self.myGyro.getGyroAngleY(), 5)).ljust(25),
                "Z:",
                str(round(self.myGyro.getGyroAngleZ(), 5)).ljust(25),
            )
            self.statusTimer.reset()

    def teleopInit(self):
        """Executed at the start of teleop mode"""
        pass

    def teleopPeriodic(self):
        """Runs the motors with tank steering"""
        pass


if __name__ == "__main__":
    run(MyRobot)

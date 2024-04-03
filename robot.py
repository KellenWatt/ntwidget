# TODO: insert robot code here

from wpilib import TimedRobot, Joystick
from wpilib import SmartDashboard as sd


class Robot(TimedRobot):
    def robotInit(self):
        self.controller = Joystick(0)
        self.prev_val = None

    def robotPeriodic(self):
        throttle = self.controller.getThrottle()
        if self.prev_val != throttle:
            self.prev_val = throttle
            sd.putNumber("throttle", self.controller.getThrottle())
        

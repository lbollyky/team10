#!/usr/bin/env python3

import rclpy
from asl_tb3_lib.control import BaseController
from asl_tb3_msgs.msg import TurtleBotControl


class PerceptionController(BaseController):
    def __init__(self):
        super().__init__("perception_controller")
        self.kp = 2.0
        self.stopped_time = None
        self.declare_parameter("active", True)

    def get_seconds(self):
        return self.get_clock().now().nanoseconds / 1e9

    @property
    def active(self):
        return self.get_parameter("active").value
    
    def set_active(self, val):
        self.set_parameters([rclpy.Parameter("active", rclpy.Parameter.Type.BOOL, val)])
    
    
    def compute_control(self) -> TurtleBotControl:
        control = TurtleBotControl()
        if self.active:
            control.omega = 0.5
            return control
        else:
            now = self.get_seconds()
            if self.stopped_time is None:
                self.stopped_time = now
                return control
            elif now - self.stopped_time >= 5:
                self.stopped_time = None
                self.set_active(True)
                control.omega = 0.5
                return control
            else:
                return control
            
if __name__ == "__main__":  
    rclpy.init()
    controller = PerceptionController()
    rclpy.spin(controller)
    rclpy.shutdown()
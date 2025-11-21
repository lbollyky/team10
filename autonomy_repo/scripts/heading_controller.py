#!/usr/bin/env python3

import rclpy
from asl_tb3_lib.control import BaseHeadingController
from asl_tb3_lib.math_utils import wrap_angle
from asl_tb3_msgs.msg import TurtleBotControl, TurtleBotState

class HeadingController(BaseHeadingController):
    def __init__(self):
        super().__init__()
        self.kp = 2.0

    def compute_control_with_goal(self, current_state: TurtleBotState, desired_state: TurtleBotState) -> TurtleBotControl:
        error = wrap_angle(desired_state.theta - current_state.theta)
        control = TurtleBotControl()
        control.omega = self.kp * error
        return control
    

if __name__ == "__main__":  
    rclpy.init()
    controller = HeadingController()
    rclpy.spin(controller)
    rclpy.shutdown()
#!/usr/bin/env python3

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node


class ConstantControl(Node):
    def __init__(self):
        super().__init__("constant_control")
        self.publisher = self.create_publisher(Twist, "/cmd_vel", 10)
        run_every = 0.2
        self.timer = self.create_timer(run_every, self.ping)

    def ping(self):
        msg = Twist()
        msg.linear.x = 1.0
        msg.angular.z = 1.0
        self.publisher.publish(msg)


def main():
    rclpy.init()
    constant_control = ConstantControl()
    rclpy.spin(constant_control)


if __name__ == "__main__":
    main()

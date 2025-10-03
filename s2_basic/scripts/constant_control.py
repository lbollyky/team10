#!/usr/bin/env python3

import rclpy
from geometry_msgs.msg import Twist, Vector3
from std_msgs.msg import Bool
from rclpy.node import Node


class ConstantControl(Node):
    def __init__(self):
        super().__init__("constant_control")
        self.publisher = self.create_publisher(Twist, "/cmd_vel", 10)
        self.subscriber = self.create_subscription(Bool, "/kill", self.kill_cb, 10)
        run_every = 0.2
        self.timer = self.create_timer(run_every, self.ping)

    def ping_twist(self, linear=None, angular=None):
        msg = Twist()
        if linear: msg.linear = linear
        if angular: msg.angular = angular
        self.publisher.publish(msg)

    def ping(self):
        self.ping_twist(
            Vector3(x=1.0), 
            Vector3(z=1.0),
        )

    def kill_cb(self, msg: Bool):
        if msg.data:
            self.timer.cancel()
            self.ping_twist()


def main():
    rclpy.init()
    constant_control = ConstantControl()
    rclpy.spin(constant_control)


if __name__ == "__main__":
    main()

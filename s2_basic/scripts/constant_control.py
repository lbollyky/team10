#!/usr/bin/env python3

import rclpy
from std_msgs.msg import String
from rclpy.node import Node


class ConstantControl(Node):
    def __init__(self):
        super().__init__("constant_control")
        self.publisher = self.create_publisher(String, "/ping", 10)
        run_every = 0.2
        self.timer = self.create_timer(run_every, self.ping)

    def ping(self):
        msg = String()
        msg.data = "sending constant control..."
        self.publisher.publish(msg)


def main():
    rclpy.init()
    constant_control = ConstantControl()
    rclpy.spin(constant_control)


if __name__ == "__main__":
    main()

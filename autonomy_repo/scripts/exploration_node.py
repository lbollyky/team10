#!/usr/bin/env python3

import rclpy
from geometry_msgs.msg import PoseStamped
from rclpy.node import Node
from nav_msgs.msg import OccupancyGrid
from std_msgs.msg import Bool
from asl_tb3_lib.grids import StochOccupancyGrid2D
import numpy as np


class ExplorationNode(Node):
   def __init__(self):
       super().__init__("exploration_node")
       self.pose = None
       self.occupancy = None
       self.exploring = False
       # we can now define our subscribers
       self.create_subscription(Bool, "/nav_success", self.nav_callback, 10)
       self.create_subscription(PoseStamped, "/state", self.state_callback, 10)
       self.create_subscription(OccupancyGrid, "/map", self.map_callback, 10)
       # we can now define the publisher
       self.goal_pub = self.create_publisher(PoseStamped, "/goal_pose", 10)
       self.create_timer(1.0, self.explore)
       self.get_logger().info("Node started.")

   def cluster_frontiers(self, frontiers):
       return frontiers

   def select_frontiers(self, frontiers):
       if not frontiers:
           return None
       return frontiers[0]

   def nav_callback(self, msg):
       self.exploring = False
       if msg.data:
           self.get_logger().info("goal reached")
       else:
           self.get_logger().warn("navigation failed")


   def state_callback(self, msg):
       self.pose = msg


   def map_callback(self, msg):
       self.occupancy = StochOccupancyGrid2D(msg.info.resolution, msg.info.width, msg.info.height, msg.info.origin.position.x, msg.info.origin.position.y, window_size=9, default_val=0.5)
       map_data = np.array(msg.data).reshape(msg.info.height, msg.info.width)
       self.occupancy.probs = np.where(map_data== -1, 0.5, map_data / 100.0)
  
   def explore(self):
       if self.exploring or self.pose is None or self.occupancy is None:
           return


       frontiers = self.find_frontiers()


       if len(frontiers) == 0:
           self.get_logger().info("exploration complete")
           return
       goal = self.select_frontier(frontiers)
       if goal:
           self.send_goal(goal)


   def find_frontiers(self):
       frontiers = []
       probs = self.occupancy.probs
       h, w = probs.shape


       for i in range(1, h-1):
           for j in range(1, w-1):
               if probs[i, j] < 0.2:
                   for dix, djy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                       neigh = probs[i+dix, j+djy]
                       if 0.4 < neigh < 0.6:
                           x, y, = self.occupancy.grid_to_world(j, i)
                           frontiers.append((x,y))
                           break
       return self.cluster_frontiers(frontiers)
  
   def send_goal(self, goal):
       msg = PoseStamped()
       msg.header.frame_id = "map"
       msg.header.stamp = self.get_clock().now().to_msg() #clocl to clock. fixed this. 
       msg.pose.position.x = goal[0]
       msg.pose.position.y = goal[1]
       msg.pose.orientation.w = 1.0
       self.goal_pub.publish(msg)

   


def main(args=None):
   rclpy.init(args=args)
   node = ExplorationNode()
   rclpy.spin(node)
   node.destroy_node()
   rclpy.shutdown()


if __name__ == "__main__":
   main()

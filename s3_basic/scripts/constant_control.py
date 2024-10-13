#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool

class ConstantControl(Node):
    def __init__(self) -> None:
        super().__init__("constant_control")
        self.get_logger().info("Publisher has been created")

        # Create publisher and subscriber
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.sub = self.create_subscription(Bool, '/kill', self.kill_callback, 10)
        
        # Timer for publishing Twist messages
        self.timer = self.create_timer(0.2, self.callback)

        # Initialize velocities
        self.linear_velocity = 0.3
        self.angular_velocity = 0.2

    def callback(self):
        # Create and publish Twist message with velocities
        msg = Twist()
        msg.linear.x = self.linear_velocity
        msg.angular.z = self.angular_velocity
        self.pub.publish(msg)

    def kill_callback(self, msg: Bool) -> None:
        if msg.data:
            # If the kill signal is True, stop the robot
            self.get_logger().info("Kill signal received! Stopping the robot.")
            
            # Cancel the timer to stop periodic publications
            self.timer.cancel()
            
            # Publish zero velocities to stop the robot
            stop_msg = Twist()
            stop_msg.linear.x = 0.0
            stop_msg.angular.z = 0.0
            self.pub.publish(stop_msg)
            
            self.get_logger().info("Robot has been stopped.")


def main(args=None):
    rclpy.init(args=args)
    node = ConstantControl()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

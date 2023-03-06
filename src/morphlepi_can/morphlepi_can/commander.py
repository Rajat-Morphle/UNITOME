#!/usr/bin/env python3
#used to send the custom strings to the can_tx from terminal

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import time

class commander(Node):
    
    def __init__(self):
        super().__init__("commander")
        self.get_logger().info("commander node is running...")
    
        self.custom_frame_pub = self.create_publisher(String, "/frame_topic", 10)
        self.get_logger().info("Publisher created, publishing 'String' on 'frame_topic'.")
        # self.create_timer(0.2, self.send_string)
        self.send_string()

    def send_string(self):
        # self.get_logger().info("String message transmitted.")
        frame = String()

        while(True):
            input_str = input("enter the data corresponding to every byte of the data frame seperated with a space: \n")
            if (len(input_str)<17):
                print("data insufficient, fill all the data fields")
            else:
                break
        
        frame.data = input_str
        self.custom_frame_pub.publish(frame)
        self.get_logger().info("String sent")



def main(args=None):
    rclpy.init(args=args)
    node = commander()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()

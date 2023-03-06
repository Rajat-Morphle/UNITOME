#!/usr/bin/env python3
#Node transmitting the CAN messages into the CAN BUS

import os
import can
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class can_tx(Node):
    
    def __init__(self):
        super().__init__("can_tx")
        self.get_logger().info("CAN transmitter node running...")
        self.frame_sub = self.create_subscription(String, "/frame_topic", self.frame_sub_callback, 10)
    

    def frame_sub_callback(self, frame_string:String):
        # self.get_logger().info("Transmitting CAN message.")
        os.system('sudo ip link set can0 type can bitrate 1000000')
        os.system('sudo ifconfig can0 up')
        
        can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')# socketcan_native
        
        input = frame_string.data.split(" ")
        can_id = int(input[0])
        param_id = int(input[1])
        dlc_id= int(input[2])
        data_1 = int(input[3])
        data_2 = int(input[4])
        data_3 = int(input[5])
        data_4 = int(input[6])

        msg = can.Message(arbitration_id = can_id, dlc = dlc_id, data=[param_id, 0, data_1, data_2, data_3, data_4, 0, 0], is_extended_id=False)
        can0.send(msg)

        os.system('sudo ifconfig can0 down')
        # self.get_logger().info("sent")

        



def main(args = None):
    rclpy.init(args=args)
    node = can_tx()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
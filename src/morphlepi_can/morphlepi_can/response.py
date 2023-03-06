#!/usr/bin/env python3
# Receives the responses sent by the devices on the CAN bus and publish them on the response_topic

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import os
import can
import struct


class response(Node):
    
    def __init__(self):
        super().__init__("response")
        self.get_logger().info("response node is running...")
    
        self.response_pub = self.create_publisher(String, "/response_topic", 10)
        # self.get_logger().info("Publisher created, publishing 'String' on 'response_topic'.")


        self.create_timer(0.01, self.send_response)
        # self.send_response()

    def send_response(self):
        # self.get_logger().info("String message transmitted.")
        # Receiving CAN response message
        os.system('sudo ip link set can0 type can bitrate 1000000')
        os.system('sudo ifconfig can0 up')
        can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')# socketcan_native
        msg = can0.recv() #if you pass timeout in seconds like: can0.recv(2), it will return 'None' if timeout occurs. if no argument is passed, it will wait and only return the message whenever it receive one.
        # print(msg)
        # print("msg.data = %s\n" %msg.data)
        trimmed_array = msg.data[2:6] #trimming empty bytes from the bytearray
        # print(trimmed_array)
        #NOTE msg.data is a bytearray

        if(msg.is_rx == False):
            print("TX CAN MSG")
            # data_list = ["0x%02x" %b for b in msg.data] #converting the bytearray string into the list of hex values for each byte
            # print(data_list)
            # converting the byte array back to an integer:
            float_val = struct.unpack('f', trimmed_array)
            # print("Transmitted value:")
            print(float_val)

        else:
            print("RX CAN MSG")
            # data_list = ["0x%02x" %b for b in msg.data] #converting the bytearray string into the list of hex values for each byte
            # print(data_list)
            # print("Response value: " + str(data_list[2:6]))

            #Response ID
            print(msg.arbitration_id)

            # converting the byte array back to an integer:
            float_val = struct.unpack('f', trimmed_array)
            # print("response value:")
            print(float_val)
        
        # print("msg.is_rx = %s\n" %msg.is_rx)

        # NOTE you can parse the elements of the 'msg' using the following keywords like msg.timestamp
        # "timestamp",
        # "arbitration_id",
        # "is_extended_id",
        # "is_remote_frame",
        # "is_error_frame",
        # "channel",
        # "dlc",
        # "data",
        # "is_fd",
        # "is_rx",
        # "bitrate_switch",
        # "error_state_indicator",
        # "__weakref__",  # support weak references to messages


        # NOTE uncomment the below code if you are passing timeout in can0.recv() function bcz it returns None on timeout and this if statement will be executed in that case.
        # if msg is None:
        #     print("timeout occured, no message received.")
        
        #shutting down the CAN channel
        os.system("sudo ifconfig can0 down")

        # Publishing response on the response_topic
        frame = String()
        frame.data = str(msg)
        self.response_pub.publish(frame)
        # self.get_logger().info("String published")
        print("__________________________________________________________________")


# ///////////////////////////////////////////////////////////////////////////////////////////////
def main(args=None):
    rclpy.init(args=args)
    node = response()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
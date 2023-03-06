#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import struct
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from std_msgs.msg import Header
from rosgraph_msgs.msg import Clock
from rclpy.qos import ReliabilityPolicy, QoSProfile
# from rclpy import time
import time

DLC = 8

class trajectory(Node):
    def __init__(self):
        super().__init__("trajectory")
        self.get_logger().info("trajectory node is running...")

        self.t_prev = 0
        self.seconds = 0
    
        self.trajectory_pub = self.create_publisher(JointTrajectory, "/position_trajectory_controller/joint_trajectory", 10)
        self.get_logger().info("Publisher created.")
        self.create_timer(10, self.send_trajectory)
        # self.send_trajectory()

        self.custom_sub = self.create_subscription(Clock, "/clock", self.clock_cb, QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT))
        self.get_logger().info("Subscriber created.")

        self.frame_pub = self.create_publisher(String, "/frame_topic", 10)
        # self.send_trajectory()

    def clock_cb(self, t: Clock):
        self.seconds = t.clock.sec
        print(self.seconds)
        # self.get_logger().info(seconds)

    def convert(self, f): # Conversion function (Float to 8 bit unsigned int)
        byte_arr = bytearray(struct.pack("f", f))
        return byte_arr
    
    def send_string(self, data_str): # publishing the string on the frame_topic
        frame = String()
        frame.data = data_str
        self.frame_pub.publish(frame)

    def send_trajectory(self):

        x_home = -0.104
        x_max = 0.135
        y_home = -0.046
        y_max = 0.07

        vel = 150 #mm/s
        pos1 = 0  #mm
        pos2 = 220 #mm

        param_id = 1
        dlc=DLC
        can_id=0
        

        joint_trajectory_msg = JointTrajectory()
        joint_trajectory_msg.header = Header()
        # joint_trajectory_msg.header.stamp = time.time()

        joint_trajectory_msg.joint_names = ["Xjoint"]

        joint_trajectory_point = JointTrajectoryPoint()

        joint_trajectory_msg.points = [joint_trajectory_point]

        joint_trajectory_point.velocities= [0.0] # to add acceleration and decceleration in the motion of the joint. put the target velocity of the joint as 0. but it will increase the peak speed of the joint so that the average can be the value that we have entered.
        
        # joint_trajectory_point.accelerations = [0.0, 0.0, 0.0] #may use acceleration along with the position controller to maintain the acceleration and deceleration. it may create a trapezoid profile of motion.

        # NOTE you can comnbine both the sec and nanosec function.
        # joint_trajectory_point.time_from_start.nanosec = 500000000
        

        pos = float(pos1)
        duration = float((pos2-pos1)/vel)
        nanosex = int(duration*(10**9))
        print("nanosec: %f" %nanosex)
        # joint_trajectory_point.time_from_start.sec = sex
        if(nanosex <= 4294967000):
            joint_trajectory_point.time_from_start.nanosec = nanosex
        else:
            joint_trajectory_point.time_from_start.nanosec = 4294967000

        val_arr = self.convert(pos)
        data = str()
        data = (str(can_id) + " " + str(param_id)+ " " + str(dlc) + " " + str(val_arr[0]) + " " + str(val_arr[1]) + " " + str(val_arr[2]) + " " + str(val_arr[3]) )
        print("Data string: %s\n" %data)
        self.send_string(data)
        
        joint_trajectory_point.positions = [(pos/1000)+x_home]
        self.trajectory_pub.publish(joint_trajectory_msg)

        time.sleep(5)
        # _________________________________________________________________________________________________

        pos = float(pos2)
        duration = float((pos2-pos1)/vel)
        nanosex = int(duration*(10**9))
        print("nanosec: %f" %nanosex)
        # joint_trajectory_point.time_from_start.sec = sex
        if(nanosex <= 4294967000):
            joint_trajectory_point.time_from_start.nanosec = nanosex
        else:
            joint_trajectory_point.time_from_start.nanosec = 4294967000

        val_arr = self.convert(pos)
        data = str()
        data = (str(can_id) + " " + str(param_id)+ " " + str(dlc) + " " + str(val_arr[0]) + " " + str(val_arr[1]) + " " + str(val_arr[2]) + " " + str(val_arr[3]) )
        print("Data string: %s\n" %data)
        self.send_string(data)
        
        joint_trajectory_point.positions = [(pos/1000)+x_home]
        self.trajectory_pub.publish(joint_trajectory_msg)
        time.sleep(5)



        # while True:
        #     if((self.seconds-self.t_prev)<=2):
        #         # print(self.seconds-self.t_prev)
        #         continue
        #     else:
        #         break
        # self.t_prev = self.seconds
        # # print(self.t_prev)
        


def main(args=None):
    rclpy.init(args=args)
    node = trajectory()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()



    
 
# points = genfromtxt('./shaft/trajectory1.txt', delimiter=',')
    

    
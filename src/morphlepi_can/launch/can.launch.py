#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # can_tx = Node(
    #     package="morphlepi_can",
    #     executable="can_tx",
    #     name="can_tx",
    # )

    frame_rx = Node(
        package="morphlepi_can",
        executable="frame_rx",
        name="frame_rx",
    )
    
    frame_tx = Node(
        package="morphlepi_can",
        executable="frame_tx",
        name="frame_tx",
    )

    return LaunchDescription([
        # can_tx,
        frame_rx,
        frame_tx
    ])

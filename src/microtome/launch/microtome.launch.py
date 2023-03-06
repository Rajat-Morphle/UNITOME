import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess, IncludeLaunchDescription, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
import xacro

def generate_launch_description():

    morphle_bot_path = os.path.join(
        get_package_share_directory('microtome'))

    xacro_file = os.path.join(morphle_bot_path, 'bot_desc', 'microtome.urdf.xacro')

    doc = xacro.parse(open(xacro_file))
    xacro.process_doc(doc)
    robot_description_config = doc.toxml()
    robot_description = {'robot_description': robot_description_config}

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch'), '/gazebo.launch.py']),

        )

    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description, {'use_sim_time': True}]
    )

    spawn_entity = Node(
        package='gazebo_ros', executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'microtome'],
        output='screen',
        parameters=[{'use_sim_time': True}]
    )
    
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
        parameters=[{'use_sim_time': True}]
    )

    robot_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["position_trajectory_controller", "-c", "/controller_manager"],
        parameters=[{'use_sim_time': True}]
    )

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        parameters=[{'use_sim_time': True}],
    )

    rqt = Node(
        package="rqt_gui",
        executable="rqt_gui"
    )

    trajectory = Node(
        package="morphlepi_can",
        executable="trajectory",
        parameters=[{'use_sim_time': True}],
    )


    return LaunchDescription([

        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=spawn_entity,
                on_exit=[joint_state_broadcaster_spawner],
            )
        ),
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=joint_state_broadcaster_spawner,
                on_exit=[robot_controller_spawner],
            )
        ),
        # RegisterEventHandler(
        #     event_handler=OnProcessExit(
        #         target_action=robot_controller_spawner,
        #         on_exit=[trajectory],
        #     )
        # ),

        node_robot_state_publisher,
        gazebo,
        spawn_entity,
        # rviz,
        # rqt
    ])
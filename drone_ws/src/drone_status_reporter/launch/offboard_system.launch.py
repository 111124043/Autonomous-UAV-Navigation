from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([

        # Fake visual odometry (EKF position source)
        Node(
            package='drone_status_reporter',
            executable='fake_odom',
            name='fake_visual_odom',
            output='screen'
        ),

        # Offboard commander
        Node(
            package='drone_status_reporter',
            executable='commander',
            name='offboard_commander',
            output='screen'
        ),
    ])

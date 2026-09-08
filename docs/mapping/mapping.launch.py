from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/front_camera/image@sensor_msgs/msg/Image[gz.msgs.Image',
            '/front_camera/depth_image@sensor_msgs/msg/Image[gz.msgs.Image',
            '/front_camera/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo'
        ],
        output='screen'
    )

    static_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            '0.35', '0', '0.12',
            '0', '0', '0',
            'base_link',
            'front_camera_link'
        ],
        output='screen'
    )

    rtabmap = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('rtabmap_launch'),
                'launch',
                'rtabmap.launch.py'
            )
        ),
        launch_arguments={
            'rgb_topic': '/front_camera/image',
            'depth_topic': '/front_camera/depth_image',
            'camera_info_topic': '/front_camera/camera_info',
            'odom_topic': '/odom',
            'frame_id': 'base_link',
            'approx_sync': 'true',
            'qos': '2',
            'rtabmap_args': '--delete_db_on_start'
        }.items()
    )

    return LaunchDescription([
        bridge,
        static_tf,
        rtabmap
    ])

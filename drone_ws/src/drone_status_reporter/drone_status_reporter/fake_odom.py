import rclpy
from rclpy.node import Node
from px4_msgs.msg import VehicleOdometry


class FakeVisionOdom(Node):
    def __init__(self):
        super().__init__('fake_visual_odom')

        self.pub = self.create_publisher(
            VehicleOdometry,
            '/fmu/in/vehicle_odometry',
            10
        )

        self.timer = self.create_timer(0.05, self.timer_cb)  # 20 Hz
        self.get_logger().info('Publishing VehicleOdometry (VISION, NED)')

    def timer_cb(self):
        msg = VehicleOdometry()

        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)

        msg.pose_frame = VehicleOdometry.POSE_FRAME_NED
        msg.velocity_frame = VehicleOdometry.VELOCITY_FRAME_NED

        msg.position = [0.0, 0.0, -7.0]
        msg.velocity = [0.0, 0.0, 0.0]
        msg.q = [1.0, 0.0, 0.0, 0.0]

        msg.position_variance = [0.05, 0.05, 0.05]
        msg.velocity_variance = [0.05, 0.05, 0.05]

        self.pub.publish(msg)


def main():
    rclpy.init()
    node = FakeVisionOdom()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()


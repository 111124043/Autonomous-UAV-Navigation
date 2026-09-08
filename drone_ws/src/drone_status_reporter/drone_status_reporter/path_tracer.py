import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

from px4_msgs.msg import VehicleOdometry
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped


class PathTracer(Node):
    def __init__(self):
        super().__init__('path_tracer')

        # PX4 uses BEST_EFFORT → must match exactly
        qos_px4 = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        self.sub = self.create_subscription(
            VehicleOdometry,
            '/fmu/out/vehicle_odometry',
            self.odom_cb,
            qos_px4
        )

        self.path_pub = self.create_publisher(
            Path,
            '/drone/path',
            10
        )

        self.path = Path()
        self.path.header.frame_id = 'map'

        self.get_logger().info('Path tracer started (listening to PX4 odometry)')

    def odom_cb(self, msg: VehicleOdometry):
        pose = PoseStamped()
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.header.frame_id = 'map'

        # PX4 is NED → RViz is ENU
        pose.pose.position.x = float(msg.position[1])   # East → X
        pose.pose.position.y = float(msg.position[0])   # North → Y
        pose.pose.position.z = float(-msg.position[2])  # Down → Up


        self.path.poses.append(pose)
        self.path.header.stamp = pose.header.stamp

        self.path_pub.publish(self.path)


def main():
    rclpy.init()
    node = PathTracer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()


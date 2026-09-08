import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
from px4_msgs.msg import VehicleStatus, VehicleOdometry, BatteryStatus

class DroneStatusMonitor(Node):
    def __init__(self):
        super().__init__('drone_status_monitor')

        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )

        # Existing Subscribers
        self.status_sub = self.create_subscription(VehicleStatus, '/fmu/out/vehicle_status', self.status_callback, qos_profile)
        self.odom_sub = self.create_subscription(VehicleOdometry, '/fmu/out/vehicle_odometry', self.odom_callback, qos_profile)
        
        # NEW: Battery Subscriber
        self.battery_sub = self.create_subscription(BatteryStatus, '/fmu/out/battery_status', self.battery_callback, qos_profile)

        self.get_logger().info("Advanced Drone Monitor Started!")

    def battery_callback(self, msg):
        # msg.remaining is a value from 0.0 to 1.0 (e.g., 0.95 = 95%)
        percent = msg.remaining * 100
        
        if percent < 20.0:
            self.get_logger().error(f"⚠️ DANGER: Battery Low! {percent:.1f}% - LAND IMMEDIATELY")
        else:
            self.get_logger().info(f"Battery: {percent:.1f}%")

    def status_callback(self, msg):
        modes = {0: "Manual", 1: "Altitude", 2: "Position", 6: "Offboard"}
        current_mode = modes.get(msg.nav_state, f"Other ({msg.nav_state})")
        self.get_logger().info(f"MODE: {current_mode}")

    def odom_callback(self, msg):
        ros_altitude = -msg.position[2]
        self.get_logger().info(f"ALTITUDE: {ros_altitude:.2f}m")

def main(args=None):
    rclpy.init(args=args)
    node = DroneStatusMonitor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
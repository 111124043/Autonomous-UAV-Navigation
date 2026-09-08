import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
from px4_msgs.msg import OffboardControlMode, TrajectorySetpoint, VehicleCommand

class Task1(Node):
    def __init__(self):
        super().__init__('task1')

        # 1. Define the Waypoints [North, East, Down]
        # This forms a 5x5m square at 5m altitude
        self.waypoints = [
            [0.0, 0.0, -5.0],  # Takeoff point
            [5.0, 0.0, -5.0],  # Move 5m North
            [5.0, 5.0, -5.0],  # Move 5m East
            [0.0, 5.0, -5.0],  # Move 5m South
            [0.0, 0.0, -5.0]   # Return to Home
        ]
        self.current_index = 0
        self.offboard_setpoint_counter = 0

        # 2. Configure QoS (Quality of Service)
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )

        # 3. Publishers
        self.offboard_mode_pub = self.create_publisher(OffboardControlMode, '/fmu/in/offboard_control_mode', qos_profile)
        self.trajectory_pub = self.create_publisher(TrajectorySetpoint, '/fmu/in/trajectory_setpoint', qos_profile)
        self.command_pub = self.create_publisher(VehicleCommand, '/fmu/in/vehicle_command', qos_profile)

        # 4. Timer (Running at 10Hz - every 0.1s is plenty for smooth flight)
        self.timer = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        # A. ALWAYS publish the Offboard Heartbeat
        ocm = OffboardControlMode()
        ocm.position = True
        ocm.velocity = False
        ocm.acceleration = False
        ocm.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        self.offboard_mode_pub.publish(ocm)

        # B. Handle the Handshake (Arming and Switching to Offboard)
        if self.offboard_setpoint_counter < 11:
            self.offboard_setpoint_counter += 1
            if self.offboard_setpoint_counter == 10:
                self.change_mode(VehicleCommand.VEHICLE_CMD_DO_SET_MODE, 1.0, 6.0) # Offboard Mode
                self.arm()
        
        # C. Navigation Logic
        if self.current_index < len(self.waypoints):
            target = self.waypoints[self.current_index]
            
            # Create and publish the setpoint
            setpoint = TrajectorySetpoint()
            setpoint.position = [float(target[0]), float(target[1]), float(target[2])]
            setpoint.yaw = 0.0 # Facing North
            setpoint.timestamp = int(self.get_clock().now().nanoseconds / 1000)
            self.trajectory_pub.publish(setpoint)

            # For now, let's just stay at each waypoint for 5 seconds (50 counts at 10Hz)
            # Later, we can replace this with a Distance Check
            if self.offboard_setpoint_counter % 50 == 0 and self.offboard_setpoint_counter > 20:
                self.get_logger().info(f"Moving to next waypoint: {target}")
                self.current_index += 1
        else:
            self.get_logger().info("Mission Complete! Landing...")
            self.land()
            self.timer.cancel()

    def arm(self):
        self.change_mode(VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM, 1.0)

    def land(self):
        self.change_mode(VehicleCommand.VEHICLE_CMD_NAV_LAND, 1.0)

    def change_mode(self, command, param1, param2=0.0):
        msg = VehicleCommand()
        msg.command = command
        msg.param1 = param1
        msg.param2 = param2
        msg.target_system = 1
        msg.target_component = 1
        msg.source_system = 1
        msg.source_component = 1
        msg.from_external = True
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        self.command_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = Task1()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
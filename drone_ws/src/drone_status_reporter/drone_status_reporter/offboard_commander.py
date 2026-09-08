import rclpy
import math
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy

from px4_msgs.msg import (
    OffboardControlMode,
    TrajectorySetpoint,
    VehicleCommand,
    VehicleStatus
)


class OffboardCommander(Node):

    def __init__(self):
        super().__init__('offboard_commander')

        qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )

        self.offboard_pub = self.create_publisher(
            OffboardControlMode, '/fmu/in/offboard_control_mode', qos)

        self.traj_pub = self.create_publisher(
            TrajectorySetpoint, '/fmu/in/trajectory_setpoint', qos)

        self.cmd_pub = self.create_publisher(
            VehicleCommand, '/fmu/in/vehicle_command', qos)

        self.status_sub = self.create_subscription(
            VehicleStatus, '/fmu/out/vehicle_status', self.status_cb, qos)

        self.timer = self.create_timer(0.05, self.timer_cb)

        self.hover_z = -7.0
        self.takeoff_rate = 0.3
        self.land_rate = 0.4

        self.target_z = 0.0
        self.phase = 'INIT'
        self.counter = 0
        self.wp_index = 0
        self.wp_hold = 0

        self.hexagon = self.generate_hexagon()

    def generate_hexagon(self):
        h = float(math.sqrt(3))
        return [
            ( 2.0,  0.0),
            ( 1.0,  h),
            (-1.0,  h),
            (-2.0,  0.0),
            (-1.0, -h),
            ( 1.0, -h),
            ( 0.0,  0.0)
        ]

    def timer_cb(self):
        now = int(self.get_clock().now().nanoseconds / 1000)

        ocm = OffboardControlMode()
        ocm.position = True
        ocm.velocity = False
        ocm.timestamp = now
        self.offboard_pub.publish(ocm)

        sp = TrajectorySetpoint()
        sp.timestamp = now

        if self.phase == 'INIT':
            sp.position = [0.0, 0.0, 0.0]
            if self.counter == 100:
                self.set_mode(6)
                self.get_logger().info('OFFBOARD enabled')
            if self.counter == 160:
                self.arm()
                self.phase = 'TAKEOFF'
                self.get_logger().info('ARMED')
            self.counter += 1

        elif self.phase == 'TAKEOFF':
            self.target_z -= self.takeoff_rate * 0.05
            if self.target_z <= self.hover_z:
                self.target_z = self.hover_z
                self.phase = 'HEXAGON'
                self.get_logger().info('Reached hover altitude')

            sp.position = [0.0, 0.0, float(self.target_z)]

        elif self.phase == 'HEXAGON':
            x, y = self.hexagon[self.wp_index]
            sp.position = [float(x), float(y), self.hover_z]

            self.wp_hold += 1
            if self.wp_hold > 80:
                self.wp_hold = 0
                self.wp_index += 1
                if self.wp_index >= len(self.hexagon):
                    self.phase = 'LAND'
                    self.get_logger().info('Mission complete → Landing')

        elif self.phase == 'LAND':
            self.target_z += self.land_rate * 0.05
            if self.target_z >= 0.0:
                self.target_z = 0.0
                self.disarm()
                self.get_logger().info('Landed & disarmed')
                rclpy.shutdown()

            sp.position = [0.0, 0.0, float(self.target_z)]

        self.traj_pub.publish(sp)

    def arm(self):
        self.send_cmd(VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM, 1.0)

    def disarm(self):
        self.send_cmd(VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM, 0.0)

    def set_mode(self, mode):
        self.send_cmd(VehicleCommand.VEHICLE_CMD_DO_SET_MODE, 1.0, float(mode))

    def send_cmd(self, cmd, p1=0.0, p2=0.0):
        msg = VehicleCommand()
        msg.command = cmd
        msg.param1 = float(p1)
        msg.param2 = float(p2)
        msg.target_system = 1
        msg.target_component = 1
        msg.source_system = 1
        msg.source_component = 1
        msg.from_external = True
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        self.cmd_pub.publish(msg)

    def status_cb(self, msg):
        pass


def main():
    rclpy.init()
    node = OffboardCommander()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main() 

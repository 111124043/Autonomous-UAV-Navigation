# Autonomous UAV Navigation

## Overview

A ROS 2 and PX4-based autonomous UAV project focused on simulation, flight control, perception, mapping, and navigation.

The project was initially developed around PX4 Software-in-the-Loop (SITL) and Gazebo simulation, with ROS 2 used as the autonomy and perception interface. The work has progressed from basic offboard control and velocity-based flight to RGB-D based visual odometry, loop closure, and 3D mapping using RTAB-Map.

The repository also contains UAV mechanical CAD, URDF models, simulation assets, and experimental results.

---

## Current Work

### 1. PX4 + ROS 2 Simulation

- PX4 Software-in-the-Loop (SITL)
- Gazebo simulation
- ROS 2 integration
- Offboard velocity control
- Path tracing and autonomous motion
- Ground Control Station testing using QGroundControl
- ROS-Gazebo topic bridging

### 2. RGB-D Mapping and SLAM

An RGB-D camera was integrated into the simulated UAV and used with RTAB-Map for autonomous mapping.

The mapping pipeline consists of:

```text
RGB Image + Depth Image
          ↓
     RTAB-Map
          ↓
   Visual Odometry
          ↓
    Loop Closure
          ↓
 Pose Graph Optimization
          ↓
    3D Point Cloud
          ↓
      Global Map

Implemented components include:

RGB-D camera simulation
Depth sensing
Camera information publishing
ROS 2 ↔ Gazebo communication
TF frame configuration
Visual odometry
Loop closure
3D point-cloud mapping
RTAB-Map database generation
3. Stereo Vision

A Tara stereo camera was also investigated for stereo disparity and 3D reconstruction.

The stereo pipeline was tested independently using the Tara SDK:

Left Image + Right Image
          ↓
    Stereo Disparity
          ↓
   Depth / 3D Reconstruction
          ↓
      Point Cloud

The resulting point cloud was exported in PCD format for further processing.

4. UAV Mechanical Design

The project also includes mechanical design work for multirotor UAV components.

The CAD directory contains:

UAV frame components
Motor mounts
Motors and propellers
ESC
LiPo battery
Pixhawk
GPS
Raspberry Pi
Vibration isolation components
Assembly models

URDF models and associated meshes are also included for simulation and visualization.

Repository Structure
autonomous-uav-navigation/
├── README.md
├── docs/
│   ├── setup/
│   ├── simulation/
│   ├── mapping/
│   └── results/
├── drone_ws/
│   └── src/
│       ├── drone_status_reporter/
│       └── px4_mapping/
├── simulation/
│   └── models/
│       └── x500_flow/
├── cad/
├── urdf_models/
├── images/
├── videos/
└── archive/
Software Stack
Ubuntu / Pop!_OS
ROS 2 Humble
PX4 Autopilot
Gazebo
RTAB-Map
ROS-Gazebo Bridge
QGroundControl
Python
C++
SolidWorks
Tara Stereo SDK
Documentation

Detailed documentation is organized under docs/.

Setup

Installation and environment configuration:

ROS 2 setup
PX4 SITL setup
Gazebo setup
Simulation

Simulation configuration and UAV model development:

PX4-Gazebo integration
SDF model
Simulation environment
ROS-Gazebo bridge
TF configuration
Mapping

Mapping and SLAM development:

Odometry
RGB-D camera
RTAB-Map
Visual odometry
Loop closure
Point-cloud mapping
Tara stereo vision
Results

Experimental results, observations, and mapping outputs.

Future Development

The next stage of the project is focused on transferring the simulation work toward autonomous UAV operation in real environments.

Planned work includes:

IMU and optical-flow based state estimation
Sensor fusion
Real-world RGB-D / stereo perception
LiDAR-based mapping
Autonomous exploration
Obstacle avoidance
GPS-denied navigation
Real UAV implementation using Pixhawk and a companion computer
Project Status
Component	Status
PX4 SITL	Completed
Gazebo simulation	Completed
ROS 2 integration	Completed
Offboard control	Completed
Velocity-based control	Completed
RGB-D camera simulation	Completed
Visual odometry	Completed
Loop closure	Completed
RTAB-Map mapping	Completed
3D point-cloud mapping	Completed
Tara stereo reconstruction	Experimentally validated
Real UAV implementation	Planned
Autonomous exploration	Planned
Author

Dhruv Gupta
B.Tech Mechanical Engineering
National Institute of Technology Tiruchirappalli

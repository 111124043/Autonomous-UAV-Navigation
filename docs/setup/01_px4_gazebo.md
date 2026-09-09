# PX4 SITL and Gazebo Simulation Setup

This document describes the PX4 Software-In-The-Loop (SITL) and Gazebo simulation setup used in the Autonomous UAV Navigation project.

The simulation provides the UAV dynamics and simulated sensors that are later connected to ROS 2 for mapping and autonomous navigation.

---

## 1. Software Architecture

The simulation uses the following components:

- **PX4 SITL** — flight controller and UAV dynamics
- **Gazebo** — physics, environment, and simulated sensors
- **QGroundControl** — ground control station for monitoring and basic vehicle interaction
- **ROS 2 Humble** — robotics middleware
- **ros_gz_bridge** — communication bridge between Gazebo and ROS 2
- **RTAB-Map** — visual odometry, loop closure, and 3D mapping

The overall data flow is:

```text
                    ┌─────────────────┐
                    │  QGroundControl │
                    └────────┬────────┘
                             │
                             │ MAVLink
                             │
┌──────────────┐      ┌──────▼──────┐
│   Gazebo     │◄────►│  PX4 SITL   │
│              │      │             │
│ Physics      │      │ Flight      │
│ Environment  │      │ Controller  │
│ Sensors      │      │ Dynamics    │
└──────┬───────┘      └─────────────┘
       │
       │ Gazebo topics
       ▼
┌─────────────────┐
│ ros_gz_bridge   │
└────────┬────────┘
         │
         │ ROS 2 topics
         ▼
┌─────────────────┐
│    RTAB-Map     │
│                 │
│ Visual Odometry │
│ Loop Closure    │
│ 3D Mapping      │
└─────────────────┘
```

---

## 2. PX4 SITL

PX4 SITL allows the PX4 flight-control software to run on the computer instead of on a physical flight controller.

In this project, PX4 provides:

- Flight-control logic
- Vehicle dynamics interface
- Actuator/motor control
- Sensor interfaces
- MAVLink communication
- Simulation integration with Gazebo

The physical UAV is therefore represented by a simulated vehicle while PX4 runs the same general flight-control stack used for a real vehicle.

---

## 3. Gazebo

Gazebo is used to simulate the physical environment and UAV.

It provides:

- Physics simulation
- UAV model
- World/environment
- Simulated cameras
- Simulated optical-flow sensor
- Simulated rangefinder
- Sensor data published as Gazebo topics

The project contains custom simulation assets under:

```text
simulation/
├── models/
│   ├── x500_base/
│   └── x500_flow/
│
└── worlds/
    ├── forest.sdf
    └── colourful.sdf
```

### Custom `x500_base`

`x500_base` is the finalized custom base UAV model included in the repository as a reusable vehicle model.

It contains the UAV body, rotor geometry, inertial properties, and sensor definitions used by the simulation model.

The model is stored in:

```text
simulation/models/x500_base/
```

### `x500_flow`

`x500_flow` is the sensor-equipped UAV configuration used in the mapping simulation.

It is based on the PX4 X500 model and adds:

- Optical-flow sensor
- LW20 rangefinder
- Front-facing RGB-D camera

The model is stored in:

```text
simulation/models/x500_flow/
```

> **Note:** `x500_base` is currently included in the repository as a finalized model asset. The current `x500_flow` simulation configuration is intentionally left unchanged.

---

## 4. Simulation Worlds

Two Gazebo worlds are included in the repository.

### Forest World

```text
simulation/worlds/forest.sdf
```

The forest environment was used to evaluate the mapping pipeline.

It contains:

- Oak and pine trees
- Grass
- Directional sunlight
- A simulated outdoor environment

The mapped test area was approximately 40 × 43 m.

### Colourful World

```text
simulation/worlds/colourful.sdf
```

This is a small self-contained environment designed primarily for visual and optical-flow testing.

It contains:

- A floor
- Coloured boundary walls
- Coloured visual features
- Pillars
- Cubes
- Multiple light sources

The world does not depend on external textures or meshes.

---

## 5. Starting PX4 SITL

First open a terminal and enter the PX4-Autopilot directory:

```bash
cd ~/PX4-Autopilot
```

Then start the X500 Flow simulation:

```bash
PX4_GZ_SIM_RENDER_ENGINE=ogre make px4_sitl_default gz_x500_flow
```

### Command breakdown

#### `PX4_GZ_SIM_RENDER_ENGINE=ogre`

Selects the Gazebo rendering engine used for the simulation.

#### `make`

Invokes the PX4 build system.

#### `px4_sitl_default`

Selects the PX4 Software-In-The-Loop build target.

#### `gz_x500_flow`

Starts the Gazebo X500 Flow simulation configuration.

After the command starts successfully, PX4 SITL and Gazebo should be running.

---

## 6. QGroundControl

QGroundControl can be started separately to monitor the simulated vehicle.

From the directory containing the QGroundControl AppImage:

```bash
./QGroundControl.AppImage
```

QGroundControl communicates with PX4 through MAVLink.

It is useful for:

- Monitoring vehicle state
- Viewing telemetry
- Checking connection status
- Basic flight-control interaction during development

QGroundControl is not part of the ROS 2 mapping pipeline itself.

---

## 7. ROS 2 Workspace

The ROS 2 workspace used by this project is:

```text
drone_ws/
```

The relevant packages are located under:

```text
drone_ws/src/
```

Before using the workspace, source ROS 2:

```bash
source /opt/ros/humble/setup.bash
```

Then source the workspace:

```bash
source ~/autonomous-uav-navigation/drone_ws/install/setup.bash
```

The first command makes ROS 2 Humble available in the terminal.

The second command makes the packages built in this workspace available.

---

## 8. Gazebo–ROS 2 Communication

Gazebo and ROS 2 use different communication systems.

The project uses:

```text
ros_gz_bridge
```

to connect them.

The bridge converts selected Gazebo messages into ROS 2 messages.

For example:

```text
Gazebo Camera
     │
     │ Gazebo Image message
     ▼
ros_gz_bridge
     │
     │ sensor_msgs/msg/Image
     ▼
ROS 2
```

The mapping launch file bridges the following camera topics:

```text
/front_camera/image
/front_camera/depth_image
/front_camera/camera_info
```

These are then available to ROS 2 nodes such as RTAB-Map.

---

## 9. Starting the ROS 2 Mapping Pipeline

After PX4 SITL and Gazebo are running, open another terminal.

Source ROS 2:

```bash
source /opt/ros/humble/setup.bash
```

Source the project workspace:

```bash
source ~/autonomous-uav-navigation/drone_ws/install/setup.bash
```

Then start the mapping pipeline:

```bash
ros2 launch px4_mapping mapping.launch.py
```

The launch file starts:

- Gazebo–ROS 2 camera bridges
- Static camera TF
- RTAB-Map

RTAB-Map receives:

- RGB image
- Depth image
- Camera information
- Odometry

and uses them for visual odometry, loop closure, and 3D mapping.

---

## 10. TF Structure

The mapping system uses the following coordinate-frame hierarchy:

```text
map
 │
 ▼
odom
 │
 ▼
base_link
 │
 ▼
front_camera_link
```

The frames have different purposes:

- `map` — global mapping frame
- `odom` — locally continuous odometry frame
- `base_link` — UAV body frame
- `front_camera_link` — coordinate frame of the front camera

The static transform between the UAV body and front camera is defined in the mapping launch file.

The camera position relative to `base_link` is:

```text
x = 0.35 m
y = 0.00 m
z = 0.12 m
```

---

## 11. Data Flow to RTAB-Map

The complete mapping data flow is:

```text
Front RGB Camera
       │
       ▼
RGB Image ──────────────┐
                        │
Front Depth Camera      │
       │                │
       ▼                │
Depth Image ────────────┤
                        │
Camera Info ────────────┤
                        ▼
                    RTAB-Map
                        │
             ┌──────────┴──────────┐
             ▼                     ▼
      Visual Odometry        Loop Closure
             │                     │
             └──────────┬──────────┘
                        ▼
                  3D Point Cloud
                        │
                        ▼
                       Map
```

RTAB-Map estimates the camera/UAV motion from the visual information and uses loop closures to reduce accumulated drift when previously observed areas are recognized again.

---

## 12. Important Notes

The repository separates the simulation assets from the ROS 2 workspace.

Simulation assets are stored under:

```text
simulation/
```

ROS 2 packages are stored under:

```text
drone_ws/src/
```

Generated ROS 2 files such as:

```text
build/
install/
log/
```

are intentionally excluded from Git.

These directories are generated locally when the ROS 2 workspace is built.

Large generated mapping databases and other local experimental data are also not intended to be committed to the public repository.

---

## 13. Typical Development Workflow

A typical simulation session follows this order.

### Terminal 1 — PX4 + Gazebo

```bash
cd ~/PX4-Autopilot

PX4_GZ_SIM_RENDER_ENGINE=ogre make px4_sitl_default gz_x500_flow
```

### Terminal 2 — QGroundControl

```bash
./QGroundControl.AppImage
```

### Terminal 3 — ROS 2 Mapping

```bash
source /opt/ros/humble/setup.bash
source ~/autonomous-uav-navigation/drone_ws/install/setup.bash

ros2 launch px4_mapping mapping.launch.py
```

The resulting system can be summarized as:

```text
PX4 SITL
   │
   ▼
Gazebo
   │
   │ simulated sensor data
   ▼
ros_gz_bridge
   │
   ▼
ROS 2
   │
   ▼
RTAB-Map
   │
   ├── Visual Odometry
   ├── Loop Closure
   └── 3D Mapping
```

---

## 14. Project Context

This simulation setup was developed as the foundation for autonomous UAV navigation using vision-based mapping.

The initial objective was to establish and validate the complete pipeline in simulation before moving toward hardware integration.

The hardware stereo-camera work using the Tara camera is documented separately.

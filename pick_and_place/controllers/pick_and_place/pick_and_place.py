"""Pick and place - YOUR CONTROLLER / TWOJ STEROWNIK.

Goal: move the cubes (red, green, yellow) into the blue crate.
The judge robot prints the result and the time in the Webots console.

You can control the arm in two ways:
  - move_to_pose(x, y, z, roll, pitch, yaw) - give the position of the grasp
    point (between the fingertips) and the gripper orientation; the joint
    angles are computed by inverse kinematics (file ur5e_kinematics.py),
  - move_to(joint_angles) - give the 6 joint angles directly.

Coordinates are in metres in the robot base frame: X forward, Y to the left,
Z up, origin at the base of the robot on the floor.
Orientation (radians): roll = pitch = yaw = 0 means the gripper points straight
down and the fingers close along the X axis. yaw turns the gripper around the
vertical axis, roll and pitch tilt it.

Fill in the parts marked TODO.
"""
import math

from controller import Robot

from ur5e_kinematics import IKError, forward_kinematics, inverse_kinematics

robot = Robot()
timestep = int(robot.getBasicTimeStep())

# --- Robot devices -----------------------------------------------------------
JOINTS = ["shoulder_pan_joint", "shoulder_lift_joint", "elbow_joint",
          "wrist_1_joint", "wrist_2_joint", "wrist_3_joint"]
motors = [robot.getDevice(name) for name in JOINTS]
sensors = [robot.getDevice(name + "_sensor") for name in JOINTS]
for sensor in sensors:
    sensor.enable(timestep)
for motor in motors:
    motor.setVelocity(1.0)  # joint speed [rad/s], you may change it

finger_left = robot.getDevice("ROBOTIQ 2F-85 Gripper::left finger joint")
finger_right = robot.getDevice("ROBOTIQ 2F-85 Gripper::right finger joint")


# --- Helper functions --------------------------------------------------------
def wait(seconds):
    """Wait for the given number of seconds of simulation time."""
    for _ in range(int(seconds * 1000 / timestep)):
        robot.step(timestep)


def current_angles():
    """Current joint angles [rad]."""
    return [s.getValue() for s in sensors]


def current_position():
    """Current position (x, y, z) of the grasp point [m]."""
    position, _ = forward_kinematics(current_angles())
    return [round(v, 3) for v in position]


def move_to(joint_angles, tolerance=0.01, timeout=10.0):
    """Set the 6 arm joints [rad] and wait until the arm gets there."""
    for motor, angle in zip(motors, joint_angles):
        motor.setPosition(angle)
    elapsed = 0.0
    while robot.step(timestep) != -1:
        elapsed += timestep / 1000.0
        error = max(abs(s.getValue() - a) for s, a in zip(sensors, joint_angles))
        if error < tolerance:
            return True
        if elapsed > timeout:
            print("Warning: the arm did not reach the target within", timeout, "s")
            return False


def move_to_pose(x, y, z, roll=0.0, pitch=0.0, yaw=0.0, linear=False):
    """Move the grasp point to (x, y, z) [m] with the given orientation [rad].

    linear=False - the arm moves along the shortest path in joint space
                   (fast, but the gripper does not move in a straight line),
    linear=True  - the gripper moves along a straight line, in 1 cm steps
                   (slower, use it to go down to a cube and to lift it).
    Returns False if the pose cannot be reached.
    """
    try:
        if not linear:
            return move_to(inverse_kinematics(x, y, z, roll, pitch, yaw, initial=current_angles()))
        start = current_position()
        steps = max(1, int(math.dist(start, (x, y, z)) / 0.01))
        q = current_angles()
        for i in range(1, steps + 1):
            k = i / steps
            p = [s + (e - s) * k for s, e in zip(start, (x, y, z))]
            q = inverse_kinematics(*p, roll, pitch, yaw, initial=q)
            move_to(q, tolerance=0.05 if i < steps else 0.01)
        return True
    except IKError as error:
        print("IK error:", error)
        return False


def open_gripper():
    finger_left.setPosition(0.0)
    finger_right.setPosition(0.0)
    wait(1.0)


def close_gripper():
    finger_left.setPosition(0.8)
    finger_right.setPosition(0.8)
    wait(1.0)


# --- Scene data --------------------------------------------------------------
# Cube centres [m] and their rotation around the vertical axis [rad].
# The cubes are 5 cm wide. During the evaluation the cube positions may be
# changed (also in this dictionary), so your program should use these data.
CUBES = {
    "red":    {"position": (0.45, -0.15, 0.025), "yaw": -0.6074},
    "green":  {"position": (0.55, 0.05, 0.025), "yaw": -0.1536},
    "yellow": {"position": (0.40, 0.20, 0.025), "yaw": 0.1588},
}
CRATE_CENTER = (0.0, 0.5)  # crate centre (x, y); the crate walls are 12 cm high

HOME = [0.0, -1.57, 1.57, -1.57, -1.57, 0.0]   # joint angles of the start pose


# --- Main program ------------------------------------------------------------
open_gripper()
move_to(HOME)
print("Arm in the HOME position, grasp point at:", current_position())

# Example: move the gripper 15 cm above the red cube, pointing down,
# with the fingers parallel to the cube faces.
x, y, z = CUBES["red"]["position"]
move_to_pose(x, y, z + 0.15, yaw=CUBES["red"]["yaw"])
print("Above the red cube:", current_position())

# TODO: program the sequence of moves for every cube:
# 1. move above the cube (done above for the red one)
# 2. go down to the cube (tip: linear=True)
# 3. close the gripper
# 4. lift the cube
# 5. move it above the crate
# 6. open the gripper

while robot.step(timestep) != -1:
    pass

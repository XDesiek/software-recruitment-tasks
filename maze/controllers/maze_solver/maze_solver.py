"""Maze - YOUR CONTROLLER / TWOJ STEROWNIK.

Goal: drive from the start to the green goal area as fast as possible,
without touching the walls.

Devices of the e-puck robot:
  - 'left wheel motor', 'right wheel motor'   - wheels, max speed 6.28 rad/s
  - 'left wheel sensor', 'right wheel sensor' - wheel encoders [rad]
  - 'ps0' ... 'ps7'  - infrared distance sensors around the robot
        ps0, ps7 - front, ps1 - front-right, ps2 - right, ps5 - left, ps6 - front-left
        ps3, ps4 - back
        about 65-70 = nothing nearby, about 150 = wall 4 cm away, more = closer
  - 'gs0', 'gs1', 'gs2' - ground sensors (the green goal area is darker than the floor)

Maze geometry: cells are 12 cm x 12 cm, walls are 1 cm thick.
Wheel radius: 2.05 cm, distance between the wheels: 5.2 cm.

Fill in the parts marked TODO.
"""
from controller import Robot
from maze_brain import Maze
from robot_brain import RobotBrain
MAX_SPEED = 6.28

robot = Robot()
robot_brain = RobotBrain()
maze = Maze(size=8)
timestep = int(robot.getBasicTimeStep())


# --- Motors ------------------------------------------------------------------
left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")
left_motor.setPosition(float("inf"))   # velocity control mode
right_motor.setPosition(float("inf"))
left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)
motors = (left_motor, right_motor)

# --- Wheel encoders ----------------------------------------------------------
left_encoder = robot.getDevice("left wheel sensor")
right_encoder = robot.getDevice("right wheel sensor")
left_encoder.enable(timestep)
right_encoder.enable(timestep)
encoders =(left_encoder, right_encoder)

# --- Distance sensors --------------------------------------------------------
distance_sensors = []
for i in range(8):
    sensor = robot.getDevice(f"ps{i}")
    sensor.enable(timestep)
    distance_sensors.append(sensor)

# --- Ground sensors ----------------------------------------------------------
ground_sensors = []
for name in ["gs0", "gs1", "gs2"]:
    sensor = robot.getDevice(name)
    sensor.enable(timestep)
    ground_sensors.append(sensor)
parts = {"motors": motors, "encoders": encoders, "distance_sensors": distance_sensors, "ground_sensors": ground_sensors}

def clamp(value, low=-MAX_SPEED, high=MAX_SPEED):
    return max(low, min(high, value))

# --- Main loop ---------------------------------------------------------------
while robot.step(timestep) != -1:
    ps = [s.getValue() for s in distance_sensors]
    importatnt_sensors = (max(ps[0], ps[7]),ps[2],max(ps[3], ps[4]),ps[5    ])

    # print ("importatnt_sensors: ", importatnt_sensors)
    if robot_brain.driving:
        (left_speed,right_speed)=robot_brain.travel(encoders=encoders)
        left_motor.setVelocity(clamp(left_speed))
        right_motor.setVelocity(clamp(right_speed))
    elif not maze.solved:
        # TODO:scan and update to maze brain

        walls = robot_brain.scan(importatnt_sensors)
        # print(importatnt_sensors)
        maze.set_walls(walls)
        direction = maze.choose_tile()
        print(direction)
        robot_brain.set_travel(direction)
        # print("current: ",maze.current_tile.paths)
        maze.go_to_next_tile(direction= direction)
        # print("next:    ",maze.current_tile.paths)



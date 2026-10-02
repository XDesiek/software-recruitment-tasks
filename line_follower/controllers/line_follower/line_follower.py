"""Line follower - YOUR CONTROLLER / TWOJ STEROWNIK.

The e-puck robot has three ground sensors at the front:
    gs0 - left, gs1 - centre, gs2 - right
They return about 300 on the black line and about 750 on the white floor.

Wheels are driven by 'left wheel motor' and 'right wheel motor'.
Maximum wheel speed: 6.28 rad/s.

Fill in the parts marked TODO.
"""
from controller import Robot

MAX_SPEED = 6.28

robot = Robot()
timestep = int(robot.getBasicTimeStep())

# --- Motors ------------------------------------------------------------------
left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")
left_motor.setPosition(float("inf"))   # velocity control mode
right_motor.setPosition(float("inf"))
left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)

# --- Ground sensors ----------------------------------------------------------
ground_sensors = []
for name in ["gs0", "gs1", "gs2"]:
    sensor = robot.getDevice(name)
    sensor.enable(timestep)
    ground_sensors.append(sensor)


def clamp(value, low=-MAX_SPEED, high=MAX_SPEED):
    return max(low, min(high, value))


# --- Main loop ---------------------------------------------------------------
while robot.step(timestep) != -1:
    left, centre, right = [s.getValue() for s in ground_sensors]

    # Uncomment to see the sensor values in the console:
    # print(f"gs0={left:.0f}  gs1={centre:.0f}  gs2={right:.0f}")

    # TODO: compute the wheel speeds based on the sensor readings.
    # Right now the robot just drives straight ahead.
    left_speed = 2.0
    right_speed = 2.0

    left_motor.setVelocity(clamp(left_speed))
    right_motor.setVelocity(clamp(right_speed))

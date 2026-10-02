"""Maze judge. DO NOT MODIFY.

Measures the time from the start until the robot centre enters the green goal
area. Every touch of a wall adds a time penalty.
Results are printed in the Webots console.
"""
import json
import math
import os
import sys

from controller import Supervisor

TIME_LIMITS = {"maze_1": 180.0, "maze_2": 300.0}   # [s] of simulation time
TOUCH_PENALTY = 2.0      # [s] added for every wall touch
ROBOT_RADIUS = 0.037     # [m]
WALL_HALF = 0.005        # [m] half of the wall thickness
CHECK_PERIOD = 0.032     # [s]

maze = sys.argv[1] if len(sys.argv) > 1 else "maze_1"
with open(os.path.join(os.path.dirname(__file__), maze + ".json")) as f:
    data = json.load(f)
walls = data["walls"]
gx, gy = data["goal"]
goal_half = data["goal_half"]
time_limit = TIME_LIMITS.get(maze, 300.0)

judge = Supervisor()
timestep = int(judge.getBasicTimeStep())
robot = judge.getFromDef("EPUCK")


def distance_to_segment(px, py, x0, y0, x1, y1):
    dx, dy = x1 - x0, y1 - y0
    t = max(0.0, min(1.0, ((px - x0) * dx + (py - y0) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - (x0 + t * dx), py - (y0 + t * dy))


def touching_wall(x, y):
    limit = ROBOT_RADIUS + WALL_HALF + 0.001
    return any(distance_to_segment(x, y, *w) < limit for w in walls)


print(f"[JUDGE] {maze}: time limit {time_limit:.0f} s, wall touch penalty {TOUCH_PENALTY:.0f} s")
touches = 0
in_contact = False
done = False
next_check = 0.0

while judge.step(timestep) != -1:
    t = judge.getTime()
    if done or t < next_check:
        continue
    next_check += CHECK_PERIOD
    x, y, _ = robot.getPosition()

    contact = touching_wall(x, y)
    if contact and not in_contact:
        touches += 1
        print(f"[JUDGE] t = {t:6.1f} s  wall touch #{touches}")
    in_contact = contact

    if abs(x - gx) < goal_half and abs(y - gy) < goal_half:
        score = t + touches * TOUCH_PENALTY
        print(f"[JUDGE] ===== RESULT: GOAL REACHED in {t:.2f} s, wall touches: {touches}, "
              f"final score: {score:.2f} s =====")
        done = True
    elif t >= time_limit:
        print(f"[JUDGE] ===== RESULT: TIME LIMIT, goal not reached (wall touches: {touches}) =====")
        done = True

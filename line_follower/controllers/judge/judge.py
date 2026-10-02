"""Line follower judge. DO NOT MODIFY.

Measures the time of one full lap along the line. The lap counts only if the
robot follows the whole track in the right direction. If the robot leaves the
line for longer than OFF_TRACK_TIME seconds, the attempt is over.

Results are printed in the Webots console.
"""
import json
import math
import os
import sys

from controller import Supervisor

TIME_LIMIT = 180.0      # [s] of simulation time
OFF_TRACK_DIST = 0.06   # [m] max distance between robot centre and the line
OFF_TRACK_TIME = 3.0    # [s] how long the robot may stay off the line
CHECK_PERIOD = 0.064    # [s]

track = sys.argv[1] if len(sys.argv) > 1 else "track_1"
with open(os.path.join(os.path.dirname(__file__), track + ".json")) as f:
    data = json.load(f)
points = data["points"]
length = data["length"]
n = len(points)
step = length / n

judge = Supervisor()
timestep = int(judge.getBasicTimeStep())
robot = judge.getFromDef("EPUCK")


def nearest(x, y, centre, before, after):
    """Nearest path index in a window around `centre` (indices wrap)."""
    best, best_d = centre, 1e9
    for k in range(-before, after + 1):
        i = (centre + k) % n
        d = math.hypot(points[i][0] - x, points[i][1] - y)
        if d < best_d:
            best, best_d = i, d
    return best, best_d


print(f"[JUDGE] {track}: track length {length:.2f} m, time limit {TIME_LIMIT:.0f} s")
index = n - int(0.03 / step) - 1   # robot starts 3 cm before the start line
progress = -0.03
off_since = None
next_check = 0.0
done = False
last_report = 0.25

while judge.step(timestep) != -1:
    t = judge.getTime()
    if done or t < next_check:
        continue
    next_check += CHECK_PERIOD
    x, y, _ = robot.getPosition()

    new_index, d = nearest(x, y, index, int(0.05 / step), int(0.15 / step))
    if d < OFF_TRACK_DIST:
        delta = ((new_index - index + n // 2) % n - n // 2) * step
        progress += delta
        index = new_index
        off_since = None
    else:
        # the robot is not near the expected part of the track
        # (it left the line or took a shortcut)
        off_since = off_since if off_since is not None else t
        if t - off_since > OFF_TRACK_TIME:
            print(f"[JUDGE] t = {t:6.1f} s  Robot left the line. Attempt over.")
            print(f"[JUDGE] ===== RESULT: NOT FINISHED, progress {max(progress, 0) / length * 100:.0f}% =====")
            done = True
            continue

    if progress / length >= last_report and progress < length:
        print(f"[JUDGE] t = {t:6.1f} s  lap progress: {last_report * 100:.0f}%")
        last_report += 0.25

    if progress >= length:
        print(f"[JUDGE] ===== RESULT: LAP COMPLETED in {t:.2f} s =====")
        done = True
    elif t >= TIME_LIMIT:
        print(f"[JUDGE] ===== RESULT: TIME LIMIT, progress {max(progress, 0) / length * 100:.0f}% =====")
        done = True

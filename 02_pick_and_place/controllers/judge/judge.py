"""Pick and place judge. DO NOT MODIFY.

Every second checks how many cubes lie inside the crate and prints the result
in the Webots console. The evaluation ends when all cubes are in the crate or
when the time limit is reached.
"""
from controller import Supervisor

TIME_LIMIT = 120.0          # [s] of simulation time
CRATE_CENTER = (0.0, 0.5)   # crate centre (x, y) [m]
CRATE_HALF = 0.135          # half of the inner crate size [m]
CUBES = ["RED_CUBE", "GREEN_CUBE", "YELLOW_CUBE"]

judge = Supervisor()
timestep = int(judge.getBasicTimeStep())
cubes = {name: judge.getFromDef(name) for name in CUBES}


def in_crate(node):
    x, y, z = node.getPosition()
    return (abs(x - CRATE_CENTER[0]) < CRATE_HALF and
            abs(y - CRATE_CENTER[1]) < CRATE_HALF and
            z < 0.12)


print(f"[JUDGE] Start. Time limit: {TIME_LIMIT:.0f} s. Cubes to move: {len(CUBES)}.")
last = []
finished = False
next_check = 1.0
while judge.step(timestep) != -1:
    t = judge.getTime()
    if finished or t < next_check:
        continue
    next_check += 1.0
    current = [name for name, node in cubes.items() if in_crate(node)]
    if current != last:
        print(f"[JUDGE] t = {t:6.1f} s  cubes in the crate: {len(current)}/{len(CUBES)}  {current}")
        last = current
    if len(current) == len(CUBES) or t >= TIME_LIMIT:
        print(f"[JUDGE] ===== RESULT: {len(current)}/{len(CUBES)} cubes, time: {t:.1f} s =====")
        finished = True

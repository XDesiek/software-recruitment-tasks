"""Kinematics of the UR5e arm with the Robotiq 2F-85 gripper (pure Python).

You do not have to modify this file. It is used by pick_and_place.py:
    forward_kinematics(q)            -> (position, rotation matrix) of the gripper
    inverse_kinematics(x, y, z, ...) -> 6 joint angles reaching the given pose

Gripper (tool) frame, with its origin between the fingertips (grasp point):
    z axis - approach direction (out of the gripper, towards the object),
    x axis - direction in which the fingers close.
Orientation is given as roll, pitch, yaw [rad] (rotations about the world X, Y, Z
axes, applied in this order) relative to the default orientation, in which the
gripper points straight down and the fingers close along the world X axis.
So roll = pitch = 0 means "pointing down", and yaw turns the fingers around the
vertical axis.

All values are in the robot base frame (the same as the world frame in this
task): metres and radians.
"""
import math

# Joint origins (xyz, rotation about Y of the parent frame) and joint axes,
# taken from the UR5e model in Webots.
_JOINTS = [
    ((0.0, 0.0, 0.163), 0.0, (0, 0, 1)),        # shoulder_pan
    ((0.0, 0.138, 0.0), math.pi / 2, (0, 1, 0)),  # shoulder_lift
    ((0.0, -0.131, 0.425), 0.0, (0, 1, 0)),     # elbow
    ((0.0, 0.0, 0.392), math.pi / 2, (0, 1, 0)),  # wrist_1
    ((0.0, 0.127, 0.0), 0.0, (0, 0, 1)),        # wrist_2
    ((0.0, 0.0, 0.1), 0.0, (0, 1, 0)),          # wrist_3
]
TOOL_OFFSET = 0.245   # wrist_3 joint -> grasp point, along the wrist_3 Y axis [m]


# --- small matrix helpers ----------------------------------------------------
def _matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def _transpose(a):
    return [list(r) for r in zip(*a)]


def _rot(axis, angle):
    x, y, z = axis
    c, s, t = math.cos(angle), math.sin(angle), 1 - math.cos(angle)
    return [[t * x * x + c, t * x * y - s * z, t * x * z + s * y],
            [t * x * y + s * z, t * y * y + c, t * y * z - s * x],
            [t * x * z - s * y, t * y * z + s * x, t * z * z + c]]


def _transform(rot, pos):
    return [rot[0] + [pos[0]], rot[1] + [pos[1]], rot[2] + [pos[2]], [0, 0, 0, 1]]


# columns: tool x, y, z expressed in the wrist_3 frame
_TOOL_ROT = [[0, 1, 0], [0, 0, 1], [1, 0, 0]]
# default tool orientation (pointing down, fingers along world X)
_DEFAULT = [[1, 0, 0], [0, -1, 0], [0, 0, -1]]


def rpy_to_matrix(roll, pitch, yaw):
    """Tool orientation from roll/pitch/yaw relative to the default orientation."""
    r = _matmul(_rot((0, 0, 1), yaw), _matmul(_rot((0, 1, 0), pitch), _rot((1, 0, 0), roll)))
    return _matmul(r, _DEFAULT)


def forward_kinematics(q):
    """Return (position [x, y, z], 3x3 rotation matrix) of the gripper tool frame."""
    t = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    for (pos, ry, axis), angle in zip(_JOINTS, q):
        t = _matmul(t, _transform(_rot((0, 1, 0), ry), pos))
        t = _matmul(t, _transform(_rot(axis, angle), (0, 0, 0)))
    t = _matmul(t, _transform(_TOOL_ROT, (0, TOOL_OFFSET, 0)))
    return [t[0][3], t[1][3], t[2][3]], [row[:3] for row in t[:3]]


def _rotation_error(r_target, r_current):
    """Rotation vector of r_target * r_current^T."""
    r = _matmul(r_target, _transpose(r_current))
    cos_a = max(-1.0, min(1.0, (r[0][0] + r[1][1] + r[2][2] - 1) / 2))
    angle = math.acos(cos_a)
    v = [r[2][1] - r[1][2], r[0][2] - r[2][0], r[1][0] - r[0][1]]
    s = math.sin(angle)
    if s < 1e-6:
        if angle < 1e-6:
            return [0.0, 0.0, 0.0]
        # angle close to pi
        axis = [math.sqrt(max(0.0, (r[i][i] + 1) / 2)) for i in range(3)]
        return [a * angle for a in axis]
    return [vi * angle / (2 * s) for vi in v]


def _solve(a, b):
    """Solve a linear system a x = b (Gaussian elimination)."""
    n = len(b)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        m[c], m[p] = m[p], m[c]
        for r in range(n):
            if r != c:
                f = m[r][c] / m[c][c]
                m[r] = [m[r][k] - f * m[c][k] for k in range(n + 1)]
    return [m[i][n] / m[i][i] for i in range(n)]


class IKError(Exception):
    pass


def inverse_kinematics(x, y, z, roll=0.0, pitch=0.0, yaw=0.0, initial=None,
                       max_iterations=200, tolerance=1e-4):
    """Joint angles that put the grasp point at (x, y, z) with the given orientation.

    initial - joint angles to start the search from (e.g. the current ones);
    the result is usually the solution closest to it. Raises IKError if the
    pose cannot be reached.

    How it works (numerical inverse kinematics):
      1. compute where the gripper is now (forward kinematics),
      2. compute the 6D error: position difference + rotation difference,
      3. compute the Jacobian J - how the gripper pose changes when each joint
         moves a tiny bit (here: by finite differences),
      4. change the joints by dq = J^T (J J^T + lambda^2 I)^-1 * error
         ("damped least squares" - the damping keeps the steps sane near
         singular configurations),
      5. repeat until the error is small enough.
    """
    q = list(initial) if initial else [0.0, -1.57, 1.57, -1.57, -1.57, 0.0]
    target_p = [x, y, z]
    target_r = rpy_to_matrix(roll, pitch, yaw)
    damping = 0.01
    for _ in range(max_iterations):
        p, r = forward_kinematics(q)
        err = [tp - cp for tp, cp in zip(target_p, p)] + _rotation_error(target_r, r)
        if max(abs(e) for e in err[:3]) < tolerance and max(abs(e) for e in err[3:]) < 10 * tolerance:
            return [math.atan2(math.sin(a), math.cos(a)) for a in q]
        # numerical Jacobian (6x6)
        jac = [[0.0] * 6 for _ in range(6)]
        h = 1e-6
        for j in range(6):
            dq = q[:]
            dq[j] += h
            p2, r2 = forward_kinematics(dq)
            d = [(a - b) / h for a, b in zip(p2, p)] + [e / h for e in _rotation_error(r2, r)]
            for i in range(6):
                jac[i][j] = d[i]
        # damped least squares: dq = J^T (J J^T + lambda^2 I)^-1 err
        jjt = _matmul(jac, _transpose(jac))
        for i in range(6):
            jjt[i][i] += damping ** 2
        y_ = _solve(jjt, err)
        step = [sum(jac[i][j] * y_[i] for i in range(6)) for j in range(6)]
        biggest = max(abs(s) for s in step)
        if biggest > 0.3:
            step = [s * 0.3 / biggest for s in step]
        q = [a + s for a, s in zip(q, step)]
    raise IKError(f"Cannot reach x={x:.3f} y={y:.3f} z={z:.3f} "
                  f"roll={roll:.2f} pitch={pitch:.2f} yaw={yaw:.2f}")

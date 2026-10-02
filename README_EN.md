# Recruitment tasks: robotics in Webots

[Wersja polska](README.md)

Welcome to the recruitment to robotic section of Students' Space Association! We have prepared three programming tasks in the **Webots** robot simulator. **Choose one of them**. The tasks are independent, and each one has its own description, simulation worlds, program skeleton and a judge that measures the result automatically.

| Task | Robot | What it is about |
|---|---|---|
| [1. Line follower](01_line_follower/README_EN.md) | e-puck | following a line, control, two tracks |
| [2. Pick and place](02_pick_and_place/README_EN.md) | UR5e arm + gripper | manipulator control, kinematics |
| [3. Maze](03_maze/README_EN.md) | e-puck | distance sensors, odometry, two mazes |

Every task folder contains a description in `README.md` (Polish) and `README_EN.md` (English), and the same descriptions as PDF files.

## How to start

1. Install Webots R2025a and Python 3 (details below).
2. Download this repository: `git clone <repository address>` or *Code → Download ZIP*.
3. Choose a task and read its description.
4. Open a world from the `worlds` folder in Webots and start writing code in the `controllers` folder.

All tasks are written in Python. You do not need to know Webots beforehand: each task description contains everything you need to get started.

## What is Webots

Webots is a free, open-source robot simulator developed by Cyberbotics. It lets you build a virtual world with robots, sensors and objects, and control the robots with programs (called controllers) written in Python, C, C++ and other languages. The simulation includes physics: friction, masses, collisions and sensor noise, so a program that works in Webots behaves similarly on a real robot.

## Installation

1. Download **Webots R2025a** from https://cyberbotics.com or https://github.com/cyberbotics/webots/releases and install it like a regular application.
2. Install **Python 3** (https://www.python.org). On Windows, tick "Add Python to PATH" in the installer.
3. If Webots does not find Python by itself, set it in *Tools → Preferences → General → Python command*.
4. Keep the repository in a normal folder, **not** in the Webots installation folder or in a folder synchronised with OneDrive.
5. The first time a world is opened, Webots downloads the robot models from the internet, so you need a network connection.

Detailed instructions, a description of the interface and solutions to common problems are at the end of each task description.

## Rules

- Solve the task on your own. You may use the documentation, the internet and AI tools, but during the interview we will ask you to explain your code.
- Do not modify the judge or world files. We will run your controller in the original worlds.
- Submit the controller file, a short screen recording and a few sentences of description (details in the task description).

Good luck!

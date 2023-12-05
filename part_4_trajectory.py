from milling_robot_model import Robot
import numpy as np
import math

robot = Robot(10, 5)

def generate_circle(z_center=10, y_center=0):
    points = []
    for i in np.arange(0, 360, 5):
        points.append([-10, y_center+8*math.cos(math.radians(i)), z_center+8*math.sin(math.radians(i))])
    return points

# robot.trajectory([
#     [-10, 7, 7],
#     [-10, 7, 15],
#     [-10, -7, 15],
#     [-10, -7, 7],
#     [-10, 7, 7]
# ])

robot.trajectory(generate_circle())
from milling_robot_model import Robot

robot = Robot(10, 5)

robot.trajectory([
    [-10, 7, 9],
    [-10, 7, -9],
    [-10, -7, -9],
    [-10, -7, 9],
    [-10, 7, 9]
])
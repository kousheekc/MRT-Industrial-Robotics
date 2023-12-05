from milling_robot_model import Robot

robot = Robot(10, 5)

robot.plot_title("Inverse Kinematic Posture")

robot.IKM_draw(-5, 7, 9)
robot.IKM_draw(-1, 5, 12)
robot.IKM_draw(-10, -7, -15)
robot.IKM_draw(-8, -3, -5)

robot.show()

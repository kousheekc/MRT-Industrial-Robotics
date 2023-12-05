from milling_robot_model import Robot

robot = Robot(10, 5)

robot.plot_title("Forward Kinematic Posture")

robot.FKM_draw(-90,   0, 8)
robot.FKM_draw(-45, -20, 6)
robot.FKM_draw(  0, -40, 4)
robot.FKM_draw( 45, -60, 2)
robot.FKM_draw( 90, -80, 0)

robot.show()
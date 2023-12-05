from milling_robot_model import Robot

robot = Robot(10, 5)

robot.plot_title("Workspace")
robot.enveloppe([-90, 90, 10], [-90, 0, 10], [0, 10, 1])
robot.FKM_draw(0, 0, 0)

robot.show()
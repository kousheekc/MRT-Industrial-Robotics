from milling_robot_model import Robot

robot = Robot(10, 5)

robot.plot_title("Workspace")
robot.enveloppe_with_links([-90, 90, 20], [-90, 0, 15], [0, 10, 2])
# robot.FKM_draw(0, 0, 0)

robot.show()
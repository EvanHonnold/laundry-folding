import math
from pyquaternion import Quaternion
from controller import Controller
import numpy as np

print("Beginning run")

from laydown_planning.testing import *
# example_inputdisplay()
# example_laydown_path_display()
# example_laydown_config_display()
# testing_overall_planner()
# checking_collision_detection()

# NOTE: this is a script to demonstrate folds at various
# # angles, not to fold the shirt neatly.
# print("beginning script")
# c = Controller()
# c.perform_pickup(item_min_x=215, slide_dist=420)
# c.perform_setdown([400, -40], math.pi)
# c.perform_pickup(item_min_x=165, slide_dist=250, lift_height=150)
# c.perform_setdown([200, -440], math.pi * 1.625, lift_height=175,
#                   right_side_down=True, pull_distance=250)
# c.perform_pickup(item_min_x=375, slide_dist=240, lift_height=125)

# c = Controller()
# c.change_xyz(z=100)
# print(c.robot.get_cartesian())
# print(c.robot.get_joints())
# from constants import Q_NEUTRAL
# c.set_quaternion(Q_NEUTRAL)


testing_overall_planner()


print("Finished executing script.")
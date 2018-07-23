from helpers import get_robot_controller, interpolate_movement, change_coords, direction, apply_quaternion
import math
from pyquaternion import Quaternion
import numpy as np


class Controller():

    def perform_setdown(self, dest_xy, angle,
                        pull_distance=425, lift_height=220, right_side_down=False):

        TABLE_Z = 200
        dest_xyz = np.array(dest_xy + [TABLE_Z])
        start_xyz = self.generate_laydown_coords(
            dest_xyz, angle, lift_height, right_side_down)
        print("Performing setdown: moving to setdown start: " + str(start_xyz))
        self.set_xyz(start_xyz)

        robot_angle = angle + math.pi * 0.25  # because 0 for the robot is 45 deg off
        q_zero = Quaternion(
            axis=[1, 0, 0],
            angle=math.pi)
        q_rotate = Quaternion(
            axis=[0, 0, 1],
            angle=robot_angle)
        q_target = apply_quaternion(q_zero, q_rotate)
        print("Turning ruler in appropriate direction: " + str(q_target))
        self.set_quaternion(q_target)

        print("Performing laydown -- interpolation towards " + str(dest_xyz))
        self.set_xyz(dest_xyz, 20)

        pull_angle = angle - math.pi/2
        pull_dir = direction(pull_angle)
        pull_dir = np.append(pull_dir, 0)  # no z change
        xyz = dest_xyz + pull_dir * pull_distance
        print("Pulling out the ruler: going to " + str(xyz))
        self.set_xyz(xyz, int(pull_distance / 10))
        self.change_xyz(z=100)  # avoid problems on next pickup

    # NOTE: see notebook for explanations of how to provide
    # values for 'xy' and 'angle'
    # TODO: deprecate this function, using the laydown_planner one instead
    def generate_laydown_coords(self, dest_xyz, angle,
                                height=250, right_side_down=False):
        assert isinstance(dest_xyz, np.ndarray)
        assert len(dest_xyz) == 3
        assert height > 0
        start_dir = direction(angle)
        if right_side_down:
            start_dir = start_dir * -1
        start_point_dir = np.append(start_dir, 0.75)
        return dest_xyz + start_point_dir * height * (1/0.75)

    def perform_pickup(self, item_min_x=60,
                       slide_dist=575, lift_height=250):

        assert item_min_x > 60  # item can't extend past table
        q_level = (
            Quaternion(axis=[1, 0, 0], angle=math.pi) *
            Quaternion(axis=[0, 0, 1], angle=math.pi / 4))
        self.set_xyz([200, -246, 300])
        self.set_quaternion(q_level)
        RULER_LENGTH = 475  # TODO import this number from constants.py instead
        self.set_xyz([item_min_x - RULER_LENGTH - 10, -246, 207],
                     10)  # prepare to enter slot
        self.apply_quaternion(
            Quaternion(axis=[0, 1, 0], angle=math.pi/12))
        self.set_xyz([item_min_x - RULER_LENGTH +
                      slide_dist, -246, 207], 20)   # slide under
        self.set_quaternion(q_level)  # begin pickup
        self.change_xyz(z=lift_height)

    # Work in Progress:
    def perform_fold__a(self):

        # ruler should point away from window parallel to gap
        self.set_joints([-119.92, 64.97, -47.45, 0.0, 72.48, 105.08])
        q_level = (Quaternion(axis=[1, 0, 0], angle=math.pi)
                   * Quaternion(axis=[0, 0, 1], angle=math.pi / 4))  # TODO replace this with the Q defined in "constants"
        self.set_quaternion(q_level)

        self.set_xyz([-421, -246, 207])   # prepare to slide under
        self.apply_quaternion(Quaternion(axis=[0, 1, 0], angle=math.pi/12))

        self.set_xyz([150, -246, 207], 20)   # slide under
        self.set_quaternion(q_level)  # begin pickup

        # NOTE: below here is hard-coded stuff for small shirt
        self.set_xyz([150, -246, 450])  # raise
        self.apply_quaternion(Quaternion(axis=[0, 0, 1], angle=-math.pi/2))
        self.set_xyz([150, -100, 450])  # prepare liedown
        # self.set_quaternion(Quaternion(scalar=0.353, vector=[-0.354, 0.853, -0.147])) # twist along ruler

        self.set_xyz([350, -100, 250])
        self.set_xyz([393, -100, 207], interpolate_steps=10)  # lie-down

        # [-3.0000000e+02  3.6739404e-14  2.1300000e+02]

        print("got here")

    def __init__(self):
        (robot, succeeded) = get_robot_controller()
        if not succeeded:
            raise Exception("Connection to robot failed!")
        else:
            self.robot = robot
            self.set_speed(0.5)
            print("Connection to robot successful.")
            c = self.robot.get_cartesian()
            self.xyz = np.array(c[0])
            self.quaternion = Quaternion(c[1])

    def set_speed(self, speed_proportion):
        assert 0 <= speed_proportion <= 1
        default = np.array([100, 50, 50, 50])
        new_speeds = default * speed_proportion
        self.robot.set_speed(new_speeds)

    def set_quaternion(self, quaternion):
        assert quaternion.__class__.__name__ == 'Quaternion'
        q_arr = [quaternion.scalar] + quaternion.vector.tolist()
        self.robot.set_cartesian([self.xyz, q_arr])
        self.quaternion = quaternion

    def set_xyz(self, xyz, interpolate_steps: int = 1):
        if not isinstance(xyz, np.ndarray):
            xyz = np.array(xyz)
        q_arr = [self.quaternion.scalar] + self.quaternion.vector.tolist()
        if interpolate_steps < 2:
            self.robot.set_cartesian([xyz, q_arr])
        else:
            interpolate_movement(self.robot, self.xyz, xyz,
                                 interpolate_steps, q_arr)
        self.xyz = xyz

    def change_xyz(self, x=0, y=0, z=0, interpolate_steps=1):
        change = np.array([x, y, z])
        self.set_xyz(self.xyz + change, interpolate_steps)

    # NOTE: takes a rotation given in terms of the unadjusted (global) axes and
    # performs the necessary computation to apply that rotation to the current
    # position (which requires rotations to use adjusted axes):
    def apply_quaternion(self, quaternion):
        assert quaternion.__class__.__name__ == 'Quaternion'
        q_new = apply_quaternion(self.quaternion, quaternion)
        self.set_quaternion(q_new)

    def set_joints(self, joint_angles):
        self.robot.set_joints(joint_angles)
        c = self.robot.get_cartesian()
        self.xyz = np.array(c[0])
        self.quaternion = Quaternion(c[1])

    def move_test(self):
        self.set_speed(0.25)
        # point the effector down towards table
        q1 = Quaternion(axis=[1, 0, 0], angle=math.pi)
        # test a small rotation around z
        q2 = Quaternion(axis=[0, 0, 1], angle=math.pi / 4)
        q3 = q1 * q2
        q_arr = [q3.scalar] + q3.vector.tolist()

        # self.set_quaternion(q1)
        self.set_quaternion(q3)

        vec = np.array([0, 1, 0])
        rot_vec = q3.rotate(vec)
        q4 = Quaternion(axis=rot_vec, angle=-1 * math.pi / 4)
        q5 = q3 * q4
        self.set_quaternion(q5)

        print("test complete")

# SIMPLE SHIRT LIFT SCRIPT


# robot arm behind table with ruler pointed to window (safe neutral position):
b1 = [[-275.36, -272.72, 331.86], [0.045, 0.868, -0.492, 0.051]]
b11 = [[-375, -272, 200], [0.0, 0.919, 0.394, 0.0]]

# ruler prepared to slide under the shirt:
b2 = [[-275.4, -272.7, 131.9], [0.0, 0.919, 0.394, 0.0]]
# ruler after sliding under the shirt:
b3 = [[102.59, -272.69, 131.9], [0, 0.919, 0.394, 0]]
# after lifting the shirt up:
b4 = [[124.6, -272.71, 609.37], [0, 0.919, 0.394, 0]]
# preparing to lie shirt down:
b5 = [[-25.4, -422.7, 609.4], [0.0, -0.985, -0.17, 0.0]]
b6 = [[-25.4, -422.7, 550], [0.0, -0.985, -0.17, 0.0]]
# example of quaternions with ruler rotated almost 90 deg: [0.005, 0.71, 0.004, 0.704]


# OTHER MISC CODE
#     # interpolate_movement(robot, b6[0], [-25.4 + 400, -422.7 + 400, 550 - 300], 10, b6[1])
#     # change_coords([400, 400, -300], robot)
#     # change_coords([-])

#     # change_coords([0, 0, 75], robot)
#     # + 150 x, - 50y
#     # robot.set_cartesian([[-275.36, -272.72, 200], [0.0, 0.919, 0.394, 0.0]])
#     # robot.set_joints([-5.9, 11.17, 5.1, 0.0, 73.74, 275])
#     # robot.set_cartesian([robot.get_cartesian()[0], [0, 0, 0, 1]])

#     print(robot.get_cartesian())
#     # print(robot.get_joints())

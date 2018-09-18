from math import sin, pi
from typing import List
from constants import ROBOT_BASE
from laydown_planning.laydown_config import LaydownConfiguration
from laydown_planning.laydown_path import LaydownPath
from laydown_planning.fold_instructions import FoldInstructions


def plan(fold_instructions: FoldInstructions)->List[LaydownConfiguration]:
    assert fold_instructions.__class__.__name__ == 'FoldInstructions'
    angle = fold_instructions.fold_angle

    # y-distance between the effector and the gap:
    ydist = sin(angle) * fold_instructions.intercept

    # determine four configs (see notebook for details)
    ruler_a = angle
    ruler_b = 2 * pi - angle
    ruler_c = pi - angle
    ruler_d = pi + angle

    c_a = LaydownConfiguration(-ydist, ruler_a, ruler_a + pi/2)
    c_b = LaydownConfiguration(ydist, ruler_b, ruler_b - pi/2)
    c_c = LaydownConfiguration(-ydist, ruler_c, ruler_c - pi/2)
    c_d = LaydownConfiguration(ydist, ruler_d, ruler_d + pi/2)

    return [c_a, c_b, c_c, c_d]


def choose_best(paths):
    """ Test each of the 4 paths with different y-translations;
        returns the best one, and assigns it the appropriate y-values.

         """
    for m_path in paths:

        # TODO iterate over various Y-translations
        for x in range(-400, 400, 20):
            m_path.shift_x(x)

            # check for out of reach, check for collisions w. self (arm)
            # if within_reach(m_path) and not collisions(m_path):
            #     value = assign_value(m_path)

            m_path.shift_x(-x)

        # TODO compare distances of workable laydown paths
        print("tested path")

    print("function incomplete")


def within_reach(laydown_path):

    print("not implemented")


def collisions(laydown_path: LaydownPath)->bool:
    for polygon in laydown_path.get_hitboxes():
        if polygon.intersection(ROBOT_BASE).area > 0:
            return True
    return False


def assign_value(laydown_path):
    """ Given a laydown option, which we assume is valid,
        assign a value to represent desirability (e.g., nearness
        to the base of the arm). Higher value -> better path. """
    print("not implemented")

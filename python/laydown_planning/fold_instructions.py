from math import pi
from constants import RULER_LENGTH


class FoldInstructions():
    """ Represents the data expected from the fold planner;
        defines a single fold.

        Assume the effector is at the origin and the ruler
        is pointing out along the positive x-axis. """

    def __init__(self, intercept, fold_angle):
        """
            intercept: the distance from the effector to the point
            where the fold line intersects the ruler
            angle: the angle of the fold line relative to the ruler
        """
        assert 0 <= intercept <= RULER_LENGTH
        assert 0 <= fold_angle <= pi

        self.intercept = intercept
        self.fold_angle = fold_angle

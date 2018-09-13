from math import pi

from numpy import append, array

from helpers import direction, hitbox_of_path
from constants import RULER_LENGTH


class LaydownPath():

    def __init__(self, laydown_config, height, pull_dist, destination_x=0):
        """ Takes the target laydown coordinates and determines
            the start and pullout locations.
            * height: how high the garment must be lifted to be off the boards
            * pull_dist: how far the ruler must be pulled to get it out of the garment
        """
        assert laydown_config.__class__.__name__ == 'LaydownConfiguration'
        LAYDOWN_SLOPE = 0.75

        dest_xyz = array([destination_x, laydown_config.y, 0])
        start_xyz_direction = append(
            direction(laydown_config.garment_direction),
            LAYDOWN_SLOPE)
        start_xyz = dest_xyz + start_xyz_direction * (height / LAYDOWN_SLOPE)

        pull_angle = laydown_config.ruler_direction + pi
        pull_direction = append(direction(pull_angle), 0)
        pull_change = pull_direction * pull_dist

        self.start_xyz = start_xyz
        self.dest_xyz = dest_xyz
        self.pullout_xyz = dest_xyz + pull_change
        self.ruler_angle = laydown_config.ruler_direction

    def shift_x(self, amount):
        translation = array([amount, 0, 0])
        self.start_xyz += translation
        self.dest_xyz += translation
        self.pullout_xyz += translation

    def get_hitboxes(self):
        """ Gets the hitboxes in xy-space. Just considers the end effector
            (modeled as a square) and the ruler. Returns a list of lists, 
            where each sublist contains the points of a polygon. """

        start = self.start_xyz[0:2]
        mid = self.dest_xyz[0:2]
        end = self.pullout_xyz[0:2]
        angle = self.ruler_angle

        # First two hitboxes are around the path traveled by the
        # effector (one for each stage of the movement).
        box1 = hitbox_of_path(start, mid, 40)
        box2 = hitbox_of_path(mid, end, 40)

        # This hitbox is the area swept by the ruler:
        rulertip_start = start + direction(angle) * RULER_LENGTH
        rulertip_mid = mid + direction(angle) * RULER_LENGTH
        box3 = [start, rulertip_start, rulertip_mid, mid]

        return [box1, box2, box3]

    def __str__(self):
        sb = []
        for key in self.__dict__:
            sb.append("{key}='{value}'".format(
                key=key, value=self.__dict__[key]))
        return ', '.join(sb)

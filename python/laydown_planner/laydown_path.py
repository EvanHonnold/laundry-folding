from math import pi

from numpy import append, array

from helpers import direction


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

    def __str__(self):
        sb = []
        for key in self.__dict__:
            sb.append("{key}='{value}'".format(
                key=key, value=self.__dict__[key]))
        return ', '.join(sb)

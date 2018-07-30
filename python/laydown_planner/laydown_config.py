from helpers import fix_angle


class LaydownConfiguration():

    def __init__(self, y, ruler_direction, garment_direction):
        """ y:  the y-change to get from the end effector location
                to the gap between the boards
            ruler_direction:  an angle that represents which way the ruler
                is pointing
            garment_direction: an angle that represents which way the garment
                should be pointing after the laydown (should be perpendicular
                to ruler_direction)
        """
        self.y = y
        self.ruler_direction = fix_angle(ruler_direction)
        self.garment_direction = fix_angle(garment_direction)

    def __str__(self):
        sb = []
        for key in self.__dict__:
            sb.append("{key}='{value}'".format(
                key=key, value=self.__dict__[key]))
        return ', '.join(sb)

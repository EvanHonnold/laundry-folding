from math import pi

from numpy import array
from pyquaternion import Quaternion

# distance between the tip of the ruler and the center
# of the effector (NOT the other end of the ruler):
RULER_LENGTH = 475

LEFT = pi
RIGHT = 0

# Quaternion: effector faces downward, ruler points in the +x direction
Q_NEUTRAL = Quaternion(axis=[1, 0, 0], angle=pi) * \
    Quaternion(axis=[0, 0, 1], angle=pi / 4)

# how far away the robot can reach from (0, 0, 200)
ROBOT_REACH = 550

# the xy-location of the intersection between the big gap
# and the line where the small plates touch the big ones
TABLE_CENTER = (237, -250)

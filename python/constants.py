from math import pi

from pyquaternion import Quaternion
from shapely.geometry import Point

# distance between the tip of the ruler and the center
# of the effector (NOT the other end of the ruler):
RULER_LENGTH = 475

LEFT = pi
RIGHT = 0

# Quaternion: effector faces downward, ruler points in the +x direction
Q_NEUTRAL = Quaternion(axis=[1, 0, 0], angle=pi) * \
    Quaternion(axis=[0, 0, 1], angle=pi / 4)

ROBOT_BASE_CENTER = [0, 0]
ROBOT_BASE_RADIUS = 100
ROBOT_BASE = Point(ROBOT_BASE_CENTER).buffer(
    ROBOT_BASE_RADIUS)  # circle is discretized into polygon

# how far away the robot can reach from (0, 0, 200)
ROBOT_REACH = 550

# the xy-location of the intersection between the big gap
# and the line where the small plates touch the big ones
TABLE_CENTER = (237, -250)

GAP_Y_MIN = -248
GAP_Y_MAX = -244
CROSSLINE_X = 237


class Rect():
    def __init__(self, xmin, xmax, ymin, ymax):
        self.x_min = xmin
        self.x_max = xmax
        self.y_min = ymin
        self.y_max = ymax


LOWER_BIG_PLATE = Rect(CROSSLINE_X,
                       CROSSLINE_X + 18 * 25.4,
                       GAP_Y_MIN - 18 * 25.4,
                       GAP_Y_MIN)

UPPER_BIG_PLATE = Rect(CROSSLINE_X,
                       CROSSLINE_X + 18 * 25.4,
                       GAP_Y_MAX,
                       GAP_Y_MAX + 18 * 25.4,)

LOWER_MEDIUM_PLATE = Rect(CROSSLINE_X - 12 * 25.4,
                          CROSSLINE_X,
                          GAP_Y_MIN - 12 * 25.4,
                          GAP_Y_MIN)

UPPER_SMALL_PLATE = Rect(CROSSLINE_X - 6 * 25.4,
                         CROSSLINE_X,
                         GAP_Y_MAX,
                         GAP_Y_MAX + 6 * 25.4)

TABLE_PLATES = [LOWER_BIG_PLATE, UPPER_BIG_PLATE,
                LOWER_MEDIUM_PLATE, UPPER_SMALL_PLATE]

import cmath
import errno
import math
import os
import socket
import sys
from math import pi, atan2
from pprint import pprint

from numpy import array
from pyquaternion import Quaternion
import abb

from shapely.geometry import Polygon


def get_robot_controller():
    """ returns a tuple: (robot controller reference, 
    boolean success indicator) """

    # abb = imp.load_source("abb", "./abb/packages/abb_communications/abb.py")
    try:
        robot = abb.Robot(ip='192.168.125.1')
        return (robot, True)
    except socket.error as err:
        print(err)
        if isinstance(err, socket.timeout):
            print("Last time it was caught, this error meant the arm's USB cable"
                  " was not plugged in to this computer.")
        elif err.errno == errno.ECONNREFUSED:
            print("Last time it was caught, this error meant the USB cable is plugged "
                  "in, but the remote control program was not yet running on the robot's "
                  "computer. Use the flex pendant to run the program.")
        else:
            print("We caught a new sort of socket error - raising it again")
            raise err
        return (None, False)


def apply_quaternion(base, adjustment):
    """ applies adjustment quaternion (given in global 
        coord system) to the base quaternion """
    assert base.__class__.__name__ == 'Quaternion'
    assert adjustment.__class__.__name__ == 'Quaternion'
    axis = adjustment.get_axis()
    inv = base.inverse
    axis_adj = inv.rotate(axis)
    q_adj = Quaternion(axis=axis_adj, angle=adjustment.angle)
    return base * q_adj

# start, end: array with [x, y, z]
# steps: number of movements to divide the path into
# quaternions: specify the effector angle (we assume this
#   shouldn't change throughout the path)


def interpolate_movement(robot, start, end, steps, quaternions):
    x_stepsize = (end[0] - start[0]) / steps
    y_stepsize = (end[1] - start[1]) / steps
    z_stepsize = (end[2] - start[2]) / steps
    print("Beginning " + str(steps) + "-step interpolation")
    print("Interpolation steps completed: ", end='', flush=True)
    for i in range(0, steps + 1):
        print(str(i) + " ", end='', flush=True)
        coords = [start[0] + x_stepsize * i, start[1] +
                  y_stepsize * i, start[2] + z_stepsize * i]
        robot.set_cartesian([coords, quaternions])
    print("")

# NOTE: deprecated
# "change" should be a three-element list consisting of the desired
# adjustment to the x, y, and z coordinates of the effector.
# Note: the orientation (quaternions) of the effector remains the same


def change_coords(change, robot):
    cartesian = robot.get_cartesian()
    coords = cartesian[0]
    newcartesian = [[coords[0] + change[0], coords[1] +
                     change[1], coords[2] + change[2]], cartesian[1]]
    robot.set_cartesian(newcartesian)


# def interpolate_movement_improved():
# TODO  implement interpolation that operates on the quaternions
#       as well as the cartesian coordinates

# returns unit vector (x-y plane) encoded as numpy array:
def direction(angle_radians):
    x_component = math.cos(angle_radians)
    y_component = math.sin(angle_radians)
    return array([x_component, y_component])


def vector_to_angle(vector):
    angle = atan2(vector[1], vector[0])
    return fix_angle(angle)


def within_range(value, a, b):
    """ Checks if value is within the endpoints 'a' and 'b'. Convenience
        method for when you don't know which endpoint will be bigger. """

    if a > b:
        return b <= value <= a
    if a < b:
        return a <= value <= b
    return value == a

# ensures the value is in the range [0, 2pi]


def fix_angle(value_radians):
    while (value_radians < 0):
        value_radians += pi * 2
    while (value_radians > pi * 2):
        value_radians -= pi * 2
    return value_radians


def rotate(points, angle):
    """ rotates the list of points around the origin """
    c_angle = cmath.exp(angle * 1j)
    newpoints = []
    for x, y in points:
        v = c_angle * complex(x, y)
        newpoints.append((v.real, v.imag))
    return newpoints


def translate(points, dx, dy):
    newpoints = []
    for p in points:
        newpoints.append((p[0] + dx, p[1] + dy))
    return newpoints


def hitbox_of_path(start, end, buffer)->Polygon:
    """ Given a start and end point, generate a rough polygonal
        hitbox around the path between. 

        Returns a list of 2d points. """

    away = vector_to_angle(start - end)  # away from direction of movement

    # three points around the start...
    s1 = start + direction(away - pi/2) * buffer
    s2 = start + direction(away) * buffer
    s3 = start + direction(away + pi/2) * buffer

    # ... and three points around the end.
    e1 = end + direction(away + pi/2) * buffer
    e2 = end + direction(away + pi) * buffer
    e3 = end + direction(away - pi/2) * buffer

    return Polygon([s1, s2, s3, e1, e2, e3])

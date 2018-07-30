from tkinter import Frame, Canvas
from constants import RULER_LENGTH
from helpers import direction, rotate, translate
from numpy import array
from math import pi
import cmath
from laydown_planner.laydown_config import LaydownConfiguration

SCALE = 0.4
size = 300  # of the window
center = array([size/2, size/2])


class LaydownConfigDisplay(Frame):
    def __init__(self, parent=None):
        color = "#%02x%02x%02x" % (224, 224, 224)  # gray 300
        Frame.__init__(self, parent, width=size, height=size)
        self.pack_propagate(False)
        canvas = Canvas(self, width=size, height=size,
                        bg=color, highlightthickness=0)
        self.canvas = canvas
        canvas.pack()

    def show(self, config: LaydownConfiguration):
        assert config.__class__.__name__ == "LaydownConfiguration"

        # vector represents the coordinate change from
        # the effector to the ruler's tip:
        v = direction(config.ruler_direction) * RULER_LENGTH * SCALE

        # walk backwards half of v's distance from the center
        # to get to the point where we draw the effector:
        e = center - v / 2
        line_end = e + v
        print(line_end)

        # draw the effector + ruler:
        line_end[1] = size - line_end[1]
        self.circle([e[0], size-e[1]], 10 * SCALE, "black")
        self.canvas.create_line(
            e[0], size-e[1], line_end[0], line_end[1], width=3)

        # draw the foldline:
        y = size - (e[1] - config.y * SCALE)
        self.canvas.create_line(0, y, size, y)
        print(y)

    def circle(self, center_coords, radius, fill=''):
        x0 = center_coords[0] - radius
        y0 = center_coords[1] - radius
        x1 = center_coords[0] + radius
        y1 = center_coords[1] + radius
        self.canvas.create_oval(x0, y0, x1, y1, fill=fill)

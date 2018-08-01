from tkinter import Frame, Canvas
from numpy import array

from constants import RULER_LENGTH
from helpers import direction
from laydown_planning.laydown_config import LaydownConfiguration

SCALE = 0.4
size = 500  # of the window
center = array([size/2, size/2])

# Class for visualizing LaydownConfig objects.


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

        def line(start, end, width=1):
            self.canvas.create_line(
                start[0], start[1], end[0], end[1], width=width)

        # draw the table gap
        line([0, size/2 - 1], [size, size/2 - 1])
        line([0, size/2 + 1], [size, size/2 + 1])

        # vector represents the coordinate change from
        # the effector to the ruler's tip:
        v = direction(config.ruler_direction) * RULER_LENGTH * SCALE
        effector = center + [0, config.y]

        ruler_end = effector + v

        garment_vec = direction(config.garment_direction) * 200 * SCALE
        corner1 = ruler_end + garment_vec
        corner2 = effector + garment_vec
        self.canvas.create_polygon(
            *effector, *ruler_end, *corner1, *corner2, fill='gray')

        self.circle(effector, 10 * SCALE, "black")
        line(effector, ruler_end, width=3)

    def circle(self, center_coords, radius, fill=''):
        x0 = center_coords[0] - radius
        y0 = center_coords[1] - radius
        x1 = center_coords[0] + radius
        y1 = center_coords[1] + radius
        self.canvas.create_oval(x0, y0, x1, y1, fill=fill)

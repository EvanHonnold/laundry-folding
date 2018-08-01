from tkinter import Frame, Canvas
from numpy import array

from constants import RULER_LENGTH, TABLE_PLATES, Rect, ROBOT_BASE_CENTER, ROBOT_BASE_RADIUS
from helpers import direction
from laydown_planning.laydown_path import LaydownPath

# Class for visualizing LaydownPath objects.


class LaydownPathDisplay(Frame):

    SCALE = 0.75

    def __init__(self, parent=None):

        window_width = 700
        window_height = 800
        self.translation = array([100, 800])  # translation applied

        color = "#%02x%02x%02x" % (224, 224, 224)  # gray 300
        Frame.__init__(self, parent, width=window_width, height=window_height)
        self.pack_propagate(False)
        canvas = Canvas(self, width=window_width, height=window_height,
                        bg=color, highlightthickness=0)
        self.canvas = canvas
        canvas.pack()

    def show(self, path: LaydownPath):

        for r in TABLE_PLATES:
            self.rectangle(r)
        self.circle(ROBOT_BASE_CENTER, ROBOT_BASE_RADIUS *
                    self.SCALE, fill="black")

        print("not implemented")

    def circle(self, center_coords, radius, fill=''):
        x0 = (center_coords[0] - radius + self.translation[0]) * self.SCALE
        y0 = (center_coords[1] - radius + self.translation[1]) * self.SCALE
        x1 = (center_coords[0] + radius + self.translation[0]) * self.SCALE
        y1 = (center_coords[1] + radius + self.translation[1]) * self.SCALE
        self.canvas.create_oval(x0, y0, x1, y1, fill=fill)

    def rectangle(self, r: Rect):
        topleft = array([r.x_min, r.y_max])
        topright = array([r.x_max, r.y_max])
        btmright = array([r.x_max, r.y_min])
        btmleft = array([r.x_min, r.y_min])
        pts = [topleft, topright, btmright, btmleft]
        values = []
        for p in pts:
            values.append(p[0] + self.translation[0])
            values.append(p[1] + self.translation[1])
        values = [v * self.SCALE for v in values]

        self.canvas.create_polygon(*values, fill="gray")

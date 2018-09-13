from tkinter import Frame, Canvas
from numpy import array

from constants import RULER_LENGTH, TABLE_PLATES, Rect, ROBOT_BASE_CENTER, ROBOT_BASE_RADIUS
from helpers import direction
from laydown_planning.laydown_path import LaydownPath

# Class for visualizing LaydownPath objects.


class LaydownPathDisplay(Frame):

    SCALE = 0.5

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

    # NOTE: no scaling and translating should occur in this function --
    #       it should all be in the helper functions below
    def show(self, path: LaydownPath):

        # draw the background:
        for r in TABLE_PLATES:
            self.rectangle(r)
        self.circle(ROBOT_BASE_CENTER, ROBOT_BASE_RADIUS, fill="black")

        # draw the collision boxes of the ruler and arm
        # TODO finish here
        box_list = path.get_hitboxes()
        for box in box_list:
            self.polygon(box)

        # draw the ruler positions:
        def ruler(start, angle):
            self.circle(start, 10, "black")  # the effector
            self.line(start, start + direction(angle) * RULER_LENGTH, width=5)
        ruler(path.start_xyz[0:2], path.ruler_angle)
        ruler(path.dest_xyz[0:2], path.ruler_angle)
        ruler(path.pullout_xyz[0:2], path.ruler_angle)

        print("not implemented")

    # helper functions -- all scaling and translating should be done here

    def circle(self, center_coords, radius, fill=''):
        center_coords = center_coords + self.translation
        center_coords = center_coords * self.SCALE
        radius = radius * self.SCALE

        x0 = center_coords[0] - radius
        y0 = center_coords[1] - radius
        x1 = center_coords[0] + radius
        y1 = center_coords[1] + radius
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

        self.canvas.create_polygon(*values, fill="darkgray")

    def line(self, start, end, width=1):
        start = (start + self.translation) * self.SCALE
        end = (end + self.translation) * self.SCALE
        width = width * self.SCALE
        self.canvas.create_line(
            start[0], start[1], end[0], end[1], width=width)

    def polygon(self, points: list):
        # translate
        points = [point + self.translation for point in points]
        # scale
        points = [point * self.SCALE for point in points]
        # unpack the array
        points_unpacked = []
        for point in points:
            points_unpacked.append(point[0])
            points_unpacked.append(point[1])

        self.canvas.create_polygon(points_unpacked, fill="gray")

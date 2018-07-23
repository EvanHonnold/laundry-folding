from constants import LEFT, RIGHT, RULER_LENGTH
from Tkinter import Frame, Canvas
from helpers import direction
from numpy import array

class InputDisplay(Frame):
    def __init__(self, parent=None):
        self.BUFFER = 75
        width = self.BUFFER * 2 + RULER_LENGTH
        height = self.BUFFER * 4
        self.width = width
        self.height = height

        color = "#%02x%02x%02x" % (144,164,174) # blue-gray 300
        Frame.__init__(self, parent, width=width, height=height)
        self.pack_propagate(False)
        canvas = Canvas(self, width=width, height=height, bg=color, highlightthickness=0)
        self.canvas = canvas
        canvas.pack()

        ruler_points = self.translate(
            [(0, 3), (0, -3), (RULER_LENGTH, -3), (RULER_LENGTH, 3)], 
            self.BUFFER, self.BUFFER * 3)
        self.polygon(ruler_points, 
            "#%02x%02x%02x" % (96,125,139)) # blue-gray 500

        cwidth = RULER_LENGTH - 70
        cheight = self.BUFFER * 2
        cloth = self.polygon([(cwidth, 0), (0, 0), (0, -cheight), (cwidth, -cheight)],
            "#%02x%02x%02x" % (176,190,197)) #blue-gray 200
        self.move(cloth, self.BUFFER + 35, self.BUFFER * 3 + 3)       

    def show(self, fold_instr):
        assert fold_instr.__class__.__name__ == "FoldInstructions"
        effector_points = [(-15, -3), (15, -3), (15, 27), (-15, 27)]
        intercept_point = None
        # if (fold_instr.ruler_angle == RIGHT):
        effector_points = self.translate(effector_points, 
            self.BUFFER, self.BUFFER * 3)
        intercept_point = array([self.BUFFER + fold_instr.intercept, self.BUFFER])
        # elif (fold_instr.ruler_angle == LEFT):
        #     effector_points = self.translate(effector_points, 
        #         self.BUFFER + RULER_LENGTH, self.BUFFER * 3)
        #     intercept_point = array([self.BUFFER + RULER_LENGTH + fold_instr.intercept, self.BUFFER])

        p = self.polygon(effector_points, 
            "#%02x%02x%02x" % (84,110,122)) # blue-gray 600

        # display the fold line
        d = direction(fold_instr.fold_angle)
        d[1] = d[1] * -1 # fix y
        upper_endpoint = intercept_point + d * 1000
        lower_endpoint = intercept_point - d * 1000
        linecolor = "#%02x%02x%02x" % (13,71,161)
        self.canvas.create_line(upper_endpoint[0], upper_endpoint[1], 
            intercept_point[0], intercept_point[1], width = 3, fill = linecolor)
        self.canvas.create_line(lower_endpoint[0], lower_endpoint[1], 
            intercept_point[0], intercept_point[1], width = 3, fill = linecolor)

    def translate(self, points, dx, dy):
        newpoints = []
        for p in points:
            newpoints.append((p[0]+ dx, p[1] + dy))
        return newpoints

    def move_poly(self, polygon, new_points):
        pts = []
        for p in new_points:
            pts.append(p[0])
            pts.append(self.height - p[1]) # to fix y direction
        self.canvas.coords(polygon, *pts)

    def polygon(self, points, fill=None):
        p = self.canvas.create_polygon(points, fill=fill)
        self.move_poly(p, points)
        return p

    def move(self, polygon, x, y):
        self.canvas.move(polygon, x, -y)


    

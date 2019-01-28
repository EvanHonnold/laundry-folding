from tkinter import Frame, Canvas
from numpy import array
from shapely.geometry import Polygon
import subprocess
import os
import numpy as np

# Usage:
# 
#   c = SmartCanvas()
#
#   # add features, for example:
#   c.line([0, 0], [1, 1]) 
#
#   c.show()


class SmartCanvas(Frame):

    def __init__(self, width=500, height=500, background=(224, 224, 224)):

        self.parent = Frame(None)
        self.parent.pack()
        self.width = width
        self.height = height

        Frame.__init__(self, self.parent,
            width=self.width,
            height=self.height)

        self.pack_propagate(False) # not sure why necessary
        self.canvas = Canvas(self, width=self.width, height=self.height,
            bg="#%02x%02x%02x" % background,  
            highlightthickness=0)
        self.canvas.pack()

        self.transforms = []

        # start off by fixing things so the origin is in 
        # the bottom left of screen, and +y is up:
        self.translation(0, self.height)
        self.scaling(1, -1)

    def translation(self, x, y):
        self.transforms.insert(0, ("translation", array([x, y]).astype(float)))

    def scaling(self, x, y):
        self.transforms.insert(0, ("scaling", array([x, y])))

    def circle(self, center, radius, fill='black'):
        x0 = center[0] - radius
        y0 = center[1] - radius
        x1 = center[0] + radius
        y1 = center[1] + radius

        p1 = self._fix_point([x0, y0])
        p2 = self._fix_point([x1, y1])
        
        self.canvas.create_oval(p1[0], p1[1], p2[0], p2[1], fill=fill)

    def line(self, start, end, width=1):
        start = self._fix_point(start)
        end = self._fix_point(end)
        
        self.canvas.create_line(*start, *end, width=width)

    def polygon(self, polygon:Polygon, fill="black"):
        x_coords, y_coords = polygon.exterior.coords.xy
        fixed_coords = []
        for i in range(len(x_coords)):
            x = x_coords[i]
            y = y_coords[i]
            fixed = self._fix_point(array([x, y]))
            fixed_coords.append(fixed[0])
            fixed_coords.append(fixed[1])
        self.canvas.create_polygon(*fixed_coords, fill=fill)

    def show(self):
        self.pack()
        self.parent.mainloop()


    def save(self, name, fileformat=".pdf"):
        self.pack()
        self.canvas.update()

        # delete any existing .ps file of the same name:
        try:
            os.remove(name + ".ps")
            print("Removed a pre-existing file with the same name (" + name + ".ps)")
        except OSError:
            pass

        # write the .ps file and then convert
        #   (must be running Linux (or WSL) with ghostscript installed)
        self.canvas.postscript(file=name+".ps", colormode='color')
        if fileformat == ".pdf":
            subprocess.run(["ps2pdf", name + ".ps", name + ".pdf"])
        elif fileformat == ".png":
            subprocess.run(["gs", "-sDEVICE=png256", "-sOutputFile=" + name + ".png", "-r50", "-dBATCH", "-dNOPAUSE", name +".ps"])
        else:
            print(fileformat + " format not supported.")



    def _fix_point(self, p):

        # ensure we're dealing with an numpy array of floats
        if not isinstance(p, np.ndarray):
            p = np.array(p)
        p = p.astype(float)

        for (transform_type, transform) in self.transforms:
            if transform_type is "translation":
                p += transform
            elif transform_type is "scaling":
                p *= transform
            else:
                raise Exception("Reached invalid transformation: " +  transform)
        return p

    

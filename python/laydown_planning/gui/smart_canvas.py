from tkinter import Frame, Canvas
from numpy import array


# Usage:
# 
#   c = SmartCanvas()
#
#   # add features, for example:
#   c.line([0, 0], [1, 1]) 
#
#   c.show()


class SmartCanvas(Frame):

    def __init__(self):

        self.parent = Frame(None)
        self.parent.pack()
        self.width = 800
        self.height = 800

        Frame.__init__(self, self.parent,
            width=self.width,
            height=self.height)

        self.pack_propagate(False) # not sure why necessary
        self.canvas = Canvas(self, width=self.width, height=self.height,
            bg="#%02x%02x%02x" % (224, 224, 224),  # gray 300
            highlightthickness=0)
        self.canvas.pack()

        self.transforms = []

        # start off by fixing things so the origin is in 
        # the bottom left of screen, and +y is up:
        self.translation(0, self.height)
        self.scaling(1, -1)

    def translation(self, x, y):
        self.transforms.insert(0, ("translation", array([x, y])))

    def scaling(self, x, y):
        self.transforms.insert(0, ("scaling", array([x, y])))

    def circle(self):
        pass

    def line(self, start, end, width=1):
        start = self._fix_point(start)
        end = self._fix_point(end)
        
        self.canvas.create_line(*start, *end, width=width)

    def show(self):
        self.pack()
        self.parent.mainloop()

    def _fix_point(self, p):
        for (transform_type, transform) in self.transforms:
            if transform_type is "translation":
                p += transform
            elif transform_type is "scaling":
                p *= transform
            else:
                raise Exception("Reached invalid transformation: " +  transform)
        return p

    

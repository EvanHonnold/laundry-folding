from shapely.geometry import Polygon
import numpy as np

from helpers import direction
from constants import RULER_LENGTH

from laydown_planning.gui.smart_canvas import SmartCanvas
from laydown_planning.fold_instructions import FoldInstructions


def display_input(instr: FoldInstructions, filename=None, fileformat=".pdf"):

    canvas = SmartCanvas(width=600, height=400)

    effector = np.array([50, 300])
    ruler_vec = np.array([RULER_LENGTH, 0])
    garment_vec = np.array([0, -200])
    ruler_end = effector + ruler_vec

    garment_start = effector + 0.1 * ruler_vec # offset from effector a bit
    garment = Polygon([garment_start, ruler_end,
                       ruler_end + garment_vec, garment_start + garment_vec])

    # draw the ruler and canvas
    canvas.circle(effector, radius=10)
    canvas.line(effector, effector + ruler_vec, width=5)
    canvas.polygon(Polygon(garment), fill="gray")

    # draw the fold line
    intercept = effector + [instr.intercept, 0]
    line_vec = direction(instr.fold_angle)
    upper_endpoint = intercept + line_vec * 1000
    lower_endpoint = intercept - line_vec * 1000
    canvas.line(upper_endpoint, lower_endpoint, width=4, 
                fill="#%02x%02x%02x" % (183, 28, 28))

    # show or save the file
    if filename is None:
        canvas.show()
    else:
        canvas.save(name=filename, fileformat=fileformat)
        print("Done saving the file.")

import numpy as np
from shapely.geometry import Polygon

from constants import RULER_LENGTH
from helpers import direction
from laydown_planning.gui.smart_canvas import SmartCanvas

# For visualizing LaydownConfig objects.

def display_laydown_config(config):

    canvas = SmartCanvas(width=600, height=600)

    # draw the center line (gap in the table)
    canvas.line([0, 302], [600, 302])
    canvas.line([0, 298], [600, 298])

    # re-center origin in the middle of that line:
    canvas.translation(x=300, y=300)
    canvas.scaling(x=0.66, y=0.66)

    # draw the ruler
    ruler_base = np.array([0, config.y])
    ruler_vec = direction(config.ruler_direction) * RULER_LENGTH
    ruler_end = ruler_base + ruler_vec
    canvas.line(ruler_base, ruler_end, width=3)

    # draw an example garment
    garment_vec = direction(config.garment_direction) * 200
    offset = ruler_vec * 0.1    # so we don't draw garment along entire ruler
    corner1 = ruler_end + garment_vec
    corner2 = ruler_base + garment_vec + offset
    garment = Polygon([ruler_base + offset, ruler_end, corner1, corner2])
    canvas.polygon(garment, fill="gray")

    canvas.circle(ruler_base, 10)
    canvas.show()

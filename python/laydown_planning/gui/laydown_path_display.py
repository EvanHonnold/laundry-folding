from constants import RULER_LENGTH, TABLE_PLATES, ROBOT_BASE
from helpers import direction

from laydown_planning.laydown_path import LaydownPath
from laydown_planning.gui.smart_canvas import SmartCanvas

# For visualizing LaydownPath objects.

def display_laydown_path(path: LaydownPath, filename=None, fileformat=".pdf"):

    canvas = SmartCanvas(width=800, height=800)
    canvas.translation(200, 600)
    canvas.scaling(x=0.66, y=0.66)

    # draw the environment:
    for p in TABLE_PLATES:
        canvas.polygon(p, fill="darkgray")
    canvas.polygon(ROBOT_BASE)

    # draw the collision boxes of the ruler and arm
    box_list = path.get_hitboxes()
    fills = [(13, 71, 161), (21, 101, 192), (25, 118, 210)]
    for idx, box in enumerate(box_list):
        canvas.polygon(box, fill=fills[idx])

    # draw the ruler positions:
    ruler_starts = [path.start_xyz[0:2], path.dest_xyz[0:2], path.pullout_xyz[0:2]]
    fills = [(38, 50, 56), (55, 71, 79), (69, 90, 100)]
    for idx, start in enumerate(ruler_starts):
        canvas.circle(start, 10, fills[idx])
        end = start + direction(path.ruler_angle) * RULER_LENGTH
        canvas.line(start, end, width=5, fill=fills[idx])

    if filename is None:
        canvas.show()
    else:
        canvas.save(name=filename, fileformat=fileformat)
        print("Done saving the file.")
        
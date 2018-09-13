from laydown_planning.laydown_planner import plan, choose_best
from numpy import array
from helpers import within_range, direction, fix_angle, rotate
from laydown_planning.laydown_path import LaydownPath
from constants import LEFT

# TODO: continue testing here
# instr = FoldInstructions(250, pi/6)
# options = plan(instr)
# paths = []
# for option in options:
#     paths += [LaydownPath(option, 250, 250)]
# choose_best(paths)

# import tkinter as tk
# import math, cmath

# window = tk.Tk()
# window.geometry('500x500')
# canvas = tk.Canvas(window, width=500, height=500)
# canvas.pack()
# center = (250, 250)
# coords = [(250, 248),(400, 248), (400, 252), (250, 252)]
# polygon = canvas.create_polygon(coords)
# angle = cmath.exp(pi * 0.25 * 1j)
# offset = complex(center[0], center[1])
# newxy = []
# for x, y in coords:
#     v = angle * (complex(x, y) - offset) + offset
#     newxy.append(v.real)
#     newxy.append(v.imag)
# canvas.coords(polygon, *newxy)
# window.mainloop()


def example_inputdisplay():
    """ """
    import tkinter as tk
    from laydown_planning.gui.input_display import InputDisplay
    from fold_instructions import FoldInstructions
    from math import pi

    instr = FoldInstructions(100, pi * 0.25)

    parent = tk.Frame(None)
    parent.pack()
    display = InputDisplay(parent)
    display.show(instr)
    display.pack()
    parent.mainloop()


def example_laydown_config_display():
    import tkinter as tk
    from laydown_planning.gui.laydown_config_display import LaydownConfigDisplay
    from laydown_planning.laydown_config import LaydownConfiguration
    from math import pi

    config = LaydownConfiguration(100, 1.3 * pi, 1.8 * pi)

    parent = tk.Frame(None)
    parent.pack()
    display = LaydownConfigDisplay(parent)
    display.show(config)
    display.pack()
    parent.mainloop()


def example_laydown_path_display():
    import tkinter as tk
    from laydown_planning.gui.laydown_path_display import LaydownPathDisplay
    from laydown_planning.laydown_config import LaydownConfiguration
    from laydown_planning.laydown_path import LaydownPath
    from math import pi

    config = LaydownConfiguration(100, 0.5 * pi, 1.0 * pi)
    path = LaydownPath(config, 100, 200, destination_x=237)

    parent = tk.Frame(None)
    parent.pack()
    display = LaydownPathDisplay(parent)
    display.show(path)
    display.pack()
    parent.mainloop()

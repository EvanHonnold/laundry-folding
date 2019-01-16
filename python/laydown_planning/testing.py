# TODO: continue testing here
# instr = FoldInstructions(250, pi/6)
# options = plan(instr)
# paths = []
# for option in options:
#     paths += [LaydownPath(option, 250, 250)]
# choose_best(paths)

from PIL import ImageGrab
from tkinter import Tk


def example_inputdisplay():
    """ """
    import tkinter as tk
    from laydown_planning.gui.input_display import InputDisplay
    from laydown_planning.fold_instructions import FoldInstructions
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

    config = LaydownConfiguration(100, 1.3 * pi, 1.8 * pi)
    path = LaydownPath(config, 100, 200, destination_x=237)

    parent = tk.Frame(None)
    parent.pack()
    display = LaydownPathDisplay(parent)
    display.show(path)
    display.pack()
    parent.mainloop()


def checking_collision_detection():
    import tkinter as tk
    from laydown_planning.gui.laydown_path_display import LaydownPathDisplay
    from laydown_planning.laydown_config import LaydownConfiguration
    from laydown_planning.laydown_path import LaydownPath
    from math import pi

    config = LaydownConfiguration(100, 1.3 * pi, 1.8 * pi)
    path = LaydownPath(config, 100, 200, destination_x=250)

    from laydown_planning.laydown_planner import collisions
    print("Is collision?", collisions(path))

    parent = tk.Frame(None)
    parent.pack()
    display = LaydownPathDisplay(parent)
    display.show(path)
    display.pack()
    parent.mainloop()


def testing_overall_planner():
    from laydown_planning.laydown_planner import plan, choose_best
    from laydown_planning.fold_instructions import FoldInstructions
    from math import pi
    import tkinter as tk
    from laydown_planning.gui.input_display import InputDisplay
    from laydown_planning.gui.laydown_config_display import LaydownConfigDisplay

    instr = FoldInstructions(400, 0.5 * pi)

    # show the fold instructions:
    # parent = tk.Frame(None)
    # parent.pack()
    # display = InputDisplay(parent)
    # display.show(instr)
    # display.pack()
    # parent.mainloop()


    configs = plan(instr)
    for i in range(0, len(configs)):
        if i is 1:
            parent = tk.Frame(None)
            parent.pack()
            display = LaydownConfigDisplay(parent)
            display.show(configs[i])
            display.pack()
            parent.mainloop()
            pass

    # TODO continue debugging here: the FoldInstructions aren't
    # converting correctly into LaydownConfigurations.

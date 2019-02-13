# TODO: continue testing here
# instr = FoldInstructions(250, pi/6)
# options = plan(instr)
# paths = []
# for option in options:
#     paths += [LaydownPath(option, 250, 250)]
# choose_best(paths)

from tkinter import Tk


def example_inputdisplay():
    """ """
    from laydown_planning.gui.input_display import display_input
    from math import pi
    from laydown_planning.fold_instructions import FoldInstructions

    instr = FoldInstructions(100, pi * 0.25)
    display_input(instr, "testing_input", ".png")


def example_laydown_config_display():
    from laydown_planning.gui.laydown_config_display import display_laydown_config
    from laydown_planning.laydown_config import LaydownConfiguration
    from math import pi

    c = LaydownConfiguration(100, 1.3 * pi, 1.8 * pi)
    display_laydown_config(c)


def example_laydown_path_display():
    from laydown_planning.laydown_config import LaydownConfiguration
    from laydown_planning.laydown_path import LaydownPath
    from laydown_planning.gui.laydown_config_display import display_laydown_config
    from laydown_planning.gui.laydown_path_display import display_laydown_path
    from math import pi

    config = LaydownConfiguration(100, 1.3 * pi, 1.8 * pi)
    path = LaydownPath(config, 100, 200, destination_x=237)
    
    display_laydown_config(config, "testing_config", ".png")
    display_laydown_path(path, "testing_path", ".png")


def checking_collision_detection():
    import tkinter as tk
    from laydown_planning.gui.laydown_path_display import display_laydown_path
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

    from laydown_planning.laydown_planner import plan, choose_best, within_reach, collisions
    from laydown_planning.fold_instructions import FoldInstructions
    from laydown_planning.laydown_path import LaydownPath

    from math import pi
    import tkinter as tk

    from laydown_planning.gui.input_display import display_input
    from laydown_planning.gui.laydown_config_display import display_laydown_config
    from laydown_planning.gui.laydown_path_display import display_laydown_path

    from constants import TABLE_PLATES

    instr = FoldInstructions(350, 0.33 * pi)
    display_input(instr, "a__Instructions", ".png")

    count = 0 # FOR TESTING

    configs = plan(instr)
    for index, laydown_config in enumerate(configs):
        display_laydown_config(laydown_config, "config %d" % index, ".png")

        path = LaydownPath(laydown_config, height=200, pull_dist=50)

        # vary the x-coordinate and evaluate the resulting paths:
        path.shift_x(-400)
        while path.dest_xyz[0] < 500:
            path.shift_x(25)

            if within_reach(path):

                # calculate intersection of area swept by ruler (hitbox 0)
                # with the table plates (the workspace)
                hbs = path.get_hitboxes()
                total_area = 0.0
                for plate in TABLE_PLATES:
                    total_area += plate.intersection(hbs[0]).area
                proportion = total_area / float(hbs[0].area)

                if proportion > 0.5 and not collisions(path):
                    display_laydown_path(path, "path%dWORKS%f" % (count, proportion), ".png")

            count += 1

    

    

"""flood_fill_py controller."""

from controller import Robot #Keyboard
from collections import namedtuple
#my modules
from Constants import *
import main_functions

def run_robot(robot):

    match mode_params.ALGORITHM:
        case 1:
            main_functions.keyboard_main(robot)
        case 2:
            main_functions.floodfill_main(robot)
        case 3:
            main_functions.DFS_main(robot)

if __name__ == "__main__":
    
    robot = Robot()
    
    run_robot(robot)
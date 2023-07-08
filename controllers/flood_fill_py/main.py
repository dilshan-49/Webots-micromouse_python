"""flood_fill_py controller."""

from controller import Robot #Keyboard
from collections import namedtuple
#my modules
from Constants import *
import main_functions as main_f

def run_robot(robot):

    match mode_params.ALGORITHM:
        case 1:
            main_f.keyboard_main(robot)
        case 2:
            main_f.floodfill_main(robot)
        case 3:
            main_f.DFS_main(robot)
        case 4:
            main_f.BFS_main(robot)
            

if __name__ == "__main__":
    
    robot = Robot()
    
    run_robot(robot)
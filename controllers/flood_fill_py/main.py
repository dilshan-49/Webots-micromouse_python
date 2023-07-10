"""flood_fill_py controller."""

from controller import Robot
#my modules
from Constants import *
import main_functions as main_f

def run_robot(robot):

    match mode_params.ALGORITHM:
        case algorithms.KEYBOARD:
            main_f.keyboard_main(robot)
        case algorithms.FLOODFILL:
            main_f.floodfill_main(robot)
        case algorithms.DFS:
            main_f.DFS_main(robot)
        case algorithms.BFS:
            main_f.BFS_main(robot)
        case algorithms.A_STAR:
            main_f.A_star_main(robot)
            

if __name__ == "__main__":
    
    robot = Robot()
    
    run_robot(robot)
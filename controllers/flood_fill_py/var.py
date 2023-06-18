from threading import Condition
from Constants import *

pos_update = False
distance_update = False
robot_pos = 0 
maze_map_global = [0] * maze_parameters.MAZE_SIZE
distance_global = [255] * maze_parameters.MAZE_SIZE
target_global = TARGET_CELL
con = Condition() #thread waiting condtion object

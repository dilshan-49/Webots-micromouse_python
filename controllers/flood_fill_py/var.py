from threading import Condition,Event
from Constants import *


distance_update = False
map_update = False

robot_pos = maze_parameters.START_CELL
maze_map_global = [0] * maze_parameters.MAZE_SIZE
distance_global = [255] * maze_parameters.MAZE_SIZE
target_global = maze_parameters.TARGET_CELL
con = Condition() #thread waiting condtion object
drawing_event = Event()
main_event = Event()

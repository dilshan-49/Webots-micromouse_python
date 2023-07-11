from threading import Event
from Constants import *


distance_update = False
map_update = False
searching_end = False

robot_pos = maze_parameters.START_CELL
maze_map_global = [0] * maze_parameters.MAZE_SIZE
distance_global = [255] * maze_parameters.MAZE_SIZE
target_global = maze_parameters.TARGET_CELL
cost_global = {}

drawing_event = Event()
main_event = Event()

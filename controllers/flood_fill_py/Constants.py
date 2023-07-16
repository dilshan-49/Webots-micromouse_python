from collections import namedtuple

# START Values to change to run program in different modes etc. START

# 1- search, 2 - speeedrun
MODE = 1                    
# 1 - keyboard/manual, 2 - floodfill, 3 - deep first search (DFS),
# 4 - breadth first search (BFS), 5 - A*, 6 - A* modified
ALGORITHM = 6           
# 1- print sensors values etc. for testing, 0 - no prints
TESTING = 0

#only for floodfill
# True - discover whole maze (guaranteed shortest path, but long searching time),
# False - make 2 runs: start -> target and target -> start (shorter searching time, but shortest path not guaranteed)
WHOLE_SEARCH = False 

# END Values to change to run program in different modes etc. END

# Robot parameters
TIME_STEP = 64
TILE_LENGTH = 0.12 #tile length
AXLE = 0.0568 #axle length 0.0568
WHEEL = 0.02002 #wheel radius 0.02002
SPEED = 4

# Modes
SEARCH = 1
SPEEDRUN = 2

# Algorithms
KEYBOARD = 1
FLOODFILL = 2
DFS = 3
BFS = 4
A_STAR = 5
A_STAR_MOD = 6

# Walls values according to direction (NORTH is not always forward etc.)
WEST =      1    #  00000001 
SOUTH =     2    #  00000010 
EAST =      4    #  00000100 
NORTH =     8    #  00001000

# Maze params
ROWS =  16
COLUMNS = 16
MAZE_SIZE = ROWS * COLUMNS
START_CELL = 0
VISITED = 64


# Sets correct target for used mode
if MODE == 2:
    TARGET_CELL = 136
elif MODE == 1:
    if WHOLE_SEARCH:
        TARGET_CELL = 1
    else:
        TARGET_CELL = 136

# Named tuples for more readable code
Direction = namedtuple("direction", " WEST SOUTH EAST NORTH")
direction = Direction(WEST, SOUTH, EAST, NORTH)

Robot_parameters = namedtuple('robot_parameters','AXLE WHEEL SPEED')
robot_parameters = Robot_parameters(AXLE, WHEEL, SPEED)

Mode_params = namedtuple('mode_params','SEARCH SPEEDRUN MODE TESTING WHOLE_SEARCH ALGORITHM')
mode_params = Mode_params(SEARCH, SPEEDRUN, MODE, TESTING, WHOLE_SEARCH, ALGORITHM)

Algorithms = namedtuple('algorithms','KEYBOARD FLOODFILL DFS BFS A_STAR A_STAR_MOD')
algorithms = Algorithms(KEYBOARD, FLOODFILL, DFS, BFS, A_STAR, A_STAR_MOD)

Maze_parameters = namedtuple('maze_parameters',
                              'ROWS COLUMNS MAZE_SIZE VISITED TARGET_CELL TILE_LENGTH START_CELL')
maze_parameters = Maze_parameters(ROWS, COLUMNS, MAZE_SIZE, VISITED, TARGET_CELL, TILE_LENGTH, START_CELL)

Moves = namedtuple("moves", "forward left back right")
moves = Moves('W', 'A', 'S', 'D')
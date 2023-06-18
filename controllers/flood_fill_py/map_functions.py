#Map updating functions
from Constants import *


def detect_walls(robot, ps, number_of_scans):
    
    avg2_right_sensor = 0    #ps2
    avg4_back_sensor = 0     #ps4
    avg5_left_sensor = 0     #ps5
    avg7_front_sensor = 0    #ps7

    #read distance sensors
    ps_values = [0] * 8
    sensors_indexes = [2, 4, 5, 7]

    for i in range(0,number_of_scans): #more scans for better accuracy
    
        for i in sensors_indexes:
            ps_values[i] = ps[i].getValue()

        avg2_right_sensor += ps_values[2]

        avg4_back_sensor += ps_values[4]

        avg5_left_sensor += ps_values[5]

        avg7_front_sensor += ps_values[7]

        robot.step(TIME_STEP) #simulation update

    #average score of sensors measurements
    avg2_right_sensor = avg2_right_sensor / number_of_scans
    avg4_back_sensor = avg4_back_sensor / number_of_scans
    avg5_left_sensor = avg5_left_sensor / number_of_scans
    avg7_front_sensor = avg7_front_sensor / number_of_scans

    #Wall detection
    left_wall = avg5_left_sensor > 80.0
    front_wall = avg7_front_sensor > 80.0
    right_wall = avg2_right_sensor > 80.0
    back_wall = avg4_back_sensor > 80.0

    return left_wall, front_wall, right_wall, back_wall, avg5_left_sensor, avg2_right_sensor


''' add_wall
# @brief Add wall according to distance sensors.
# Depending on robot orientation, value in variable wall 
# is changed so it match global directions. Then wall is added
# to maze map on robot field and respective neighbouring field.
#
# @param maze_map: list with actual maze map with walls
# @param robot_position: actual robot position in maze
# @param robot_orientation: actual robot orientation in global directions
# @param wall: value which indicates on which side of robot wall was detected
#
# @retval None.
'''
def add_wall(maze_map, robot_position, robot_orientation, wall):
    
    #shift wall value
    if robot_orientation == direction.EAST:
        if wall != direction.WEST:
            wall //= 2
        else:
            wall = 8
    elif robot_orientation == direction.SOUTH:
        if wall == direction.WEST or  wall == direction.SOUTH:
            wall *= 4
        else:
            wall //= 4
    elif robot_orientation == direction.WEST:
        if wall != direction.NORTH:
            wall *= 2
        else:
            wall = 1

    maze_map[robot_position] = maze_map[robot_position] | wall #add sensed wall
    
    #add wall in neighbour field
    if wall == direction.NORTH:
        
        robot_position = robot_position + maze_parameters.COLUMNS   #upper field
        check = robot_position in range(0,256)

        if check:
            maze_map[robot_position] = maze_map[robot_position] | direction.SOUTH

    if wall == direction.EAST:
        
        robot_position = robot_position + 1     #left field
        check = robot_position in range(0,256)

        if check:
            maze_map[robot_position] = maze_map[robot_position] | direction.WEST 
    
    if wall == direction.SOUTH:

        robot_position = robot_position - maze_parameters.COLUMNS   #lower field
        check = robot_position in range(0,256)
        
        if check:
            maze_map[robot_position] = maze_map[robot_position] | direction.NORTH

    if wall == direction.WEST:
        
        robot_position = robot_position - 1     #right field
        check = robot_position in range(0,256)
        
        if check:
            maze_map[robot_position] = maze_map[robot_position] | direction.EAST


''' init_maze_map
# @brief Initialize maze map with external walls.
#
# @param maze_map: list which contains maze map values
#
# @retv maze_map: Initialized maze map list
'''
def init_maze_map(maze_map):
    maze_map[0] = maze_map[0] | maze_parameters.VISITED #mark start as visited

    for i in range(0, 16):
        maze_map[i] = maze_map[i] | direction.SOUTH

    for i in range(240, 256):
        maze_map[i] = maze_map[i] | direction.NORTH    

    for i in range(0, 241, 16):
        maze_map[i] = maze_map[i] | direction.WEST 

    for i in range(15, 256, 16):
        maze_map[i] = maze_map[i] | direction.EAST

    #print_array(maze_map, 0)

    return maze_map


''' init_distance_map
# @brief Initialize distance map with max values and 0 as target.
# Target is 0 for floodfill algorythm working properly.
#
# @param distance: list which contains distance values
# @param target: value which contains targetted cell
#
# @retv distance: Initialized distance list
'''
def init_distance_map(distance, target):
    distance = [maze_parameters.MAZE_SIZE - 1] * maze_parameters.MAZE_SIZE
    distance[target] = 0

    return distance

   
''' print_array
# @brief print 256 element list as 16x16 in terminal.
#
# @param list: list which contains map or distance values
# @param action: value which indicates to print map walls without visited cells
#
# @retv None
'''
def print_array(list, action):

    print("")
    if action == 0:     #just print array

        i = 240
        k = 1
        while i >= 0:
            print('{0:>3}'.format(list[i]), end = " ")
            if k == 16:
                print('\n')
                i -= 31     # 32 - 1 cuz no i++ in this loop iteration
                k = 1
            else:
                k += 1
                i += 1
    elif action == 1:   #print array without visited mark to read just walls

        list_temp = list.copy()

        for i in range(len(list_temp)):
            if list_temp[i] and maze_parameters.VISITED:
                list_temp[i] -= 64  #version to avoid negative values(errors etc.)
        
        i = 240
        k = 1
        while i >= 0:
            print('{0:>3}'.format(list_temp[i]), end = " ")
            if k == 16:
                print('\n')
                i -= 31  # 32 - 1 cuz no i++ in this loop iteration
                k = 1
            else:
                k += 1
                i += 1

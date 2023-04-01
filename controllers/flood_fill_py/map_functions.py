#Map updating functions
from Constants import *


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
            wall /= 2
        else:
            wall = 8
    elif robot_orientation == direction.SOUTH:
        if wall == direction.WEST or  wall == direction.SOUTH:
            wall *= 4
        else:
            wall /= 4
    elif robot_orientation == direction.WEST:
        if wall != direction.NORTH:
            wall *= 2
        else:
            wall = 1
    
    maze_map[robot_position] = maze_map[robot_position] | wall #add sensed wall
    
    #add wall in neighbour field
    if wall == direction.NORTH:
        robot_position = robot_position + maze_parameters.COLUMNS   #upper field
        maze_map[robot_position] = maze_map[robot_position] | direction.SOUTH

    if wall == direction.EAST:
        robot_position = robot_position + 1     #left field
        maze_map[robot_position] = maze_map[robot_position] | direction.WEST 
    
    if wall == direction.SOUTH:
        robot_position = robot_position - maze_parameters.COLUMNS   #lower field
        maze_map[robot_position] = maze_map[robot_position] | direction.NORTH

    if wall == direction.WEST:
        robot_position = robot_position - 1     #right field
        maze_map[robot_position] = maze_map[robot_position] | direction.EAST


#init maze map with external walls
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

    print_array(maze_map, 0)

#init distance map with 255 and 0 as target (needed for floodfill algorythm)
def init_distance_map(distance, target):
    distance = [maze_parameters.MAZE_SIZE - 1] * maze_parameters.MAZE_SIZE
    distance[target] = 0

#print array in a shape of maze (16x16 etc.)    
def print_array(maze_map, action):

    print("")
    if action == 0:     #just print array

        i = 240
        k = 1
        while i >= 0:
            print('{0:>3}'.format(maze_map[i]), end = " ")
            if k == 16:
                print('\n')
                i -= 31     # 32 - 1 cuz no i++ in this loop iteration
                k = 1
            else:
                k += 1
                i += 1
    elif action == 1:   #print array without visited mark to read just walls

        mapp_temp = maze_map.copy()

        for i in range(len(mapp_temp)):
            if mapp_temp[i] and maze_parameters.VISITED:
                mapp_temp[i] -= 64  #version to avoid negative values(errors etc.)  if(array[i] & VISITED) array[i] -= 64;
        
        i = 240
        k = 1
        while i >= 0:
            print('{0:>3}'.format(maze_map[i]))
            if k == 16:
                print('\n')
                i -= 31  # 32 - 1 cuz no i++ in this loop iteration
                k = 1
            else:
                k += 1
                i += 1
    print('')

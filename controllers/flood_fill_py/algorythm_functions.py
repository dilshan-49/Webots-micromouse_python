#Algorythm related functions

from Constants import *
from map_functions import print_array


#floodfill algorythm
def floodfill(maze_map, robot_position, distance):
    
    search = True

    while search:
        search = False

        for i in range(0, maze_parameters.MAZE_SIZE):
            if distance[i] < 255:

                if (maze_map[i] & direction.NORTH) != direction.NORTH:
                    if distance[i + maze_parameters.COLUMNS] == 255 or ((distance[i] +1) < distance[i + maze_parameters.COLUMNS]):
                        distance[i + maze_parameters.COLUMNS] = distance[i] +1  #update distance value on north tile
                        search = True
                
                if (maze_map[i] & direction.EAST) != direction.EAST:
                     if distance[i + 1] == 255 or ((distance[i] +1) < distance[i + 1]):
                         distance[i + 1] = distance[i] +1   #update distance value on EAST tile
                         search = True
                
                if (map[i] & direction.WEST) != direction.WEST:
                    if distance[i - 1] == 255 or ((distance[i] +1) < distance[i - 1]):
                        distance[i - 1] = distance[i] + 1   #update distance value on WEST tile
                        search = True
                #prop unnecessary cuz robot doesnt move backward
                if (maze_map[i] & direction.SOUTH) != direction.SOUTH: 
                    if distance[i - maze_parameters.COLUMNS] == 255 or ((distance[i] +1) < distance[i - maze_parameters.COLUMNS]):
                        distance[i - maze_parameters.COLUMNS] = distance[i] + 1 #update distance value on SOUTH tile
                        search = True
            
    print('\n TRASA ')
    print_array(distance, 0)
    print('\n TRASA ')


''' where_to_move
# @brief Decide where to move by checking distance values in neighbors cells.
# Depending on robot orientation, value in variable wall 
# is changed so it match global directions. Then wall is added
# to maze map on robot field and respective neighbouring field.
#
# @param maze_map: list with actual maze map with walls
# @param robot_position: variable with actual robot position in maze
# @param distance: list with actual distances values/path
# @param robot_orientation: variable with actual robot orientation in global directions
#
# @retval move_direction: variable with move direction to do
'''
def where_to_move(maze_map, robot_position, distance, robot_orientation):

    best_neighbour = 255
    move_direction = direction.NORTH

    if (maze_map[robot_position] & direction.NORTH) != direction.NORTH:

        if distance[robot_position + maze_parameters.COLUMNS] <= best_neighbour:

            if distance[robot_position + maze_parameters.COLUMNS] < best_neighbour:

                best_neighbour = distance[robot_position + maze_parameters.COLUMNS]
                move_direction = direction.NORTH

            elif robot_orientation == direction.NORTH:
                move_direction = direction.NORTH
    
    if (maze_map[robot_position] & direction.EAST) != direction.EAST:

        if distance[robot_position + 1] <= best_neighbour:

            if distance[robot_position + 1] < best_neighbour:

                best_neighbour = distance[robot_position + 1]
                move_direction = direction.EAST

            elif robot_orientation == direction.EAST:
                move_direction = direction.EAST

    if (maze_map[robot_position] & direction.SOUTH) != direction.SOUTH:

        if distance[robot_position - maze_parameters.COLUMNS] <= best_neighbour:

            if distance[robot_position - maze_parameters.COLUMNS] < best_neighbour:

                best_neighbour = distance[robot_position - maze_parameters.COLUMNS]
                move_direction = direction.SOUTH

            elif robot_orientation == direction.SOUTH:
                move_direction = direction.SOUTH
    
    if (maze_map[robot_position] & direction.WEST) != direction.WEST:

        if distance[robot_position - 1] <= best_neighbour:

            if distance[robot_position - 1] < best_neighbour:

                best_neighbour = distance[robot_position - 1]
                move_direction = direction.WEST
                
            elif robot_orientation == direction.WEST:
                move_direction = direction.WEST

    return move_direction





            







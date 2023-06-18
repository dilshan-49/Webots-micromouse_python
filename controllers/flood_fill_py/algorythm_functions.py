#Algorythm related functions

from Constants import *
from map_functions import print_array
import draw_maze


''' floodfill
# @brief Floodfill algorythm which calculates shortest path to actual target based on actual maze map.
#
# @param maze_map: list with actual maze map with walls
# @param distance: list with actual distances values/path
#
# @retval move_direction: variable with move direction to do
'''
def floodfill(maze_map, distance):
    
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
                
                if (maze_map[i] & direction.WEST) != direction.WEST:
                    if distance[i - 1] == 255 or ((distance[i] +1) < distance[i - 1]):
                        distance[i - 1] = distance[i] + 1   #update distance value on WEST tile
                        search = True
                #prop unnecessary cuz robot doesnt move backward
                if (maze_map[i] & direction.SOUTH) != direction.SOUTH: 
                    if distance[i - maze_parameters.COLUMNS] == 255 or ((distance[i] +1) < distance[i - maze_parameters.COLUMNS]):
                        distance[i - maze_parameters.COLUMNS] = distance[i] + 1 #update distance value on SOUTH tile
                        search = True
            
    # print('\n Path ')
    # print_array(distance, 0)
    # print(' Path ')

    return distance


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


''' change_orientation
# @brief Change robot orientation basing on last orientation and last turn.
#
# @param robot_orientation: variable with actual robot orientation in global directions
# @param action: variable with information where robot turns
#
# @retval robot_orientation: variable with updated robot orientation
'''
def change_orientation(robot_orientation, action):
    match action:
        case keys.right: #turn right
            if robot_orientation == direction.WEST:
                robot_orientation = direction.NORTH
            else:
                robot_orientation //= 2
        case keys.left: #turn left
            if robot_orientation == direction.NORTH:
                robot_orientation = direction.WEST
            else:
                robot_orientation *= 2
        case keys.back: #turn back
            if robot_orientation == direction.NORTH or robot_orientation == direction.EAST:
                robot_orientation //= 4
            else:
                robot_orientation *= 4
    
    x = direction.index(robot_orientation)
    
    if TESTING:
        print('orientacja:', direction._fields[x])
    
    return robot_orientation


''' change_position
# @brief Update position of the robot basing on current orientation of the robot.
#
# @param robot_position: variable with robot position
# @param robot_orientation: variable with actual robot orientation in global directions
#
# @retval robot_position: variable with updated robot position
'''
def change_position(robot_position, robot_orientation):
    
    if robot_orientation == direction.NORTH:
        robot_position = robot_position + maze_parameters.COLUMNS
    
    elif robot_orientation == direction.EAST:
        robot_position = robot_position + 1
    elif robot_orientation == direction.SOUTH:
        robot_position = robot_position - maze_parameters.COLUMNS
    
    elif robot_orientation == direction.WEST:
        robot_position = robot_position - 1

    return robot_position
    

''' change_target
# @brief Marks every visited cell, after reaching targeted cell, change cell to first unvisited cell.
# When reaching final target, saves distance map to file.
#
# @param maze_map: list with actual maze map with walls
# @param robot_position: variable with actual robot position in maze
# @param distance: list with actual distances values/path
# @param target: variable with field number to which robot tries to get
#
# @retval target: variable with updated targetted field
'''
def change_target(maze_map, robot_position, distance, target):
    
    search = True
    i = 0

    while search: #search to find unvisited cell, otherwise end
        
        if not(maze_map[i] & maze_parameters.VISITED):
            
            target = i
            search = False
            if TESTING:
                print('target =', target)
        else:
            i += 1
        
        if i == 256:
            target = 136
            search = False
            if TESTING:
                print('target =', target)

    if (robot_position == target) and (search == False) and (target == 136): #after reaching final target, save result in file
        print('KONIEC!!!!!!!')

        write_file('path.txt', distance)
        
        #Check that distance was correctly written to file
        distance_temp = read_file('path.txt')

        print('############ KONCOWA TRASA ############')
        print_array(distance_temp, 0) 

        write_file('maze.txt', maze_map)
    
        #Check that maze map was correctly written to file
        maze_map_temp = read_file('maze.txt')

        print('############ KONCOWY LABIRYNT ############')
        print_array(maze_map_temp, 1) 
        #draw_maze.draw_maze(maze_map_temp, distance_temp)
        input("press any key to end")
        exit(0)
            
    return target


def read_file(file_name):
        
        file = open(file_name,'r')
        if file == None:
            print('ERROR')
            exit(1)
        
        list_temp = []
        for field in file:
            list_temp.append(int(field))
        file.close()
        
        return list_temp


def write_file(file_name, list):
        
        file = open(file_name,'w')
        
        if file == None:
            print('ERROR')
            exit(1)
        
        for field in list:
            file.write('%i\n' % field)
        
        file.close()

        




      





            







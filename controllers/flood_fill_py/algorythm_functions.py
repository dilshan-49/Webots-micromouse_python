#Algorythm related functions

from Constants import *
from map_functions import print_array, init_distance_map
import var
import heapq

# def dijkstra(maze_map, start, target):
#     distances = {}  # Dictionary to store the shortest distances
#     prev = {}  # Dictionary to store the previous node in the shortest path
#     heap = []  # Min-heap to prioritize cells with shorter distances

#     distances[start] = 0
#     heapq.heappush(heap, (distances[start], start))

#     while heap:
#         curr_dist, curr_node = heapq.heappop(heap)

#         if curr_node == target:
#             break

#         if curr_dist > distances[curr_node]:
#             continue

#         for neighbor in get_neighbors(curr_node):
#             new_dist = curr_dist + 1  # Assuming each movement has a cost of 1

#             if neighbor not in distances or new_dist < distances[neighbor]:
#                 distances[neighbor] = new_dist
#                 prev[neighbor] = curr_node
#                 heapq.heappush(heap, (new_dist, neighbor))

#     if target not in prev:
#         return None  # No path found

#     # Reconstruct the shortest path
#     path = []
#     curr = target
#     while curr != start:
#         path.append(curr)
#         curr = prev[curr]
#     path.append(start)
#     path.reverse()

#     return path 


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
    
    if mode_params.TESTING:
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
    
    match mode_params.WHOLE_SEARCH:
        case False:
            if robot_position == 136:

                mark_center(maze_map)

                distance = init_distance_map(distance, target) #reset path
                distance = floodfill(maze_map, distance) #path
                
                #fill unvisited cells with 4 walls to verify if the shortest path was find
                distance_check = check_distance(distance, maze_map, target)

                if distance_check == True:
                    print("To jest najkrotsza/jedna z najkrotszych tras")
                    var.searching_end = True
                else:
                    print("Moze byc krotsza trasa, lecimy dalej")
                    target = 0

            elif robot_position == 0:
                distance_check = check_distance(distance, maze_map, target)
                if distance_check == True:
                    print("To jest najkrotsza/jedna z najkrotszych tras")
                else:
                    print("Moze byc krotsza trasa")
                var.searching_end = True
                target = 136
        case True:
            search = True
            i = 0
            while search: #search to find unvisited cell, otherwise end
            
                if not(maze_map[i] & maze_parameters.VISITED):
                    
                    target = i
                    search = False
                    if mode_params.TESTING:
                        print('target =', target)
                else:
                    i += 1
                
                if i == 256:
                    target = 136
                    search = False
                    var.searching_end = True
                    if mode_params.TESTING:
                        print('target =', target)

    # if (robot_position == target) and (search == False) and (target == 136): #after reaching final target, save result in file
    if var.searching_end:
    
        distance = init_distance_map(distance, target) #reset path
        distance = floodfill(maze_map, distance) #path
        
        write_file('path.txt', distance)
        
        #Check that distance was correctly written to file
        distance_temp = read_file('path.txt')
        
        if mode_params.TESTING:
            print('############ ENDING PATH ############')
            print_array(distance_temp, 0) 

        write_file('maze.txt', maze_map)
    
        #Check that maze map was correctly written to file
        maze_map_temp = read_file('maze.txt')
        
        if mode_params.TESTING:
            print('############ ENDING MAZE ############')
            print_array(maze_map_temp, 1) 
        # var.searching_end = True
        #draw_maze.draw_maze(maze_map_temp, distance_temp)
        # input("press any key to end")
        # exit(0)
            
    return target


def mark_center(maze_map):
        center = [119, 120, 135]
        for center_cell in center:
            if (maze_map[center_cell] & maze_parameters.VISITED) != maze_parameters.VISITED:
                match center_cell:
                    case 119:
                        maze_map[center_cell] = 3 #+ maze_parameters.VISITED
                        maze_map[center_cell - 1] |= direction.EAST
                        maze_map[center_cell - 16] |= direction.NORTH
                    case 120:
                        maze_map[center_cell] = 6 #+ maze_parameters.VISITED
                        maze_map[center_cell + 1] |= direction.WEST
                        maze_map[center_cell - 16] |= direction.NORTH
                    case 135:
                        maze_map[center_cell] = 9 #+ maze_parameters.VISITED
                        maze_map[center_cell - 1] |= direction.EAST
                        maze_map[center_cell + 16] |= direction.SOUTH

def check_distance(distance, maze_map, target):
    distance_check = distance.copy()
    maze_map_check = maze_map.copy()
    for i in range(0, maze_parameters.MAZE_SIZE):
        if (maze_map_check[i] & maze_parameters.VISITED) != maze_parameters.VISITED:
            maze_map_check[i] = maze_map_check[i] | 15 | maze_parameters.VISITED
    
    distance_check = init_distance_map(distance_check, target) #reset path
    distance_check = floodfill(maze_map_check, distance_check) #path
    check = distance[0] >= distance_check[0]

    return check


''' read_file
# @brief Read file
#
# @param file_name: variable with a file name
#
# @retval list_temp: list with a content of a file
'''
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

''' write_file
# @brief Write file
#
# @param file_name: variable with a file name
# @param: list: list with a content to write file
# @retval None
'''
def write_file(file_name, list):
        
        file = open(file_name,'w')
        
        if file == None:
            print('ERROR')
            exit(1)
        
        for field in list:
            file.write('%i\n' % field)
        
        file.close()

        




      





            







from controller import Robot, Keyboard
from collections import namedtuple
from threading import Thread
import copy
#my modules
from Constants import *
import map_functions
import move_functions
import algorythm_functions
import draw_maze
import var
import BFS_functions
''' init_maze_map_graph
# @brief Initialize maze map with external walls as graph.
# #params None
# @retv maze_map: Initialized maze map dictionary
'''
def init_maze_map_graph():
    maze_map = {}
    rows = maze_parameters.ROWS
    cols = maze_parameters.COLUMNS
    size = rows * cols
    left_down_corner = 0
    right_down_corner = rows - 1
    left_up_corner = rows * (cols - 1)
    right_up_corner = size - 1
    
    #corners
    maze_map[left_down_corner] = [rows, 1]
    maze_map[right_down_corner] = [right_down_corner + rows, right_down_corner - 1]
    maze_map[left_up_corner] = [left_up_corner + 1, left_up_corner - rows]
    maze_map[right_up_corner] = [right_up_corner - rows, right_up_corner - 1]

    #down wall cells
    for cell in range(left_down_corner + 1, right_down_corner):
        maze_map[cell] = [cell + rows, cell + 1, cell - 1]
    #up wall cells
    for cell in range(left_up_corner + 1, right_up_corner):
        maze_map[cell] = [cell + 1, cell - rows, cell - 1]
    #left wall cells
    for cell in range(left_down_corner + rows, left_up_corner, 16):
        maze_map[cell] = [cell + rows, cell + 1, cell - rows]
    #right wall cells
    for cell in range(right_down_corner + rows, right_up_corner, 16):
        maze_map[cell] = [cell + rows, cell - rows, cell - 1]
    cell = 17
    #inside cells
    while True:
        maze_map[cell] = [cell + rows, cell + 1, cell - rows, cell - 1]
        end = cell == (right_up_corner - 1 - rows)
        if end:
            break

        z = (cell % rows) == 14
        
        if z: # next row
            cell += 3
        else: # next column
            cell += 1

    return maze_map


def init_maze_map_graph2():
    maze_map = {}
    maze = []
    for i in range(0, maze_parameters.MAZE_SIZE):
        maze_map[i] = []

    return maze_map

''' add_wall TODO update
# @brief Add wall according to distance sensors.
# Depending on robot orientation, value in variable wall 
# is changed so it match global directions. Then wall is added
# to maze map on robot field and respective neighbouring field.
#
# @param maze_map: list with actual maze map with walls
# @param robot_position: actual robot position in maze
# @param robot_orientation: actual robot orientation in global directions
# @param detected_wall: value which indicates on which side of robot wall was detected
#
# @retval None.
'''
def add_walls_graph(maze_map, robot_position, robot_orientation, detected_wall):
    walls = []
    rows = maze_parameters.ROWS
    
    for i in detected_wall.keys():
        if not detected_wall[i]:
            match i:
                case 'front wall':
                    if robot_orientation == direction.NORTH:
                        walls.append(robot_position + rows)
                    elif robot_orientation == direction.EAST:
                        walls.append(robot_position + 1)
                    elif robot_orientation == direction.SOUTH:
                        walls.append(robot_position - rows)
                    elif robot_orientation == direction.WEST:
                        walls.append(robot_position - 1)
                case 'left wall':
                    if robot_orientation == direction.NORTH:
                        walls.append(robot_position - 1)
                    elif robot_orientation == direction.EAST:
                        walls.append(robot_position + rows)
                    elif robot_orientation == direction.SOUTH:
                        walls.append(robot_position + 1)
                    elif robot_orientation == direction.WEST:
                        walls.append(robot_position - rows)
                case 'right wall':
                    if robot_orientation == direction.NORTH:
                        walls.append(robot_position + 1)
                    elif robot_orientation == direction.EAST:
                        walls.append(robot_position - rows)
                    elif robot_orientation == direction.SOUTH:
                        walls.append(robot_position - 1)
                    elif robot_orientation == direction.WEST:
                        walls.append(robot_position + rows)         
                case 'back wall':
                    if robot_orientation == direction.NORTH:
                        walls.append(robot_position - rows)
                    elif robot_orientation == direction.EAST:
                        walls.append(robot_position - 1)
                    elif robot_orientation == direction.SOUTH:
                        walls.append(robot_position + rows)
                    elif robot_orientation == direction.WEST:
                        walls.append(robot_position + 1) 
    
    maze_map[robot_position] = walls

    return maze_map

''' where_to_move TODO works only for 16x16 maze
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
def where_to_move_graph(robot_position, current_destination):

    x = current_destination - robot_position
    match x:
        case -16:
            move_direction = direction.SOUTH
        case -1:
            move_direction = direction.WEST
        case 1:
            move_direction = direction.EAST
        case 16:
            move_direction = direction.NORTH

    return move_direction


def move_back(destination, maze_map, robot_position, intersection, intersection_number, intersection_count, robot_orientation,\
               robot, ps, tof, left_motor, right_motor, ps_left, ps_right, path):
    while destination not in maze_map[robot_position]:
        for cell in reversed(intersection[intersection_number]):
            
            robot_position, robot_orientation = BFS_functions.move_one_position(cell, robot_position, robot_orientation, robot,\
                                                                ps, tof, left_motor, right_motor, ps_left, ps_right) 

            intersection[intersection_number].pop()
            path.pop()

        intersection_count[intersection_number] -= 1
        if intersection_count[intersection_number] == 0:
                intersection_number -= 1

    return intersection, intersection_number,intersection_count, path, robot_orientation, robot_position
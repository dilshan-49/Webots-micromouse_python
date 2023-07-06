from controller import Robot, Keyboard
from collections import namedtuple, deque
from threading import Thread
#my modules
from Constants import *
import map_functions
import move_functions
import algorythm_functions
import draw_maze
import var
import DFS_functions

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

def check_possible_routes(maze_map, robot_position, visited, queue, cross, target):
    deadend = True
    searching_end = False
    for n in maze_map[robot_position]:
        if n not in visited:
            visited.append(n)
            queue.append(n)
            deadend = False
            if n == target:
                searching_end = True
                break
    
    if searching_end:
        current_destination = queue[-1]
    elif cross or deadend:
        current_destination = queue[0]
    else:
        current_destination = queue[-1]
    
    return current_destination, visited, queue, deadend, searching_end


def bfs_back(graph, start, target):
    visited = []

    queue = deque()
    path = []
    parent = {}
    visited.append(start)
    queue.append(start)
    parent[start] = start

    while queue:
        # popleft is O(1)
        s = queue.popleft()

        for n in graph[s]:
            if n not in visited:
                visited.append(n)
                queue.append(n)
                parent[n] = s
                if n == target:
                    while parent[n] != n:
                        path.append(n)
                        n = parent[n]
    return path
                
def move_one_position(current_destination, robot_position, robot_orientation, robot, ps, tof, left_motor, right_motor, ps_left, ps_right):
    
    move_direction = DFS_functions.where_to_move_graph(robot_position, current_destination)
    
    _, front_wall, _, _, _, _ = map_functions.detect_walls(robot, ps, 5)
    if front_wall:
        move_functions.move_front_correct(tof, left_motor, right_motor, robot, ps)
    
    robot_orientation =  move_functions.move(robot_orientation, move_direction,\
                                            robot, left_motor, right_motor, ps_left, ps_right, ps) #git

    robot_position = current_destination
    
    return robot_position, robot_orientation
from controller import Robot, Keyboard
from collections import namedtuple, deque
from threading import Thread
from pathlib import Path
#my modules
from Constants import *
import map_functions
import move_functions
import algorythm_functions
import draw_maze
import var
import map_functions
import DFS_functions
import BFS_functions

def floodfill_main(robot):

    left_motor, right_motor, ps_left, ps_right, ps, tof = init_devices(robot)

    maze_map = [0] * maze_parameters.MAZE_SIZE
    distance = [255] * maze_parameters.MAZE_SIZE

    target = maze_parameters.TARGET_CELL            # robot start target
    robot_position  = maze_parameters.START_CELL    # robot start position
    move_direction = direction.NORTH                # where robot wants to move on start
    start = 1                                       # to open file 1 time
    robot_orientation = direction.NORTH             # robot start orientation
    maze_map = map_functions.init_maze_map(maze_map)
    var.maze_map_global = maze_map

    while robot.step(TIME_STEP) != -1:
            
            if mode_params.TESTING:
                print('sensor tof %.2f'% tof.getValue()) #do usuniecia

            if mode_params.TESTING:
                print('sensor ps6 left %.2f'% ps[6].getValue()) #do usuniecia
            
            if mode_params.TESTING:
                print('sensor ps1 right %.2f'% ps[1].getValue()) #do usuniecia

            match mode_params.MODE:
                case 2: #search
                    
                    if start:
                        #run in another thread to make it possible to look on it during robot run
                        Maze_thread = Thread(target = draw_maze.draw_maze, args = (var.maze_map_global, var.distance_global), daemon = True)
                        Maze_thread.start()
                        
                        start = 0
                    if mode_params.TESTING:
                        timer = robot.getTime()

                    left_wall, front_wall, right_wall, back_wall, avg5_left_sensor, avg2_right_sensor = map_functions.detect_walls(robot, ps, 5)

                    if left_wall:
                        maze_map = map_functions.add_wall(maze_map, robot_position, robot_orientation, direction.WEST)
                    
                    if front_wall:
                        maze_map = map_functions.add_wall(maze_map, robot_position, robot_orientation, direction.NORTH)
                        move_functions.move_front_correct(tof, left_motor, right_motor, robot, ps)

                    if right_wall:
                        maze_map = map_functions.add_wall(maze_map, robot_position, robot_orientation, direction.EAST)

                    if back_wall:
                        maze_map = map_functions.add_wall(maze_map, robot_position, robot_orientation, direction.SOUTH)

                    distance = map_functions.init_distance_map(distance, target) #reset path

                    distance = algorythm_functions.floodfill(maze_map, distance) #path

                    var.robot_pos = robot_position

                    var.maze_map_global = maze_map

                    if var.distance_global != distance:
                        var.distance_global = distance
                        var.distance_update = True

                    var.target_global = target
                    var.drawing_event.set()
                    
                    if var.searching_end:
                        print('Target reached')
                        print('Searching time: %.2f'% robot.getTime(),'s')
                        input("press any key to end")
                        exit(0)

                    move_direction = algorythm_functions.where_to_move(maze_map, robot_position, distance, robot_orientation)

                    robot_orientation =  move_functions.move(robot_orientation, move_direction,\
                                                            robot, left_motor, right_motor, ps_left, ps_right, ps)
                    
                    if mode_params.TESTING:
                        timer = robot.getTime() - timer
                        print('Move time: %.2f'% timer,'s')

                    robot_position = algorythm_functions.change_position(robot_position, robot_orientation)
                    
                    maze_map[robot_position] = maze_map[robot_position] | maze_parameters.VISITED  #mark visited tile

                    if robot_position == target:
                        target = algorythm_functions.change_target(maze_map, robot_position, distance, target)
                    
                    var.main_event.wait()
                    var.main_event.clear()

                case 3: #speedrun

                    if start:
                        distance = algorythm_functions.read_file('floodfill_path.pkl')
                        maze_map = algorythm_functions.read_file('floodfill_maze.pkl')

                        #run in another thread to make it possible to look on it during robot run
                        Maze_thread = Thread(target = draw_maze.draw_maze, args = (maze_map, distance), daemon = True)
                        Maze_thread.start()
                        
                        start = 0

                    move_direction = algorythm_functions.where_to_move(maze_map, robot_position, distance, robot_orientation)

                    robot_orientation =  move_functions.move(robot_orientation, move_direction,\
                                                            robot, left_motor, right_motor, ps_left, ps_right, ps)
                    
                    robot_position = algorythm_functions.change_position(robot_position, robot_orientation)
                    
                    var.robot_pos = robot_position

                    var.drawing_event.set()
                    
                    var.main_event.wait()
                    var.main_event.clear()

                    if robot_position == target:
                        print('Target reached')
                        print('Speedrun time: %.2f'% robot.getTime(),'s')
                        input("press any key to end")
                        exit(0)


def DFS_main(robot):

    left_motor, right_motor, ps_left, ps_right, ps, tof = init_devices(robot)

    maze_map2 = DFS_functions.init_maze_map_graph()
    maze_map = DFS_functions.init_maze_map_graph2()
    target = maze_parameters.TARGET_CELL            # robot start target
    robot_position  = maze_parameters.START_CELL    # robot start position
    move_direction = direction.NORTH                # where robot wants to move on start
    start = 1                                       # to open file 1 time TODO
    robot_orientation = direction.NORTH             # robot start orientation
    var.maze_map_global = maze_map2

    #dfs vars
    intersection_number = -1
    intersection_count = {}
    intersection = {}
    visited = []
    stack = []
    path = []
    visited.append(robot_position)
    stack.append(robot_position) 

    while robot.step(TIME_STEP) != -1:
        if mode_params.TESTING:
            print('sensor tof %.2f'% tof.getValue()) #do usuniecia

        if mode_params.TESTING:
            print('sensor ps6 left %.2f'% ps[6].getValue()) #do usuniecia
        
        if mode_params.TESTING:
            print('sensor ps1 right %.2f'% ps[1].getValue()) #do usuniecia

        match mode_params.MODE:
            case 2: #search
                
                if start:
                    #run in another thread to make it possible to look on it during robot run
                    Maze_thread = Thread(target = draw_maze.draw_maze, args = (var.maze_map_global, []), daemon = True)
                    Maze_thread.start()
                    
                    start = 0
                if mode_params.TESTING:
                    timer = robot.getTime()
                
                while stack:
                    stack.pop()
                    
                    left_wall, front_wall, right_wall, back_wall, _, _ = map_functions.detect_walls(robot, ps, 5)
                    walls = {'front wall': front_wall,'right wall': right_wall, 'back wall': back_wall, 'left wall': left_wall}
                    
                    maze_map = DFS_functions.add_walls_graph(maze_map, robot_position, robot_orientation, walls)
                    
                    path.append(robot_position)
                    
                    var.robot_pos = robot_position

                    var.maze_map_global = maze_map
                    var.drawing_event.set()

                    if robot_position == target:
                        print('Target reached')
                        print('Searching time: %.2f'% robot.getTime(),'s')
                        algorythm_functions.write_file('DFS_path.pkl', path)
                        algorythm_functions.write_file('DFS_maze.pkl', maze_map)
                        input("press any key to end")
                        exit(0)
                    
                    routes = len(maze_map[robot_position])
                    if routes >= 3:
                        intersection_number += 1
                    
                    if intersection_number > -1:
                        if routes >= 3:
                            intersection[intersection_number] = [robot_position]
                            if routes == 3:
                                intersection_count[intersection_number] = 1
                            else:
                                intersection_count[intersection_number] = 2
                        elif routes == 2:
                            intersection[intersection_number].append(robot_position)
                        else:
                            intersection, intersection_number, intersection_count, path, robot_orientation, robot_position = \
                                DFS_functions.move_back(stack[-1], maze_map, robot_position, intersection, intersection_number, intersection_count, robot_orientation,\
                                                        robot, ps, tof, left_motor, right_motor, ps_left, ps_right, path)
                            
                            intersection[intersection_number].append(path[-1])
                    
                    for cell in reversed(maze_map[robot_position]):
                        if cell not in visited:
                            visited.append(cell)
                            stack.append(cell)
                            if cell == target:
                                break
                    
                    current_destination = stack[-1]
                    
                    if current_destination not in maze_map[robot_position]:
                        intersection[intersection_number].pop()
                        intersection, intersection_number, intersection_count, path, robot_orientation, robot_position = \
                            DFS_functions.move_back(current_destination, maze_map, robot_position, intersection, intersection_number, intersection_count, robot_orientation,\
                                                    robot, ps, tof, left_motor, right_motor, ps_left, ps_right, path)
                        intersection[intersection_number].append(robot_position)

                    robot_position, robot_orientation = BFS_functions.move_one_position(current_destination, robot_position, robot_orientation, robot,\
                                                                        ps, tof, left_motor, right_motor, ps_left, ps_right)  
                    
                    if mode_params.TESTING:
                        timer = robot.getTime() - timer
                        print('Move time: %.2f'% timer,'s')
                    
                    var.main_event.wait()
                    var.main_event.clear()

            case 3: #speedrun

                if start:
                    path = algorythm_functions.read_file('DFS_path.pkl')
                    path.reverse()
                    path.pop() #remove start cell
                    
                    maze_map = algorythm_functions.read_file('DFS_maze.pkl')
                    var.maze_map_global = maze_map
                    
                    #run in another thread to make it possible to look on it during robot run
                    Maze_thread = Thread(target = draw_maze.draw_maze, args = (maze_map, []), daemon = True)
                    Maze_thread.start()
                    
                    start = 0

                while path:
                    current_destination = path.pop()
                    move_direction = DFS_functions.where_to_move_graph(robot_position, current_destination)

                    robot_orientation =  move_functions.move(robot_orientation, move_direction,\
                                                            robot, left_motor, right_motor, ps_left, ps_right, ps)
                    
                    
                    robot_position = current_destination
                    
                    var.robot_pos = robot_position

                    var.drawing_event.set()
                    
                    var.main_event.wait()
                    var.main_event.clear()

                    if robot_position == target:
                        print('Target reached')
                        print('Speedrun time: %.2f'% robot.getTime(),'s')
                        input("press any key to end")
                        exit(0)

def BFS_main(robot):

    left_motor, right_motor, ps_left, ps_right, ps, tof = init_devices(robot)

    maze_map2 = DFS_functions.init_maze_map_graph()
    maze_map = DFS_functions.init_maze_map_graph2()
    
    target = maze_parameters.TARGET_CELL            # robot start target
    robot_position  = maze_parameters.START_CELL    # robot start position
    move_direction = direction.NORTH                # where robot wants to move on start
    start = 1                                       # to open file 1 time TODO
    robot_orientation = direction.NORTH             # robot start orientation
    var.maze_map_global = maze_map2

    #bfs vars
    visited = []
    path = []
    searching_end = False
    moved_back = False
    cross = False
    queue = deque()

    visited.append(robot_position) 
    queue.append(robot_position)

    while robot.step(TIME_STEP) != -1:
        if mode_params.TESTING:
            print('sensor tof %.2f'% tof.getValue()) #do usuniecia

        if mode_params.TESTING:
            print('sensor ps6 left %.2f'% ps[6].getValue()) #do usuniecia
        
        if mode_params.TESTING:
            print('sensor ps1 right %.2f'% ps[1].getValue()) #do usuniecia

        match mode_params.MODE:
            case 2: #search
                
                if start:
                    #run in another thread to make it possible to look on it during robot run
                    Maze_thread = Thread(target = draw_maze.draw_maze, args = (var.maze_map_global, []), daemon = True)
                    Maze_thread.start()
                    
                    start = 0
                if mode_params.TESTING:
                    timer = robot.getTime()
                
                while queue:
                    if searching_end:
                        robot_position = queue.pop()
                    elif moved_back or cross:
                        robot_position = queue.popleft()
                        moved_back = False
                    else:
                        robot_position = queue.pop()
                    
                    left_wall, front_wall, right_wall, back_wall, _, _ = map_functions.detect_walls(robot, ps, 5)
                    walls = {'front wall': front_wall,'right wall': right_wall, 'back wall': back_wall, 'left wall': left_wall}
                    
                    maze_map = DFS_functions.add_walls_graph(maze_map, robot_position, robot_orientation, walls)
                    
                    path.append(robot_position)
                    
                    var.robot_pos = robot_position

                    var.maze_map_global = maze_map
                    var.drawing_event.set()

                    if robot_position == target:
                        print('Target reached')
                        print('Searching time: %.2f'% robot.getTime(),'s')
                        path2 = BFS_functions.bfs_back(maze_map, maze_parameters.START_CELL, target)
                        algorythm_functions.write_file('BFS_path.pkl', path2)
                        algorythm_functions.write_file('BFS_maze.pkl', maze_map)
                        input("press any key to end")
                        exit(0)
                    
                    routes = len(maze_map[robot_position])
                    cross = (routes >= 3)
                    
                    current_destination, visited, queue, moved_back, searching_end = BFS_functions.check_possible_routes(maze_map, robot_position, visited, queue, cross, target)
                    
                    if current_destination not in maze_map[robot_position]: #not adjacent cell e.g. we move back farther than 1 cell      
                        temp_graph = {}
                        for cell in visited:#creaty sub-graph only from visited cells
                            temp_graph[cell] = maze_map[cell]
                        
                        back_path = BFS_functions.bfs_back(temp_graph, robot_position, current_destination)
                        
                        for n in reversed(back_path):
                            Move_to = back_path.pop()

                            robot_position, robot_orientation = BFS_functions.move_one_position(Move_to, robot_position, robot_orientation, robot,\
                                                                              ps, tof, left_motor, right_motor, ps_left, ps_right)
                            if n not in path:
                                break
                            path.pop()

                        while back_path:
                            path.append(Move_to)
                            Move_to = back_path.pop()
                            robot_position, robot_orientation = BFS_functions.move_one_position(Move_to, robot_position, robot_orientation, robot,\
                                                                              ps, tof, left_motor, right_motor, ps_left, ps_right)
                    else:
                        robot_position, robot_orientation = BFS_functions.move_one_position(current_destination, robot_position, robot_orientation, robot,\
                                                                          ps, tof, left_motor, right_motor, ps_left, ps_right)

                    if mode_params.TESTING:
                        timer = robot.getTime() - timer
                        print('Move time: %.2f'% timer,'s')
                    
                    var.main_event.wait()
                    var.main_event.clear()

            case 3: #speedrun

                if start:
                    path = algorythm_functions.read_file('BFS_path.pkl')
                    
                    maze_map = algorythm_functions.read_file('BFS_maze.pkl')
                    var.maze_map_global = maze_map
                    
                    #run in another thread to make it possible to look on it during robot run
                    Maze_thread = Thread(target = draw_maze.draw_maze, args = (maze_map, []), daemon = True)
                    Maze_thread.start()
                    
                    start = 0

                while path:
                    current_destination = path.pop()
                    move_direction = DFS_functions.where_to_move_graph(robot_position, current_destination)

                    robot_orientation =  move_functions.move(robot_orientation, move_direction,\
                                                            robot, left_motor, right_motor, ps_left, ps_right, ps)
                    
                    
                    robot_position = current_destination
                    
                    var.robot_pos = robot_position

                    var.drawing_event.set()
                    
                    var.main_event.wait()
                    var.main_event.clear()

                    if robot_position == target:
                        print('Target reached')
                        print('Speedrun time: %.2f'% robot.getTime(),'s')
                        input("press any key to end")
                        exit(0)

def keyboard_main(robot):

    left_motor, right_motor, ps_left, ps_right, ps, tof = init_devices(robot)
    
    keyboard = Keyboard()
    keyboard.enable(TIME_STEP)

    while robot.step(TIME_STEP) != -1:

        if mode_params.TESTING:
            print('sensor tof %.2f'% tof.getValue()) #do usuniecia

        if mode_params.TESTING:
            print('sensor ps6 left %.2f'% ps[6].getValue()) #do usuniecia
        
        if mode_params.TESTING:
            print('sensor ps1 right %.2f'% ps[1].getValue()) #do usuniecia

        key = keyboard.get_key()
        if key in keys:
            match key:
                case keys.forward:
                    print(key)
                    move_functions.move_1_tile(robot, left_motor, right_motor, ps_left, ps_right, ps)
                case keys.right | keys.left | keys.back:
                    print(key)
                    move_functions.turn(robot, key, left_motor, right_motor, ps_left, ps_right)


def init_devices(robot):
    left_motor = robot.getDevice('left wheel motor')
    right_motor = robot.getDevice('right wheel motor')

    left_motor.setVelocity(robot_parameters.SPEED)
    right_motor.setVelocity(robot_parameters.SPEED)

    ps_left = robot.getDevice("left wheel sensor")
    ps_left.enable(TIME_STEP)
    ps_right = robot.getDevice("right wheel sensor")
    ps_right.enable(TIME_STEP)

    ps = [''] * 8
    ps_names = (
        "ps0", "ps1", "ps2", "ps3",
          "ps4", "ps5", "ps6", "ps7"
    )
    for i in range(len(ps_names)):
        ps[i] = robot.getDevice(ps_names[i])
        ps[i].enable(TIME_STEP)
    
    tof = robot.getDevice('tof')
    tof.enable(TIME_STEP)
    
    return left_motor, right_motor, ps_left, ps_right, ps, tof

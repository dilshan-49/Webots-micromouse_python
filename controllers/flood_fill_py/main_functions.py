from controller import Robot, Keyboard
from collections import namedtuple, deque
from threading import Thread
#my modules
from Constants import *
import map_functions as map_f
import move_functions as move_f
import algorithm_functions as algorithm_f
import draw_maze
import var


''' floodfill_main
# @brief Main program for floodfill algorithm controller. 
#
# @param robot: object with robot instance
#
# @retval None
'''     
def floodfill_main(robot):

    left_motor, right_motor, ps_left, ps_right, ps, tof = init_devices(robot)
    target, robot_position, start, robot_orientation = init_parameters()

    maze_map = [0] * maze_parameters.MAZE_SIZE
    distance = [255] * maze_parameters.MAZE_SIZE

    maze_map = map_f.init_maze_map(maze_map)

    var.maze_map_global = maze_map

    floodfill_path_file = 'Results/floodfill_path.pkl'
    floodfill_maze_file = 'Results/floodfill_maze.pkl'

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
                        
                        start = False
                    if mode_params.TESTING:
                        timer = robot.getTime()

                    left_wall, front_wall, right_wall, back_wall = map_f.detect_walls(robot, ps, tof, 5)

                    if left_wall:
                        maze_map = map_f.add_wall(maze_map, robot_position, robot_orientation, direction.WEST)
                    
                    if front_wall:
                        maze_map = map_f.add_wall(maze_map, robot_position, robot_orientation, direction.NORTH)

                    if right_wall:
                        maze_map = map_f.add_wall(maze_map, robot_position, robot_orientation, direction.EAST)

                    if back_wall:
                        maze_map = map_f.add_wall(maze_map, robot_position, robot_orientation, direction.SOUTH)

                    distance = map_f.init_distance_map(distance, target) #reset path

                    distance = algorithm_f.floodfill(maze_map, distance) #path

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
                        algorithm_f.write_file(floodfill_path_file, distance)
                        algorithm_f.write_file(floodfill_maze_file, maze_map)
                        input("press any key to end")
                        exit(0)
                    
                    robot_position, robot_orientation = \
                        move_f.move_one_position(maze_map[robot_position], distance, robot_position, robot_orientation, robot,\
                                                 ps, tof, left_motor, right_motor, ps_left, ps_right)
                    
                    if mode_params.TESTING:
                        timer = robot.getTime() - timer
                        print('Move time: %.2f'% timer,'s')
                    
                    maze_map[robot_position] |= maze_parameters.VISITED  #mark visited tile

                    if robot_position == target:
                        target, maze_map = algorithm_f.change_target(maze_map, robot_position, distance, target)
                    
                    var.main_event.wait()
                    var.main_event.clear()

                case 3: #speedrun

                    if start:
                        distance = algorithm_f.read_file(floodfill_path_file)
                        maze_map = algorithm_f.read_file(floodfill_maze_file)

                        #run in another thread to make it possible to look on it during robot run
                        Maze_thread = Thread(target = draw_maze.draw_maze, args = (maze_map, distance), daemon = True)
                        Maze_thread.start()
                        
                        start = 0

                    robot_position, robot_orientation = \
                        move_f.move_one_position(maze_map[robot_position], distance, robot_position, robot_orientation, robot,\
                                                ps, tof, left_motor, right_motor, ps_left, ps_right)
                    
                    var.robot_pos = robot_position

                    var.drawing_event.set()
                    
                    var.main_event.wait()
                    var.main_event.clear()

                    if robot_position == target:
                        print('Target reached')
                        print('Speedrun time: %.2f'% robot.getTime(),'s')
                        input("press any key to end")
                        exit(0)


''' DFS_main
# @brief Main program for Deep first search algorithm controller.
#
# @param robot: object with robot instance
#
# @retval None
'''    
def DFS_main(robot):

    left_motor, right_motor, ps_left, ps_right, ps, tof = init_devices(robot)
    target, robot_position, start, robot_orientation = init_parameters()

    maze_map = map_f.init_maze_map_graph()

    var.maze_map_global = maze_map

    DFS_path_file = 'Results/DFS_path.pkl'
    DFS_maze_file = 'Results/DFS_maze.pkl'

    #dfs vars
    fork_number = -1
    fork_count = {}
    fork = {}
    visited = []
    stack = []
    path = []
    visited.append(robot_position)
    stack.append(robot_position) 


    match mode_params.MODE:
        case 2: #search
            
            if start:
                #run in another thread to make it possible to look on it during robot run
                Maze_thread = Thread(target = draw_maze.draw_maze, args = (var.maze_map_global, []), daemon = True)
                Maze_thread.start()
                
                start = False
            
            if mode_params.TESTING:
                timer = robot.getTime()
            
            while stack:
                
                if robot.step(TIME_STEP) == -1:
                    break
                
                stack.pop()
                
                left_wall, front_wall, right_wall, back_wall = map_f.detect_walls(robot, ps, tof, 5)
                walls = {'front wall': front_wall,'right wall': right_wall, 'back wall': back_wall, 'left wall': left_wall}
                
                maze_map = map_f.add_walls_graph(maze_map, robot_position, robot_orientation, walls)
                
                path.append(robot_position)
                
                var.robot_pos = robot_position
                var.maze_map_global = maze_map

                var.drawing_event.set()

                if robot_position == target:
                    print('Target reached')
                    print('Searching time: %.2f'% robot.getTime(),'s')
                    algorithm_f.write_file(DFS_path_file, path)
                    algorithm_f.write_file(DFS_maze_file, maze_map)
                    input("press any key to end")
                    exit(0)
                
                fork, fork_number, fork_count, dead_end = algorithm_f.check_fork(maze_map[robot_position], robot_position, fork, fork_number, fork_count)
                
                if dead_end:
                    fork, fork_number, fork_count, path, robot_orientation, robot_position = \
                        move_f.move_back(stack[-1], maze_map, robot_position, fork, fork_number, fork_count, robot_orientation,\
                                                robot, ps, tof, left_motor, right_motor, ps_left, ps_right, path)
                    fork[fork_number].append(path[-1])
                            
                current_destination, visited, stack =\
                        algorithm_f.check_possible_routes_DFS(maze_map[robot_position], visited, stack, target)
                
                if current_destination not in maze_map[robot_position]:
                    fork[fork_number].pop()
                    fork, fork_number, fork_count, path, robot_orientation, robot_position = \
                        move_f.move_back(current_destination, maze_map, robot_position, fork, fork_number, fork_count, robot_orientation,\
                                                robot, ps, tof, left_motor, right_motor, ps_left, ps_right, path)
                    fork[fork_number].append(robot_position)

                robot_position, robot_orientation = move_f.move_one_position_graph(current_destination, robot_position, robot_orientation, robot,\
                                                                    ps, tof, left_motor, right_motor, ps_left, ps_right)  
                

                if mode_params.TESTING:
                    timer = robot.getTime() - timer
                    print('Move time: %.2f'% timer,'s')
                
                var.main_event.wait()
                var.main_event.clear()

        case 3: #speedrun

            if start:
                path = algorithm_f.read_file(DFS_path_file)
                path.reverse()
                path.pop() #remove start cell
                
                maze_map = algorithm_f.read_file(DFS_maze_file)
                var.maze_map_global = maze_map
                
                #run in another thread to make it possible to look on it during robot run
                Maze_thread = Thread(target = draw_maze.draw_maze, args = (maze_map, []), daemon = True)
                Maze_thread.start()
                
                start = 0

            while path:
                
                if robot.step(TIME_STEP) == -1:
                    break

                current_destination = path.pop()
                
                robot_position, robot_orientation = move_f.move_one_position_graph(current_destination, robot_position, robot_orientation, robot,\
                                                                    ps, tof, left_motor, right_motor, ps_left, ps_right)
                
                var.robot_pos = robot_position

                var.drawing_event.set()
                
                var.main_event.wait()
                var.main_event.clear()

                if robot_position == target:
                    print('Target reached')
                    print('Speedrun time: %.2f'% robot.getTime(),'s')
                    input("press any key to end")
                    exit(0)


''' BFS_main
# @brief Main program for Breadth first search algorithm controller.
#
# @param robot: object with robot instance
#
# @retval None
'''   
def BFS_main(robot):

    left_motor, right_motor, ps_left, ps_right, ps, tof = init_devices(robot)
    target, robot_position, start, robot_orientation = init_parameters()

    maze_map = map_f.init_maze_map_graph()

    var.maze_map_global = maze_map
    
    BFS_path_file = 'Results/BFS_path.pkl'
    BFS_maze_file = 'Results/BFS_maze.pkl'

    #bfs vars
    visited = []
    path = []
    searching_end = False
    move_back = False
    fork = False
    queue = deque()

    visited.append(robot_position) 
    queue.append(robot_position)


    match mode_params.MODE:
        case 2: #search
            
            if start:
                #run in another thread to make it possible to look on it during robot run
                Maze_thread = Thread(target = draw_maze.draw_maze, args = (var.maze_map_global, []), daemon = True)
                Maze_thread.start()
                
                start = False
            if mode_params.TESTING:
                timer = robot.getTime()
            
            while queue:
                
                if robot.step(TIME_STEP) == -1:
                    break

                if searching_end:
                    robot_position = queue.pop()
                elif move_back or fork:
                    robot_position = queue.popleft()
                    move_back = False
                else:
                    robot_position = queue.pop()
                
                left_wall, front_wall, right_wall, back_wall = map_f.detect_walls(robot, ps, tof, 5)
                walls = {'front wall': front_wall,'right wall': right_wall, 'back wall': back_wall, 'left wall': left_wall}
                
                maze_map = map_f.add_walls_graph(maze_map, robot_position, robot_orientation, walls)
                
                path.append(robot_position)
                
                var.robot_pos = robot_position

                var.maze_map_global = maze_map
                var.drawing_event.set()

                if robot_position == target:
                    print('Target reached')
                    print('Searching time: %.2f'% robot.getTime(),'s')
                    path2 = algorithm_f.get_backward_path(maze_map, maze_parameters.START_CELL, target)
                    algorithm_f.write_file(BFS_path_file, path2)
                    algorithm_f.write_file(BFS_maze_file, maze_map)
                    input("press any key to end")
                    exit(0)
                
                routes = len(maze_map[robot_position])
                fork = (routes >= 3)
                
                current_destination, visited, queue, move_back, searching_end =\
                        algorithm_f.check_possible_routes_BFS(maze_map[robot_position], visited, queue, fork, target)
                
                if current_destination not in maze_map[robot_position]: #not adjacent cell e.g. we move back farther than 1 cell      
                    temp_graph = {}
                    for cell in visited:#creaty sub-graph only from visited cells
                        temp_graph[cell] = maze_map[cell]
                    
                    back_path = algorithm_f.get_backward_path(temp_graph, robot_position, current_destination)
                    
                    for n in reversed(back_path):
                        Move_to = back_path.pop()

                        robot_position, robot_orientation = move_f.move_one_position_graph(Move_to, robot_position, robot_orientation, robot,\
                                                                            ps, tof, left_motor, right_motor, ps_left, ps_right)
                        if n not in path:
                            break
                        path.pop()

                    while back_path:
                        path.append(Move_to)
                        Move_to = back_path.pop()
                        robot_position, robot_orientation = move_f.move_one_position_graph(Move_to, robot_position, robot_orientation, robot,\
                                                                            ps, tof, left_motor, right_motor, ps_left, ps_right)
                else:
                    robot_position, robot_orientation = move_f.move_one_position_graph(current_destination, robot_position, robot_orientation, robot,\
                                                                        ps, tof, left_motor, right_motor, ps_left, ps_right)

                if mode_params.TESTING:
                    timer = robot.getTime() - timer
                    print('Move time: %.2f'% timer,'s')
                
                var.main_event.wait()
                var.main_event.clear()

        case 3: #speedrun

            if start:
                path = algorithm_f.read_file(BFS_path_file)
                
                maze_map = algorithm_f.read_file(BFS_maze_file)
                var.maze_map_global = maze_map
                
                #run in another thread to make it possible to look on it during robot run
                Maze_thread = Thread(target = draw_maze.draw_maze, args = (maze_map, []), daemon = True)
                Maze_thread.start()
                
                start = 0

            while path:

                if robot.step(TIME_STEP) == -1:
                    break

                current_destination = path.pop()
                
                robot_position, robot_orientation = move_f.move_one_position_graph(current_destination, robot_position, robot_orientation, robot,\
                                                                    ps, tof, left_motor, right_motor, ps_left, ps_right)
                
                var.robot_pos = robot_position

                var.drawing_event.set()
                
                var.main_event.wait()
                var.main_event.clear()

                if robot_position == target:
                    print('Target reached')
                    print('Speedrun time: %.2f'% robot.getTime(),'s')
                    input("press any key to end")
                    exit(0)


''' keyboard_main
# @brief Main program for manual/with arrows controller.
#
# @param robot: object with robot instance
#
# @retval None
'''   
def keyboard_main(robot):

    left_motor, right_motor, ps_left, ps_right, ps, tof = init_devices(robot)
    
    keyboard = Keyboard()
    keyboard.enable(TIME_STEP)
    max_tof = 0
    while robot.step(TIME_STEP) != -1:

        if mode_params.TESTING:
            avg_front_sensor = 0
            for i in range(0,3): #more scans for better accuracy
                
                avg_front_sensor += tof.getValue()

                robot.step(TIME_STEP) #simulation update
            
            avg_front_sensor = avg_front_sensor / 3
            # x = tof.getValue()
            print('sensor tof %.2f'% avg_front_sensor) #do usuniecia
            if avg_front_sensor > max_tof:
                max_tof = avg_front_sensor
            print('max tof %.2f'% max_tof)

        # if mode_params.TESTING:
        #     print('sensor ps6 left %.2f'% ps[6].getValue()) #do usuniecia
        
        # if mode_params.TESTING:
        #     print('sensor ps1 right %.2f'% ps[1].getValue()) #do usuniecia

        key = keyboard.get_key()
        if key in keys:
            match key:
                case keys.forward:
                    print(key)
                    move_f.move_1_tile(robot, left_motor, right_motor, ps_left, ps_right, ps)
                case keys.right | keys.left | keys.back:
                    print(key)
                    move_f.turn(robot, key, left_motor, right_motor, ps_left, ps_right)


''' init_devices
# @brief Init robot peripherals.
#
# @param robot: object with robot instance
#
# @retval left_motor: object with left motor instance
# @retval right_motor: object with right motor instance
# @retval ps_left: object with left position sensor instance
# @retval ps_right: object with right position sensor instance
# @retval ps: list of distance IR sensors objects
# @retval tof: object with distance Tof sensor
'''   
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


''' init_parameters
# @brief Init robot peripherals.
#
# @param None
#
# @retval target: variable with target cell
# @retval robot_position: variable with starting robot position
# @retval start: bool variable with start indication
# @retval robot_orientation: variable with starting robot orientation
'''   
def init_parameters():
    
    target = maze_parameters.TARGET_CELL            # robot start target
    robot_position  = maze_parameters.START_CELL    # robot start position
    start = True                                    # to open file 1 time 
    robot_orientation = direction.NORTH             # robot start orientation

    return target, robot_position, start, robot_orientation


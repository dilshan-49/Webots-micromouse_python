"""flood_fill_py controller."""

from controller import Robot, Keyboard
from collections import namedtuple
from threading import Thread, Condition
#my modules
from Constants import *
import map_functions
import move_functions
import algorythm_functions
import draw_maze
import var

if __name__ == "__main__":

    # create the Robot instance.
    robot = Robot()
    
    left_motor = robot.getDevice('left wheel motor')
    right_motor = robot.getDevice('right wheel motor')

    left_motor.setVelocity(robot_parameters.SPEED)
    right_motor.setVelocity(robot_parameters.SPEED)

    ps_left = robot.getDevice("left wheel sensor")
    ps_left.enable(TIME_STEP)
    ps_right = robot.getDevice("right wheel sensor")
    ps_right.enable(TIME_STEP)

    maze_map = [0] * maze_parameters.MAZE_SIZE
    distance = [255] * maze_parameters.MAZE_SIZE
    
    target = maze_parameters.TARGET_CELL        #robot start target
    robot_position  = 0                          #robot start position
    move_direction = direction.NORTH            #where robot wants to move on start
    mode = robot_parameters.MODE                # 1- keyboard, 2- search, 3 - speeedrun
    open = 1                                    #to open file 1 time
    robot_orientation = direction.NORTH         #robot start orientation
    maze_map = map_functions.init_maze_map(maze_map)
    var.maze_map_global = maze_map
    if robot_parameters.MODE == 1:
        keyboard = Keyboard()
        keyboard.enable(TIME_STEP)

    ps = [''] * 8
    ps_names = (
        "ps0", "ps1", "ps2", "ps3",
          "ps4", "ps5", "ps6", "ps7"
    )
    for i in range(len(ps_names)):
        #ps[i] = robot.getDistanceSensor(ps_names[i])
        ps[i] = robot.getDevice(ps_names[i])
        ps[i].enable(TIME_STEP)
    
    #tof = robot.getDistanceSensor('tof')
    tof = robot.getDevice('tof')
    tof.enable(TIME_STEP)

    while robot.step(TIME_STEP) != -1:
        
        #print('sensor tof {}',tof.getValue()) #do usuniecia
        #print('sensor ps5 {}',ps[5].getValue()) #do usuniecia

        #detect walls
        #left_wall, front_wall, right_wall, back_wall, avg5_left_sensor, avg2_right_sensor = map_functions.detect_walls(robot, ps, 5)
        
        if TESTING:
            print('sensor ps6 left {}',ps[6].getValue()) #do usuniecia
        if TESTING:
            print('sensor ps1 right {}',ps[1].getValue()) #do usuniecia


        match mode:
            case 1: #keyboard
                key = keyboard.get_key()
                if key in keys:
                    match key:
                        case keys.forward:
                            print(key)
                            move_functions.move_1_tile(robot, left_motor, right_motor, ps_left, ps_right, left_wall, right_wall, ps)
                        case keys.right | keys.left | keys.back:
                            print(key)
                            move_functions.turn(robot, key, left_motor, right_motor, ps_left, ps_right)

            case 2: #search
                
                if open:
                    #run in another thread to make it possible to look on it during robot run
                    Maze_thread = Thread(target = draw_maze.draw_maze, args = (var.maze_map_global, var.distance_global, 1), daemon = True)
                    Maze_thread.start()
                    
                    open = 0

                left_wall, front_wall, right_wall, back_wall, avg5_left_sensor, avg2_right_sensor = map_functions.detect_walls(robot, ps, 5)

                if left_wall:
                    map_functions.add_wall(maze_map, robot_position, robot_orientation, direction.WEST)
                
                if front_wall:
                    map_functions.add_wall(maze_map, robot_position, robot_orientation, direction.NORTH)
                
                if right_wall:
                    map_functions.add_wall(maze_map, robot_position, robot_orientation, direction.EAST)

                if back_wall:
                    map_functions.add_wall(maze_map, robot_position, robot_orientation, direction.SOUTH)

                # print('MAZE MAP')
                # map_functions.print_array(maze_map, 0)
                # print('MAZE MAP')

                distance = map_functions.init_distance_map(distance, target) #reset path

                distance = algorythm_functions.floodfill(maze_map, distance) #path

                move_direction = algorythm_functions.where_to_move(maze_map, robot_position, distance, robot_orientation)

                robot_orientation =  move_functions.move(robot_orientation, move_direction,\
                                                        robot, left_motor, right_motor, ps_left, ps_right, ps)

                robot_position = algorythm_functions.change_position(robot_position, robot_orientation)
                
                maze_map[robot_position] = maze_map[robot_position] | maze_parameters.VISITED   #mark visited tile


                if robot_position == target:
                    target = algorythm_functions.change_target(maze_map, robot_position, distance, target)
                
                var.robot_pos = robot_position
                var.maze_map_global = maze_map
                if distance != var.distance_global:
                    var.distance_global = distance
                    var.distance_update = True
                var.target_global = target
                with var.con: #notify maze thread that robot position has changed
                    var.pos_update = True
                    var.con.notify()

            case 3: #speedrun

                if open:
                    distance = algorythm_functions.read_file('path.txt')
                    maze_map = algorythm_functions.read_file('maze.txt')

                    #run in another thread to make it possible to look on it during robot run
                    Maze_thread = Thread(target = draw_maze.draw_maze, args = (maze_map, distance, 0), daemon = True)
                    Maze_thread.start()
                    
                    open = 0

                move_direction = algorythm_functions.where_to_move(maze_map, robot_position, distance, robot_orientation)

                robot_orientation =  move_functions.move(robot_orientation, move_direction,\
                                                        robot, left_motor, right_motor, ps_left, ps_right, ps)
                
                robot_position = algorythm_functions.change_position(robot_position, robot_orientation)
                
                var.robot_pos = robot_position
                with var.con: #notify maze thread that robot position has changed
                    var.pos_update = True
                    var.con.notify()

                if robot_position == target:
                    print('Target reached')
                    input("press any key to end")
                    exit(0)
                    

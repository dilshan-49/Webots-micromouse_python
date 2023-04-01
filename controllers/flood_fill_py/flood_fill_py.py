"""flood_fill_py controller."""

from controller import Robot, Keyboard, Motor, PositionSensor,DistanceSensor
from collections import namedtuple

#my modules
from Constants import *
import map_functions
import move_functions
import algorythm_functions


if __name__ == "__main__":

    # create the Robot instance.
    robot = Robot()



    left_motor = robot.getDevice('left wheel motor')
    right_motor = robot.getDevice('right wheel motor')
    #left_motor.setPosition(float('inf'))
    #right_motor.setPosition(float('inf'))

    ps_left = robot.getPositionSensor("left wheel sensor")
    ps_left.enable(TIME_STEP)
    ps_right = robot.getPositionSensor("right wheel sensor")
    ps_right.enable(TIME_STEP)

    left_motor.setVelocity(3.14)
    right_motor.setVelocity(3.14)
    maze_map = [0] * maze_parameters.MAZE_SIZE
    distance = [255] * maze_parameters.MAZE_SIZE
    
    target = maze_parameters.TARGET_CELL
    robot_position = 0
    move_direction = direction.NORTH #where robot wants to move
    mode = robot_parameters.MODE # 1- keyboard, 2- search, 3 - speeedrun
    open = 1 #to open file 1 time
    robot_orientation = direction.NORTH
    map_functions.init_maze_map(maze_map)
    keyboard = Keyboard()
    keyboard.enable(TIME_STEP)
    keys = ['W', 'A', 'S', 'D']
    
    ps = [''] * 8
    ps_names = (
        "ps0", "ps1", "ps2", "ps3",
          "ps4", "ps5", "ps6", "ps7"
    )
    for i in range(len(ps_names)):
        ps[i] = robot.getDistanceSensor(ps_names[i])
        ps[i].enable(TIME_STEP)
    
    tof = robot.getDistanceSensor('tof')
    tof.enable(TIME_STEP)
    


    while robot.step(TIME_STEP) != -1:
        
        print('sensor tof {}',tof.getValue()) #do usuniecia
        print('sensor ps0 {}',ps[0].getValue()) #do usuniecia

        avg2_right_sensor = 0    #ps2
        avg4_back_sensor = 0     #ps4
        avg5_left_sensor = 0     #ps5
        avg7_front_sensor = 0    #ps7
        number_of_scans = 5

        #read distance sensors
        ps_values = [0] * 8

        for i in range(0,number_of_scans): #more scans for better accuracy
            
            for i in range(0,8):
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

        if left_wall:
            map_functions.add_wall(maze_map, robot_position, robot_orientation, direction.WEST)
        
        if front_wall:
            map_functions.add_wall(maze_map, robot_position, robot_orientation, direction.NORTH)
        
        if right_wall:
            map_functions.add_wall(maze_map, robot_position, robot_orientation, direction.EAST)

        if back_wall:
            map_functions.add_wall(maze_map, robot_position, robot_orientation, direction.SOUTH)
        

        match mode:
            case 1: #keyboard
                key = keyboard.get_key()
                if key in keys:
                    match key:
                        case 'W':
                            print(key)
                            move_functions.move_1_tile(robot, left_motor, right_motor, ps_left, ps_right)
                        case 'D' | 'A' | 'S':
                            print(key)
                            move_functions.turn(robot, key, left_motor, right_motor, ps_left, ps_right)
            case 2: #search

                print('search') #do usuniecia

                print('MAPA')
                map_functions.print_array(maze_map, 0)
                print('MAPA')

                map_functions.init_distance_map(distance, target) #reset path
                #map_functions.print_array(distance, 0)
                algorythm_functions.floodfill(maze_map, 0, distance) #path
                move_direction = algorythm_functions.where_to_move(maze_map, robot_position, distance, robot_orientation)
                
                if robot_orientation == move_direction: #move forward
                    if left_wall and right_wall:
                        #speed_correction
                        move_functions.move_1_tile(robot, left_motor, right_motor, ps_left, ps_right)




            case 3: #speedrun
                print('speedrun')


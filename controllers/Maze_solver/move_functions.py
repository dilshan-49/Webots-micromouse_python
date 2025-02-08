#Move related functions

from math import pi

from Constants import *
from algorithm_functions import change_orientation
import algorithm_functions as algorithm_f
import map_functions as map_f


''' move_one_position_graph
# @brief Executes robot movement to next position. Used in graph algorithms.
#
# @param current_destination: variable with cell to which robot moves
# @param robot_position: variable with current robot position
# @param robot_orientation: variable with current robot orientation in global directions
# @params robot, ps, tof, left_motor, right_motor, ps_left, ps_right: variables with robot devices
#
# @retval robot_position: variable with updated robot position
# @retval robot_orientation: variable with updated robot orientation in global directions
'''
def move_one_position_graph(current_destination, robot_position, robot_orientation, robot, ps, tof, left_motor, right_motor, ps_left, ps_right):
    
    move_direction = algorithm_f.where_to_move_graph(robot_position, current_destination)
    
    _, front_wall, _, _ = map_f.detect_walls(robot, ps, tof, 5)
    if front_wall:
        move_front_correct(tof, left_motor, right_motor, robot, ps)
    
    robot_orientation = drive(robot_orientation, move_direction,\
                                            robot, left_motor, right_motor, ps_left, ps_right, ps)

    robot_position = current_destination
    
    return robot_position, robot_orientation


''' move_one_position
# @brief Executes robot movement to next position. Used in floodfill
#
# @param walls: variable with walls in current robot position
# @param robot_position: variable with current robot position
# @param robot_orientation: variable with current robot orientation in global directions
# @params robot, ps, tof, left_motor, right_motor, ps_left, ps_right: variables with robot devices
#
# @retval robot_position: variable with updated robot position
# @retval robot_orientation: variable with updated robot orientation in global directions
'''
def move_one_position(walls, distance, robot_position, robot_orientation, robot, ps, tof, left_motor, right_motor, ps_left, ps_right):
    
    move_direction = algorithm_f.where_to_move(walls, robot_position, distance, robot_orientation)
    
    _, front_wall, _, _ = map_f.detect_walls(robot, ps, tof, 5)
    
    if front_wall:
        move_front_correct(tof, left_motor, right_motor, robot, ps)
    
    robot_orientation = drive(robot_orientation, move_direction,\
                                            robot, left_motor, right_motor, ps_left, ps_right, ps)
    
    robot_position = algorithm_f.change_position(robot_position, robot_orientation)
    
    return robot_position, robot_orientation


''' drive
# @brief Drive robot motors etc. to actually move based on its orientation and move direction.
#
# @param robot_orientation: variable with actual robot orientation in global directions
# @param move_direction: variable direction where to move in global directions
# @params robot, ps, tof, left_motor, right_motor, ps_left, ps_right: variables with robot devices

# @retval robot_orientation: variable with updated robot orientation in global directions
'''
def drive(robot_orientation, move_direction,\
            robot, left_motor, right_motor, ps_left, ps_right, ps):
    if robot_orientation == move_direction: #move forward
        move_1_tile(robot, left_motor, right_motor, ps_left, ps_right, ps)

    elif (not( (robot_orientation == direction.WEST) and (move_direction == direction.NORTH) ) ) != \
        (not( (robot_orientation // 2) == move_direction) ):   #right, XOR, 'not' to avoid nonzero values
        
        robot_orientation = change_orientation(robot_orientation, moves.right)
        turn(robot, moves.right, left_motor, right_motor, ps_left, ps_right)
        move_1_tile(robot, left_motor, right_motor, ps_left, ps_right, ps)

    elif (not((robot_orientation == direction.NORTH) and (move_direction == direction.WEST))) != \
            (not( (robot_orientation * 2) == move_direction) ): #left, XOR
        
        robot_orientation = change_orientation(robot_orientation, moves.left)
        turn(robot, moves.left, left_motor, right_motor, ps_left, ps_right)
        move_1_tile(robot, left_motor, right_motor, ps_left, ps_right, ps)

    elif ( not( (robot_orientation * 4) == move_direction)) != \
        (not( (robot_orientation // 4) == move_direction) ): #back, XOR

        robot_orientation = change_orientation(robot_orientation, moves.back)
        turn(robot, moves.back, left_motor, right_motor, ps_left, ps_right)
        move_1_tile(robot, left_motor, right_motor, ps_left, ps_right, ps)
    
    return robot_orientation


''' read_sensors
# @brief Read and process left and right sensors for a PID controller.
#
# @params robot, ps: variables with robot devices
# @param number_of_reads: variable which indicates how many times to read sensors
#
# @retval avg1_right_angle_sensor: variable with right angle sensor value
# @retval avg6_left_angle_sensor: variable with left angle sensor value
# @retval left_wall: variable which indicates left wall presence
# @retval right_wall: variable which indicates right wall presence
'''
def read_sensors(robot, ps, number_of_reads):
    
    avg1_right_angle_sensor = 0    #ps1
    avg6_left_angle_sensor = 0     #ps6

    avg2_right_sensor = 0     #ps2
    avg5_left_sensor = 0     #ps5

    #read distance sensors
    for i in range(0,number_of_reads): #more scans for better accuracy
    
        avg1_right_angle_sensor += ps[1].getValue()
        avg6_left_angle_sensor += ps[6].getValue()

        avg2_right_sensor += ps[2].getValue()
        avg5_left_sensor += ps[5].getValue()

        robot.step(TIME_STEP) #simulation update

    #average score of sensors measurements
    avg1_right_angle_sensor = avg1_right_angle_sensor / number_of_reads
    avg6_left_angle_sensor = avg6_left_angle_sensor / number_of_reads
    
    avg2_right_sensor = avg2_right_sensor / number_of_reads
    avg5_left_sensor = avg5_left_sensor / number_of_reads

    left_wall = avg5_left_sensor > 80.0
    right_wall = avg2_right_sensor > 80.0


    return avg1_right_angle_sensor, avg6_left_angle_sensor, left_wall, right_wall


''' PID_correction
# @brief Correct robot position according to distance sensors by changing motors speed.
#
# @params left_motor, right_motor, robot, ps, ps_left, ps_right: variables with robot devices
#
# @retv None
'''
def PID_correction(left_motor, right_motor, robot, ps, ps_left, ps_right):
    
    while True:
        distance_left_now = ps_left.getValue()
        distance_right_now = ps_right.getValue()

        right_angle_sensor, left_angle_sensor, left_wall, right_wall = read_sensors(robot, ps, 2)

        previous_error = 0.00
        error_integral = 0.00
        P = 0.005  #0.005
        I = 0.0008 #0.0005  0.0001
        D = 0.0005 # 0.0002
        Middle = 75
        
        if left_wall and right_wall:
        
            error = left_angle_sensor - right_angle_sensor
            
            if mode_params.TESTING:
                print('error %.3f'% error)

            error_integral += error
            error_derivative = (previous_error - error)
            previous_error = error
            MotorSpeed = P * error + I * error_integral + D * error_derivative
            if MotorSpeed > 0.2:
                MotorSpeed = 0.2
            elif MotorSpeed < -0.2:
                MotorSpeed = -0.2
            
            if mode_params.TESTING:
                print('speed %.3f'% MotorSpeed)

            left_motor.setVelocity(robot_parameters.SPEED + MotorSpeed)
            right_motor.setVelocity(robot_parameters.SPEED - MotorSpeed)
        elif left_wall:
            error = left_angle_sensor - Middle
            
            if mode_params.TESTING:
                print('errorL %.3f'% error)
                
            error_integral += error
            error_derivative = (previous_error - error)
            previous_error = error
            MotorSpeed = P * error + I * error_integral + D * error_derivative
            if MotorSpeed > 0.06:
                MotorSpeed = 0.06
            elif MotorSpeed < -0.06:
                MotorSpeed = -0.06
            
            if mode_params.TESTING:
                print('speed %.3f'% MotorSpeed)

            left_motor.setVelocity(robot_parameters.SPEED + MotorSpeed)
            right_motor.setVelocity(robot_parameters.SPEED - MotorSpeed)
        elif right_wall:
            error = right_angle_sensor - Middle
            
            if mode_params.TESTING:
                print('errorR %.3f'% error)

            error_integral += error
            error_derivative = (previous_error - error)
            previous_error = error
            MotorSpeed = P * error + I * error_integral + D * error_derivative
            if MotorSpeed > 0.06:
                MotorSpeed = 0.06
            elif MotorSpeed < -0.06:
                MotorSpeed = -0.06
            
            if mode_params.TESTING:
                print('speed %.3f'% MotorSpeed)

            left_motor.setVelocity(robot_parameters.SPEED - MotorSpeed)
            right_motor.setVelocity(robot_parameters.SPEED + MotorSpeed)
    
        distance_left_later = ps_left.getValue()
        distance_right_later = ps_right.getValue()

        if (distance_left_now == distance_left_later) and (distance_right_now == distance_right_later):
            break

    
''' move_1_tile
# @brief Drive robot motors and set encoders position
# to move forward by distance of exactly one tile.
#
# @params robot, left_motor, right_motor, ps_left, ps_right, ps: variables with robot devices
#
# @retv None
'''
def move_1_tile(robot, left_motor, right_motor, ps_left, ps_right, ps):
    
    revolutions = maze_parameters.TILE_LENGTH / robot_parameters.WHEEL #rev in radians
    
    left_wheel_revolutions = ps_left.getValue()
    right_wheel_revolutions = ps_right.getValue()

    left_wheel_revolutions += revolutions
    right_wheel_revolutions += revolutions

    left_motor.setVelocity(robot_parameters.SPEED)
    right_motor.setVelocity(robot_parameters.SPEED)

    left_motor.setPosition(left_wheel_revolutions)
    right_motor.setPosition(right_wheel_revolutions)
    PID_correction(left_motor, right_motor, robot, ps, ps_left, ps_right)
    
    if mode_params.TESTING:
        print('forward')

    #wait_move_end(robot, ps_left, ps_right)


''' move_front_correct
# @brief Corrects robot position in reference to front wall.
# Uses front angles IR sensors to straight up robot
# and front tof sensor to correct distance.
#
# @params robot, left_motor, right_motor, tof, ps: variables with robot devices
#
# @retv None
'''
def move_front_correct(tof, left_motor, right_motor, robot, ps):

    left_motor.setPosition(float('inf'))
    right_motor.setPosition(float('inf'))

    left = ps[7].getValue()
    right = ps[0].getValue()

    if left < right:
        while left < right:

            left_motor.setVelocity(robot_parameters.SPEED * 0.1)
            right_motor.setVelocity(robot_parameters.SPEED * -0.1)
            robot.step(TIME_STEP)
            left = ps[7].getValue()
            right = ps[0].getValue()
            if mode_params.TESTING:
                print('sensor angle %.2f'% left, '%.2f'% right)

    elif left > right:
        while left > right:

            left_motor.setVelocity(robot_parameters.SPEED * -0.1)
            right_motor.setVelocity(robot_parameters.SPEED * 0.1)
            robot.step(TIME_STEP)
            left = ps[7].getValue()
            right = ps[0].getValue()
            if mode_params.TESTING:
                print('sensor angle %.2f'% left, '%.2f'% right)

    front = tof.getValue()
    desired_distance = 40.0

    if front > desired_distance:
        while front > desired_distance:

            left_motor.setVelocity(robot_parameters.SPEED * 0.1)
            right_motor.setVelocity(robot_parameters.SPEED * 0.1)
            
            robot.step(TIME_STEP)
            
            front = tof.getValue()

            if mode_params.TESTING:
                print('sensor tof %.2f'% front)

    elif front < desired_distance:
        while front < desired_distance:

            left_motor.setVelocity(robot_parameters.SPEED * -0.1)
            right_motor.setVelocity(robot_parameters.SPEED * -0.1)
            
            robot.step(TIME_STEP)
            
            front = tof.getValue()

            if mode_params.TESTING:
                print('sensor tof %.2f'% front)

    left_motor.setVelocity(0)
    right_motor.setVelocity(0)


''' turn
# @brief Drive robot motors and set encoders position
# to turn by exactly 90 or 180 degrees.
#
# @param move_direction: variable with direction where to move in global directions
# @params robot, left_motor, right_motor, ps_left, ps_right: variables with robot devices
#
# @retv None
'''
def turn(robot, move_direction, left_motor, right_motor, ps_left, ps_right):

    revolutions = (pi/2) * robot_parameters.AXLE / 2 / robot_parameters.WHEEL # in radians

    left_wheel_revolutions = ps_left.getValue()
    right_wheel_revolutions = ps_right.getValue()

    left_motor.setVelocity(robot_parameters.SPEED * 0.33)
    right_motor.setVelocity(robot_parameters.SPEED * 0.33)

    match move_direction:
        case moves.right:
            left_wheel_revolutions += revolutions
            right_wheel_revolutions -= revolutions
            left_motor.setPosition(left_wheel_revolutions)
            right_motor.setPosition(right_wheel_revolutions)
            
            if mode_params.TESTING:
                print('right')
        case moves.left:
            left_wheel_revolutions -= revolutions
            right_wheel_revolutions += revolutions
            left_motor.setPosition(left_wheel_revolutions)
            right_motor.setPosition(right_wheel_revolutions)
            
            if mode_params.TESTING:
                print('left')
        case moves.back:
            revolutions *= 2
            left_wheel_revolutions += revolutions
            right_wheel_revolutions -= revolutions
            left_motor.setPosition(left_wheel_revolutions)
            right_motor.setPosition(right_wheel_revolutions)
            
            if mode_params.TESTING:
                print('back')

    wait_move_end(robot, ps_left, ps_right)


''' move_back_DFS
# @brief Moves robot back to previous valid fork (Deep first search).
# 
# @param destination: variable with robot destination cell
# @param maze_map: dictionary with maze map graph
# @param robot_position: variable with current robot position in maze
# @param fork: dictionary with paths to each fork from current position
# @param fork_number: variable with number of last used fork
# @param unused_routes: dictionary with number of unused routes for each fork
# @param robot_orientation: variable with current robot orientation in maze
# @params robot, ps, tof, left_motor, right_motor, ps_left, ps_right: variables with robot devices
# @param path: list with actual path from start to current position
#
# @retv fork, fork_number, fork_count, path, robot_orientation, robot_position: updated values
'''
def move_back_DFS(destination, maze_map, robot_position, fork, fork_number, unused_routes, robot_orientation,\
               robot, ps, tof, left_motor, right_motor, ps_left, ps_right, path):
    
    while destination not in maze_map[robot_position]:
        for cell in reversed(fork[fork_number]):
            
            robot_position, robot_orientation = move_one_position_graph(cell, robot_position, robot_orientation, robot,\
                                                                ps, tof, left_motor, right_motor, ps_left, ps_right) 

            fork[fork_number].pop()
            path.pop()

        unused_routes[fork_number] -= 1
        if unused_routes[fork_number] == 0: #go back to previous fork
                if fork_number != 0:
                    fork_number -= 1

    return fork, fork_number, unused_routes, path, robot_orientation, robot_position


''' wait_move_end
# @brief Stops main loop execution until robot ends move.
#
# @params robot, ps_left, ps_right: variables with robot devices
# 
# @retv None
'''
def wait_move_end(robot, ps_left, ps_right):

    while True:
        distance_left_now = ps_left.getValue()
        distance_right_now = ps_right.getValue()

        robot.step(TIME_STEP)

        distance_left_later = ps_left.getValue()
        distance_right_later = ps_right.getValue()

        if (distance_left_now == distance_left_later) and (distance_right_now == distance_right_later):
            break

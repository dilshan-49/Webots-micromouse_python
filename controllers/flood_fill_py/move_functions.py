#Move related functions
from Constants import *
from math import pi, fabs
from algorythm_functions import change_orientation


''' move
# @brief Execute robot move based on its orientation and move direction.
#
# @param robot_orientation: variable with actual robot orientation in global directions
# @param move_direction: variable direction where to move in global directions
# @param robot: object with robot instance
# @param left_motor: object with left motor instance
# @param right_motor: object with right motor instance
# @param ps_left: object with left position sensor instance
# @param ps_right: object with right position sensor instance
# @param ps: list of distance sensors objects
#
# @retv robot_orientation: variable with updated robot orientation in global directions
'''
def move(robot_orientation, move_direction,\
            robot, left_motor, right_motor, ps_left, ps_right, ps):
    if robot_orientation == move_direction: #move forward
        move_1_tile(robot, left_motor, right_motor, ps_left, ps_right, ps)

    elif (not( (robot_orientation == direction.WEST) and (move_direction == direction.NORTH) ) ) != \
        (not( (robot_orientation // 2) == move_direction) ):   #right, XOR, 'not' to avoid nonzero values
        
        robot_orientation = change_orientation(robot_orientation, keys.right)
        turn(robot, keys.right, left_motor, right_motor, ps_left, ps_right)
        move_1_tile(robot, left_motor, right_motor, ps_left, ps_right, ps)

    elif (not((robot_orientation == direction.NORTH) and (move_direction == direction.WEST))) != \
            (not( (robot_orientation * 2) == move_direction) ): #left, XOR
        
        robot_orientation = change_orientation(robot_orientation, keys.left)
        turn(robot, keys.left, left_motor, right_motor, ps_left, ps_right)
        move_1_tile(robot, left_motor, right_motor, ps_left, ps_right, ps)

    elif ( not( (robot_orientation * 4) == move_direction)) != \
        (not( (robot_orientation // 4) == move_direction) ): #back, XOR

        robot_orientation = change_orientation(robot_orientation, keys.back)
        turn(robot, keys.back, left_motor, right_motor, ps_left, ps_right)
        move_1_tile(robot, left_motor, right_motor, ps_left, ps_right, ps)
    
    return robot_orientation


''' speed_correction #replaced by PID_correction
# @brief Correct robot position according to distance sensors by changing motors speed.
# O
# @param left_wall: value which indicates existance of left wall in this field
# @param right_wall: value which indicates existance of right wall in this field
# @param left_motor: object with left motor instance
# @param right_motor: object with right motor instance
#
# @retv None
'''
def speed_correction(left_wall, right_wall, left_motor, right_motor):
    if fabs(left_wall - right_wall) > 20:

        if left_wall > right_wall:
            right_motor.setVelocity(robot_parameters.SPEED * 0.96)
            left_motor.setVelocity(robot_parameters.SPEED)
        else:
            right_motor.setVelocity(robot_parameters.SPEED)
            left_motor.setVelocity(robot_parameters.SPEED * 0.96)
    elif fabs(left_wall - right_wall) > 10:
        
        if left_wall > right_wall:
            right_motor.setVelocity(robot_parameters.SPEED * 0.98)
            left_motor.setVelocity(robot_parameters.SPEED)
        else:
            right_motor.setVelocity(robot_parameters.SPEED)
            left_motor.setVelocity(robot_parameters.SPEED * 0.98)


''' read_sensors
# @brief Read and process left and right sensors for a pid.
#
# @param robot: object with robot instance
# @param ps: list of distance sensors objects
# @param number_of_reads: variable which indicates how many times to read sensors
#
# @retval avg1_right_angle_sensor: variable with right angle sensor value
# @retval avg6_left_angle_sensorL variable with left angle sensor value
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
# @param left_motor: object with left motor instance
# @param right_motor: object with right motor instance
# @param robot: object with robot instance
# @param ps: list of distance sensors objects
# @param ps_left: object with left position sensor instance
# @param ps_right: object with right position sensor instance
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
        I = 0.0005 #0.0005
        D = 0.0002 # 0.0
        Middle = 75
        
        if left_wall and right_wall:
        
            error = left_angle_sensor - right_angle_sensor
            
            if mode_params.TESTING:
                print('error {}',error)

            error_integral += error
            error_derivative = (previous_error - error)
            previous_error = error
            MotorSpeed = P * error + I * error_integral + D * error_derivative
            if MotorSpeed > 0.2:
                MotorSpeed = 0.2
            elif MotorSpeed < -0.2:
                MotorSpeed = -0.2
            
            if mode_params.TESTING:
                print('speed {}',MotorSpeed)

            left_motor.setVelocity(robot_parameters.SPEED + MotorSpeed)
            right_motor.setVelocity(robot_parameters.SPEED - MotorSpeed)
        elif left_wall:
            error = left_angle_sensor - Middle
            
            if mode_params.TESTING:
                print('errorL {}',error)
                
            error_integral += error
            error_derivative = (previous_error - error)
            previous_error = error
            MotorSpeed = P * error + I * error_integral + D * error_derivative
            if MotorSpeed > 0.06:
                MotorSpeed = 0.06
            elif MotorSpeed < -0.06:
                MotorSpeed = -0.06
            
            if mode_params.TESTING:
                print('speed {}',MotorSpeed)

            left_motor.setVelocity(robot_parameters.SPEED + MotorSpeed)
            right_motor.setVelocity(robot_parameters.SPEED - MotorSpeed)
        elif right_wall:
            error = right_angle_sensor - Middle
            
            if mode_params.TESTING:
                print('errorR {}',error)

            error_integral += error
            error_derivative = (previous_error - error)
            previous_error = error
            MotorSpeed = P * error + I * error_integral + D * error_derivative
            if MotorSpeed > 0.06:
                MotorSpeed = 0.06
            elif MotorSpeed < -0.06:
                MotorSpeed = -0.06
            
            if mode_params.TESTING:
                print('speed {}',MotorSpeed)

            left_motor.setVelocity(robot_parameters.SPEED - MotorSpeed)
            right_motor.setVelocity(robot_parameters.SPEED + MotorSpeed)
    
        distance_left_later = ps_left.getValue()
        distance_right_later = ps_right.getValue()

        if (distance_left_now == distance_left_later) and (distance_right_now == distance_right_later):
            break

    
''' move_1_tile
# @brief Makes robot move forward to next maze cell.
#
# @param robot: object with robot instance
# @param left_motor: object with left motor instance
# @param right_motor: object with right motor instance
# @param ps_left: object with left position sensor instance
# @param ps_right: object with right position sensor instance
# @param ps: list of distance sensors objects
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


''' turn
# @brief Makes robot turn left, right or backward.
#
# @param robot: object with robot instance
# @param move_direction: variable with direction where to move in global directions
# @param left_motor: object with left motor instance
# @param right_motor: object with right motor instance
# @param ps_left: object with left position sensor instance
# @param ps_right: object with right position sensor instance
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
        case keys.right: #right
            left_wheel_revolutions += revolutions
            right_wheel_revolutions -= revolutions
            left_motor.setPosition(left_wheel_revolutions)
            right_motor.setPosition(right_wheel_revolutions)
            
            if mode_params.TESTING:
                print('right')
        case keys.left: #left
            left_wheel_revolutions -= revolutions
            right_wheel_revolutions += revolutions
            left_motor.setPosition(left_wheel_revolutions)
            right_motor.setPosition(right_wheel_revolutions)
            
            if mode_params.TESTING:
                print('left')
        case keys.back: #back
            revolutions *= 2
            left_wheel_revolutions += revolutions
            right_wheel_revolutions -= revolutions
            left_motor.setPosition(left_wheel_revolutions)
            right_motor.setPosition(right_wheel_revolutions)
            
            if mode_params.TESTING:
                print('back')

    wait_move_end(robot, ps_left, ps_right)


''' wait_move_end
# @brief Stops main loop execution until robot ends move.
#
# @param robot: object with robot instance
# @param ps_left: object with left position sensor instance
# @param ps_right: object with right position sensor instance
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

#Move related functions
from Constants import *
from math import pi, fabs
from algorythm_functions import change_orientation


''' move
# @brief Execute robot move based on its orientation and move direction.
#
# @param robot_orientation: variable with actual robot orientation in global directions
# @param move_direction: variable direction where to move in global directions
# @param left_wall: value which indicates existance of left wall in this field
# @param right_wall: value which indicates existance of right wall in this field
# @param robot: object with robot instance
# @param left_motor: object with left motor instance
# @param right_motor: object with right motor instance
# @param ps_left: object with left position sensor instance
# @param ps_right: object with right position sensor instance
#
# @retv robot_orientation: variable with updated robot orientation in global directions
'''
def move(robot_orientation, move_direction, left_wall, right_wall, left_wall_distance, right_wall_distance, robot, left_motor, right_motor, ps_left, ps_right):
    if robot_orientation == move_direction: #move forward
        if left_wall and right_wall:
            speed_correction(left_wall_distance, right_wall_distance, left_motor, right_motor)
        move_1_tile(robot, left_motor, right_motor, ps_left, ps_right)

    elif (not( (robot_orientation == direction.WEST) and (move_direction == direction.NORTH) ) ) != \
        (not( (robot_orientation // 2) == move_direction) ):   #right, XOR, '!' to avoid nonzero values
        
        robot_orientation = change_orientation(robot_orientation, keys.right)
        turn(robot, keys.right, left_motor, right_motor, ps_left, ps_right)
        move_1_tile(robot, left_motor, right_motor, ps_left, ps_right)

    elif (not((robot_orientation == direction.NORTH) and (move_direction == direction.WEST))) != \
            (not( (robot_orientation * 2) == move_direction) ): #left, XOR
        
        robot_orientation = change_orientation(robot_orientation, keys.left)
        turn(robot, keys.left, left_motor, right_motor, ps_left, ps_right)
        move_1_tile(robot, left_motor, right_motor, ps_left, ps_right)

    elif ( not( (robot_orientation * 4) == move_direction)) != \
        (not( (robot_orientation // 4) == move_direction) ): #back, XOR

        robot_orientation = change_orientation(robot_orientation, keys.back)
        turn(robot, keys.back, left_motor, right_motor, ps_left, ps_right)
        move_1_tile(robot, left_motor, right_motor, ps_left, ps_right)
    
    return robot_orientation


''' speed_correction
# @brief Correct robot position according to distance sensors by changing motors speed.
#
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

''' move_1_tile
# @brief Makes robot move forward to next maze cell.
#
# @param robot: object with robot instance
# @param left_motor: object with left motor instance
# @param right_motor: object with right motor instance
# @param ps_left: object with left position sensor instance
# @param ps_right: object with right position sensor instance
#
# @retv None
'''
def move_1_tile(robot, left_motor, right_motor, ps_left, ps_right):
    
    revolutions = maze_parameters.TILE_LENGTH / robot_parameters.WHEEL #rev in radians
    
    left_wheel_revolutions = ps_left.getValue()
    right_wheel_revolutions = ps_right.getValue()

    left_wheel_revolutions += revolutions
    right_wheel_revolutions += revolutions
    
    left_motor.setPosition(left_wheel_revolutions)
    right_motor.setPosition(right_wheel_revolutions)
    
    print('forward')
    wait_move_end(robot, ps_left, ps_right)


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

    left_motor.setVelocity(robot_parameters.SPEED)
    right_motor.setVelocity(robot_parameters.SPEED)

    match move_direction:
        case keys.right: #right
            left_wheel_revolutions += revolutions
            right_wheel_revolutions -= revolutions
            left_motor.setPosition(left_wheel_revolutions)
            right_motor.setPosition(right_wheel_revolutions)
            print('right')
        case keys.left: #left
            left_wheel_revolutions -= revolutions
            right_wheel_revolutions += revolutions
            left_motor.setPosition(left_wheel_revolutions)
            right_motor.setPosition(right_wheel_revolutions)
            print('left')
        case keys.back: #back
            revolutions *= 2
            left_wheel_revolutions += revolutions
            right_wheel_revolutions -= revolutions
            left_motor.setPosition(left_wheel_revolutions)
            right_motor.setPosition(right_wheel_revolutions)
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

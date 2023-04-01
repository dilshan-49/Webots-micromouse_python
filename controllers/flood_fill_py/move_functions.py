#Move related functions
from controller import Motor, PositionSensor
from Constants import *
from math import pi
def move_1_tile(robot, left_motor, right_motor, ps_left, ps_right):
    
    revolutions = maze_parameters.TILE_LENGTH / robot_parameters.WHEEL #rev in radians
    
    left_wheel_revolutions = ps_left.getValue()
    right_wheel_revolutions = ps_right.getValue()

    left_wheel_revolutions += revolutions
    right_wheel_revolutions += revolutions
    
    left_motor.setPosition(left_wheel_revolutions)
    right_motor.setPosition(right_wheel_revolutions)
    
    print('prosto')
    wait_move_end(robot, ps_left, ps_right)

def turn(robot, move_direction, left_motor, right_motor, ps_left, ps_right):

    revolutions = (pi/2) * robot_parameters.AXLE / 2 / robot_parameters.WHEEL # in radians

    left_wheel_revolutions = ps_left.getValue()
    right_wheel_revolutions = ps_right.getValue()

    left_motor.setVelocity(robot_parameters.SPEED)
    right_motor.setVelocity(robot_parameters.SPEED)

    match move_direction:
        case 'D': #right
            left_wheel_revolutions += revolutions
            right_wheel_revolutions -= revolutions
            left_motor.setPosition(left_wheel_revolutions)
            right_motor.setPosition(right_wheel_revolutions)
            print('prawo')
        case 'A': #left
            left_wheel_revolutions -= revolutions
            right_wheel_revolutions += revolutions
            left_motor.setPosition(left_wheel_revolutions)
            right_motor.setPosition(right_wheel_revolutions)
            print('lewo')
        case 'S': #back
            revolutions *= 2
            left_wheel_revolutions += revolutions
            right_wheel_revolutions -= revolutions
            left_motor.setPosition(left_wheel_revolutions)
            right_motor.setPosition(right_wheel_revolutions)
            print('tyl')

    wait_move_end(robot, ps_left, ps_right)





def wait_move_end(robot, ps_left, ps_right):

    while True:
        distance_left = ps_left.getValue()
        distance_right = ps_right.getValue()
        robot.step(TIME_STEP)
        distance_left2 = ps_left.getValue()
        distance_right2 = ps_right.getValue()
        if (distance_left == distance_left2) and (distance_right == distance_right2):
            break

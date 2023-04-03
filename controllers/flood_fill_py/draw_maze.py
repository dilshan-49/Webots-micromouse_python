from turtle import *
from freegames import line

''' draw_maze
# @brief Create final maze with distance values with a use of turtle graphics.
#
# @param maze_map: list with actual maze map with walls
# @param distance: list with actual distances values/path
#
# @retval None
'''
def draw_maze(maze_map, distance):
    setup(1020, 1020, 1040, 360) #size and position on screen
    hideturtle()
    tracer(False)
    color('black')
    width(1)
    size = 60
    #draw grid
    for y in range(-480, 480, size):
        for x in range(-480, 480, size):
            line(x, y + size, x + size, y + size)
            line(x + size, y, x + size, y + size)
            line(x, y, x + size, y)
            line(x, y, x, y + size)

    width(5)
    #draw walls
    i = 0
    for y in range(-480, 480, size):
        for x in range(-480, 480, size):
            draw_wall(maze_map[i] - 64, distance[i], x, y, size)
            i += 1

    update()
    print('DONE')
    done()


''' draw_wall
# @brief Draw corresponding walls and values in each field.
#
# @param maze_map: list with actual maze map with walls
# @param distance: list with actual distances values/path
# @param x: variable with offest in x direction
# @param y: variable with offest in y direction
# @param size: value with one field size (for easier change when changing window size)
#
# @retval None
'''
def draw_wall(maze_map, distance, x, y, size):
    penup()
    goto(x + 8, y + 16)
    write('%i' % distance, font=("Verdana", 13, 'bold'))
    pendown()
    match maze_map:
        case 1:
            line(x, y, x, y + size)
        case 2:
            line(x, y, x + size, y)
        case 3:
            line(x, y, x, y + size)
            line(x, y, x + size, y)
        case 4:
            line(x + size, y, x + size, y + size)
        case 5:
            line(x, y, x, y + size)
            line(x + size, y, x + size, y + size)
        case 6:
            line(x + size, y, x + size, y + size)
            line(x, y, x + size, y)
        case 7:
            line(x + size, y, x + size, y + size)
            line(x, y, x + size, y)
            line(x, y, x, y + size)
        case 8:
            line(x, y + size, x + size, y + size)
        case 9:
            line(x, y, x, y + size)
            line(x, y + size, x + size, y + size)
        case 10:
            line(x, y + size, x + size, y + size)
            line(x, y, x + size, y)
        case 11:
            line(x, y + size, x + size, y + size)
            line(x, y, x + size, y)
            line(x, y, x, y + size)
        case 12:
            line(x, y + size, x + size, y + size)
            line(x + size, y, x + size, y + size)
        case 13:
            line(x, y + size, x + size, y + size)
            line(x + size, y, x + size, y + size)
            line(x, y, x, y + size)
        case 14:
            line(x, y + size, x + size, y + size)
            line(x + size, y, x + size, y + size)
            line(x, y, x + size, y)
        case 15:
            line(x, y + size, x + size, y + size)
            line(x + size, y, x + size, y + size)
            line(x, y, x + size, y)
            line(x, y, x, y + size)
            print('WTF POLE %i' % maze_map )


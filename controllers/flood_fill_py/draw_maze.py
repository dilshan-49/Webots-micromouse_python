from turtle import *
from freegames import line


def draw_maze(maze_map, distance):
    setup(1020, 1020, 1040, 360) #rozmiar i pozycja na ekranie
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


def open_file(file_name):
    maze = open(file_name, 'r')
    if maze == None:
        print('ERROR')
        exit(1)

    maze_map_temp = []
    for field in maze:
        maze_map_temp.append(int(field))
    maze.close()
    return maze_map_temp


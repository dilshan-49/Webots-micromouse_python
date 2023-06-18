from turtle import *
#from freegames import line 
import var


def init_maze(maze_map, distance, size):
    setup(1020, 1020, 1040, 360) #size and position on screen
    maze = Turtle()
    maze.hideturtle()
    tracer(False)
    maze.color('black')
    maze.width(1)
    
    grid = Turtle()
    grid.hideturtle()
    grid.color('black')
    grid.width(1)

    text = Turtle()
    text.hideturtle()
    text.width(1)


    #draw grid
    for y in range(-480, 480, size):
        for x in range(-480, 480, size):
            line(x, y + size, x + size, y + size, grid)
            line(x + size, y, x + size, y + size, grid)
            line(x, y, x + size, y, grid)
            line(x, y, x, y + size, grid)

    maze.width(5)
    #draw walls
    i = 0
    for y in range(-480, 480, size):
        for x in range(-480, 480, size):
            write_distance(x, y, distance[i], text)
            if maze_map[i] < 64:
                draw_wall(maze_map[i], x, y, size, maze)
            draw_wall(maze_map[i] - 64, x, y, size, maze)
            i += 1

    return text, maze


''' draw_maze
# @brief Create final maze with distance values with a use of turtle graphics.
#
# @param maze_map: list with actual maze map with walls
# @param distance: list with actual distances values/path
#
# @retval None
'''
def draw_maze(maze_map, distance, mode):
    
    size = 60

    text, maze = init_maze(maze_map, distance, size)
 
    circles = Turtle()
    circles.pencolor("red")
    circles.hideturtle()
    circles.width(4)

    lines = Turtle()
    lines.pencolor("red")
    lines.hideturtle()
    lines.width(4)
    if mode == 1:
        update_maze_search(size, circles, text, maze)

    update_maze(size, lines, circles)

    done()

def update_maze(size, lines, circles):
    last_x, last_y = draw_path(0, 0, size, lines)
    draw_position(size, circles)

    while var.robot_pos != 136:
        with var.con:
            while not var.pos_update:
                var.con.wait()
            
        var.pos_update = False
        last_x, last_y = draw_path(last_x, last_y, size, lines)
        circles.clear()
        draw_position(size, circles)

def update_maze_search(size, circles, text, maze):
    draw_position(size, circles)

    while var.robot_pos != var.target_global:
        with var.con:
            while not var.pos_update:
                var.con.wait()
            
        var.pos_update = False

        draw_position(size, circles)
        maze.clear()
        i = 0
        for y in range(-480, 480, size):
            for x in range(-480, 480, size):                   
                if var.maze_map_global[i] < 64:
                    draw_wall(var.maze_map_global[i], x, y, size, maze)
                draw_wall(var.maze_map_global[i] - 64, x, y, size, maze)
                i += 1
        i = 0
        if var.distance_update:
            text.clear()
            for y in range(-480, 480, size):
                for x in range(-480, 480, size):
                    write_distance(x, y, var.distance_global[i], text)
                    i += 1
            var.distance_update = False
    
        # print("pozycja robo")
        # print (var.robot_pos)
        # xx = var.robot_pos % 16
        # xx = -480 + x * size 
        # yy = int(var.robot_pos / 16)
        # yy = -480 + y * size
        # if var.maze_map_global[var.robot_pos] < 64:
        #     draw_wall(var.maze_map_global[var.robot_pos], xx, yy, size, maze)
        # else:
        #     draw_wall(var.maze_map_global[var.robot_pos] - 64, xx, yy, size, maze)

        update()
        

def line(a, b, x, y, turtle):
    turtle.up()
    turtle.goto(a, b)
    turtle.down()
    turtle.goto(x, y) 


def draw_path(last_x, last_y, size, t):
    next_x = var.robot_pos % 16
    next_y = int(var.robot_pos / 16)
    t.penup()
    t.goto(-450 + last_x * size, -450 + last_y * size) #last position
    t.pendown()
    line(-450 + last_x * size, -450 + last_y * size, -450 + next_x * size, -450 + next_y * size, t)
    update()

    return next_x, next_y
def draw_position(size, t):
    next_x = var.robot_pos % 16
    next_y = int(var.robot_pos / 16)
    t.penup()
    t.goto(-450 + next_x * size, -450 + next_y * size - 6) #last position
    t.pendown()
    t.fillcolor("red")
    t.begin_fill()
    t.circle(6)
    t.end_fill()
    update()

def write_distance(x, y, distance, t):
    t.penup()
    t.goto(x + 8, y + 16)
    t.write('%i' % distance, font=("Verdana", 13, 'bold'))
    t.pendown()

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
def draw_wall(maze_map, x, y, size, t):

    match maze_map:
        case 1:
            line(x, y, x, y + size, t)
        case 2:
            line(x, y, x + size, y, t)
        case 3:
            line(x, y, x, y + size, t)
            line(x, y, x + size, y, t)
        case 4:
            line(x + size, y, x + size, y + size, t)
        case 5:
            line(x, y, x, y + size, t)
            line(x + size, y, x + size, y + size, t)
        case 6:
            line(x + size, y, x + size, y + size, t)
            line(x, y, x + size, y, t)
        case 7:
            line(x + size, y, x + size, y + size, t)
            line(x, y, x + size, y, t)
            line(x, y, x, y + size, t)
        case 8:
            line(x, y + size, x + size, y + size, t)
        case 9:
            line(x, y, x, y + size, t)
            line(x, y + size, x + size, y + size, t)
        case 10:
            line(x, y + size, x + size, y + size, t)
            line(x, y, x + size, y, t)
        case 11:
            line(x, y + size, x + size, y + size, t)
            line(x, y, x + size, y, t)
            line(x, y, x, y + size, t)
        case 12:
            line(x, y + size, x + size, y + size, t)
            line(x + size, y, x + size, y + size, t)
        case 13:
            line(x, y + size, x + size, y + size, t)
            line(x + size, y, x + size, y + size, t)
            line(x, y, x, y + size, t)
        case 14:
            line(x, y + size, x + size, y + size, t)
            line(x + size, y, x + size, y + size, t)
            line(x, y, x + size, y, t)
        case 15:
            line(x, y + size, x + size, y + size, t)
            line(x + size, y, x + size, y + size, t)
            line(x, y, x + size, y, t)
            line(x, y, x, y + size, t)
            print('WTF POLE %i' % maze_map )


import copy
import map_functions
graph_maze = {
  0 : [4],
  1 : [2, 5],
  2 : [1, 3],
  3 : [2],
  4 : [0,5,8],
  5 : [1,4,6,9],
  6 : [5,7],
  7 : [6,11],
  8 : [4,12],
  9 : [5,13],
  10 : [11],
  11 : [7,10,15],
  12 : [8, 13],
  13 : [9, 12, 14],
  14 : [13],
  15 : [11],
}
graph_init = {
  0 : [1,4],
  1 : [0,2, 5],
  2 : [1, 3,6],
  3 : [2,7],
  4 : [0,5,8],
  5 : [1,4,6,9],
  6 : [2,5,7,10],
  7 : [3,6,11],
  8 : [4,9,12],
  9 : [5,8,10,13],
  10 : [6,9,11,14],
  11 : [7,10,15],
  12 : [8,13],
  13 : [9,12,14],
  14 : [10,13,15],
  15 : [11,14],
}

def init_graph(graph):
    for i in range(0,4):
        graph[i].append(i+4)
        graph[i].append(i+1)
    for i in range(12,16):
        graph[i].append(i-4)
        graph[i].append(i+1)

    # for i in range()

def dfs(maze_map, node):
    intersection_number = -1
    intersection = {}
    visited = []
    stack = []
    path = []
    visited.append(node)
    stack.append(node) 
    while stack:
        robot_position = stack.pop() #obecna pozycja
        current_pos = robot_position
        maze_map[robot_position] = graph_maze[robot_position] #skan scian
        
        path.append(robot_position)
        if robot_position == 12: #czy target
            print(path)
            break
        
        l = len(maze_map[robot_position])
        if l >=3:
            intersection_number += 1
        if intersection_number > -1:
            if l >= 3:
                intersection[intersection_number] = [robot_position]
            elif l == 2:
                intersection[intersection_number].append(robot_position)
            else: #slepy zaulek
                intersection_number += 1 #copy
                while stack[-1] not in maze_map[current_pos]:
                    intersection_number -= 1
                    for n in reversed(intersection[intersection_number]):
                        current_pos = n#move n
                        intersection[intersection_number].pop()
                        path.pop()
                intersection[intersection_number].append(copy.copy(path[-1]))
        print(robot_position, end = " ")

        # reverse iterate through edge list so results match recursive version
        for n in reversed(maze_map[robot_position]): #check possible routes
            if n not in visited:
                visited.append(n)
                stack.append(n)
                if n == 12: # == target
                    break
 
        #move to next pos stack[-1]

def main():
    print(len(graph_init[0]))
    # print(graph_init2[0])
    # graph_init2[0] = graph_maze[0]
    # print(graph_init2[0])
    maze_map = map_functions.init_maze_map_graph()
    print(maze_map)
    dfs(graph_init, 0)

main()
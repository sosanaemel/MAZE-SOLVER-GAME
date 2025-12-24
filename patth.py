from maze import maze
import curses
from curses import wrapper
import queue
import time

# second step in code 
#algorithms BFS to draw maze
def print_maze(maze, stdscr, path=[]):
    BLUE = curses.color_pair(1)
    RED = curses.color_pair(2)
    
    #print the maze in 2D array
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i, j*2, "X", RED)
            else:
                stdscr.addstr(i, j*2, value, BLUE) # i rows , j*2 columns , value in maze , color BLUE text 

# fours step in code  
def find_start(maze, start):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return i, j
    return None

# six step in code  
#not found end point , test all neighbors point in 4 direction but not visited before and in maze
def find_neighbors(maze, row, col):
    neighbors = []
    
    #TEST UP AND DOWN
    if row > 0:  
        neighbors.append((row - 1, col))
    if row + 1 < len(maze): 
        neighbors.append((row + 1, col))
            
    #TEST LEFT AND RIGHT
    if col > 0:  # LEFT
        neighbors.append((row, col - 1))
    if col + 1 < len(maze[0]):  #number of rows 
        neighbors.append((row, col + 1))
    
    return neighbors

# third step in code  
#algorithms BFS to find a sort path in maze
def find_path(maze, stdscr):
    start = "O"
    end = "X"
    start_pos = find_start(maze, start)
    
    # fives step in code  
    q = queue.Queue() #first in first out
    q.put((start_pos, [start_pos])) # start point , position of point and save all path i took
    
    visited = set() # save all point i took
    visited.add(start_pos)
    
    while not q.empty(): #loop is run to end or visit all point and not found end point
        current_pos, path = q.get() # get first point in queue and path to this point
        row, col = current_pos
        
        stdscr.clear()
        print_maze(maze, stdscr, path)
        time.sleep(0.2)
        stdscr.refresh()
        
        if maze[row][col] == end: #found end point
            return path
        
        neighbors = find_neighbors(maze, row, col)
        for neighbor in neighbors:
            if neighbor in visited: # if point visited before skip it
                continue
            
            #obistecal
            r, c = neighbor
            if maze[r][c] == "#": # if point is wall skip it
                continue
            
            new_path = path + [neighbor] # add point to path
            q.put((neighbor, new_path)) # add point to queue with path to this point
            visited.add(neighbor) # add point to visited set

# first step in code  
def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK) # 1 is id , color blue text , color black background
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK) # 2 is id , color red text , color black background
    color_1 = curses.color_pair(1)
    color_2 = curses.color_pair(2)
    
    find_path(maze, stdscr)
    stdscr.getch()
    
    # stdscr.addstr(0, 0, "Hello World", color_1) # 0 first rows, 0 second columns

wrapper(main)

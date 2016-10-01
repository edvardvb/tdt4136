"""
This is a solution to the Rush Hour Puzzle using A*. The algorithm takes in a start state
and performs an A* search using all possible moves from the start state, the possible moves
from these states, and so on.
"""

import math
from GUI import draw_path
from tkinter import *
import time

#Weight of the heuristic
alpha = 1

#fill value for the empty spaces
fill_value = 'x'

#Denotes how often the GUI should refresh to show new moves
#(Currently not used, but once the GUI updates in the same window this will be needed.
GUI_seconds = 1
#Denotes the size of the squares in the GUI
rec_size = 50

class State:
    """
    The state class keeps record of how the vehicles are positioned at the moment. It has a state
    attribute, which is a list of the vehicles, their position, x, y and length. It also
    contains a board which is an overview of what the playing board looks like in this state.
    The rest of the attributes should be pretty self explanitory.
    """

    def __init__(self, cost, state):
        self.state = state
        self.board = self.initialize_board()
        self.children = []
        self.parent = None
        self.g = float('inf')  # cost for this path so far
        self.h = None  # estimated remaining cost for this path
        self.cost = cost  # can be changed for later implementations

    def initialize_board(self):
        #Converts the state into how the board looks
        state = self.state
        #Initialize with fill_value. For now the board is 6 x 6
        board = [[fill_value for x in range(6)] for y in range(6)]
        #put n where the n'th vehicle is
        for vehicle_nr in range(len(state)):
            row = state[vehicle_nr]
            orientation = row[0]
            vehicle_x = row[1]
            vehicle_y = row[2]
            vehicle_length = row[3]
            if orientation == 0: #vehicle is horizontal
                for j in range(vehicle_length): #the length of the vehicle
                    board[vehicle_y][vehicle_x + j] = vehicle_nr
            elif orientation == 1: #vehicle is vertical
                for j in range(vehicle_length): #the length of the vehicle
                    board[vehicle_y + j][vehicle_x] = vehicle_nr
        return board

    def print_state(self):
        print('\n')
        for row in self.state: print(row)

    def f(self):
        return self.g + self.h

    def __str__(self):
        string_board = []

        for row in self.board:
            string_row = [str(x) for x in row]
            string_board.append(string_row)

        s = ''
        for row in string_board:
            for symbol in row: 
                s+=symbol
            s+='\n'

        return s

    def __eq__(self, other):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] != other.board[i][j]:
                    return False

        return True

#Coordinates that we want the vehicle to reach, x first, y second
goal = [4,2]

def heuristic(state):
    #Compare the euclidian distance of the vehicle we want to move and the goal.
    #We do this by comparing the first coordinate of the goal wih the first coordinate
    #of the vehicle, and the same for the second coordinate
    #The vehicle we want to move is in the first row of the state

    #return math.sqrt((goal[0] - state.state[0][1])**2 + (goal[1] - cell.state[0][2])**2)

    #Actually, let's try how many open tiles the move leaves infront of the exit
    row = state.board[goal[1]]
    nr_of_open = 0
    x = -1
    #iterate backwards over the goal row to see how many free spaces there are infront of the exit
    while row[x] == fill_value:
        nr_of_open += 1
        x -= 1

    #Multiply the huristic value with our weight alpha
    return nr_of_open * alpha

def possible_moves(state):
    #returns a list of possible next states
    possible_moves = []
    for vec_nr in range(len(state.state)): #iterate over the number of cars, and check each possible move
        vehicle_moves = possible_vehicle_moves(state, state.state[vec_nr])
        for move in vehicle_moves:
            new_state = State(move[4], create_new_state_from_move(move, vec_nr, state))
            possible_moves.append(new_state)

    return possible_moves

def create_new_state_from_move(move, vehicle_nr, state):
    #make a new state row with number of cars * empty lists
    new_state = [[] for x in range(len(state.state))]
    for i in range(len(state.state)):
        if i != vehicle_nr:
            new_state[i] = [x for x in state.state[i]]

    new_state[vehicle_nr] = move[:4]
    #print("Trying to move vec_nr: " + str(vehicle_nr))
    #print("Move: " + str(move))
    return new_state

def possible_vehicle_moves(state, vehicle):
    possible_moves = []
    vehicle_x = vehicle[1]
    vehicle_y = vehicle[2]
    vehicle_length = vehicle[3]
    board = state.board

    if vehicle[0] == 0: #Vehicle is horizontal
        #For each case we add another element in the list, representing the cost
        #check left
        x = vehicle_x - 1
        while x > -1 and board[vehicle_y][x] == fill_value:
            possible_moves.append([0, x, vehicle_y, vehicle_length, math.fabs(vehicle_x - x)])
            x -= 1
        #check right
        x = vehicle_x + vehicle_length
        while x < len(board[0]) and board[vehicle_y][x] == fill_value:
            possible_moves.append([0, x - vehicle_length + 1, \
                    vehicle_y, vehicle_length, math.fabs(vehicle_x - x - 1)])
            x += 1

    elif vehicle[0] == 1: #Vehicle is vertical
        #check up
        y = vehicle_y - 1
        while y > -1 and board[y][vehicle_x] == fill_value:
            possible_moves.append([1, vehicle_x, y, vehicle_length, math.fabs(vehicle_y - y)])
            y -= 1
        #check down
        y = vehicle_y + vehicle_length
        while y < len(board) and board[y][vehicle_x] == fill_value:
            possible_moves.append([1, vehicle_x, y - vehicle_length + 1, \
                    vehicle_length, math.fabs(vehicle_y - y + 1)])
            y += 1

    return possible_moves

def is_at_goal(state):
    #check if the coorindates of the zero car is at goal position
    return state.state[0][1] == goal[0] and state.state[0][2] == goal[1]

#The different levels
easy = [
        [0,2,2,2],
        [0,0,4,3],
        [0,3,4,2],
        [0,4,1,2],
        [1,2,0,2],
        [1,4,2,2]
        ]
medium = [
        [0,1,2,2],
        [0,0,5,3],
        [0,1,3,2],
        [0,3,0,2],
        [1,0,2,3],
        [1,2,0,2],
        [1,3,1,2],
        [1,3,3,3],
        [1,4,2,2],
        [1,5,0,2],
        [1,5,2,2]
        ]
hard = [
        [0,2,2,2],
        [0,0,4,2],
        [0,0,5,2],
        [0,2,5,2],
        [0,4,0,2],
        [1,0,0,3],
        [1,1,1,3],
        [1,2,0,2],
        [1,3,0,2],
        [1,4,2,2],
        [1,4,4,2],
        [1,5,3,3]
        ]
expert = [
        [0,0,2,2],
        [0,0,1,3],
        [0,0,5,2],
        [0,1,0,2],
        [0,2,3,2],
        [0,3,4,2],
        [1,0,3,2],
        [1,2,4,2],
        [1,3,0,3],
        [1,4,0,2],
        [1,4,2,2],
        [1,5,2,2],
        [1,5,4,2]
        ]
start = State(0, expert)


def a_star(start):
    """
    Perform an A* search from the start state. The children of the start state will be
    all the possible moves we can make from here. Then it checks all the
    children states for possible moves, and so on until it finds the goal state.
    The method returns a boolean stating if the search was successfull, and the final state.
    The commented print statements are really nice to see how the algorithm is working.
    """
    print('\n ***** NEW RUN ***** \n')
    closedSet = []
    openSet = [start]
    start.g = 0
    start.h = heuristic(start)
    iteration = 0

    while openSet:
        iteration += 1
        print('\n ITERATION NR: ' + str(iteration) + '\n')
        openSet.sort(key=lambda x : -x.f())
        current = openSet.pop()
        print("Current: ")
        print(current)
        closedSet.append(current)
        if is_at_goal(current):
            return True, current

        child_states = possible_moves(current)

        for neighbour in child_states:
            if neighbour in closedSet:
                continue

            tentative_gScore = current.g + neighbour.cost

            if neighbour not in openSet:
                openSet.append(neighbour)

            elif tentative_gScore >= neighbour.g:
                continue

            neighbour.parent = current
            neighbour.g = tentative_gScore
            neighbour.h = heuristic(neighbour)

    return False, current

#Solves the puzlle and returns weather it was solvable in the 'solved' boolean
solved, final_state = a_star(start)

#Chain backwards through the parents, starting at the final stage
if solved:
    seq = [final_state]
    pred = final_state.parent
    while pred:
        seq.append(pred)
        pred = pred.parent

    #print('\n ***** NOW PRINTING SOLUTION ***** \n')

    #Print moves in both textual and GUI form
    cost = 0
    for state in reversed(seq): 
        #print(state)
        draw_path(str(state), rec_size, fill_value)
        cost += state.cost

    print("Moves used: " + str(len(seq) - 1))
    print("Total cost: " + str(cost))

else: print("Could not solve")

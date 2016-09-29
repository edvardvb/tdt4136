"""
Produces a simple visualisation of the shortest path from A to B
for boards 2-1 to 2-4, using my own implementation of the a*-algorithm.
"""
from GUI_2 import draw_path
from math import sqrt


class Cell:
    """
    One 'node' or element in the given string/board.
    """
    def __init__(self, x, y, cost, type):
        self.x = x
        self.y = y
        self.children = []
        self.parent = None
        self.g = float('inf')   # cost for this path so far
        self.h = None           # estimated remaining cost for this path
        self.solution = False
        self.cost = cost        # cost of node
        self.type = type        # type of node, used for representation purposes and marking start/goal

    def f(self):
        """
        :return: Estimated total cost for a path going through this node.
        """
        return self.g + self.h

    # The following are simply used for comparison and printing purposes
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return str(self.x) + ' ' + str(self.y) + ' ' + self.type

    def __repr__(self):
        return str(self.x) + ' ' + str(self.y) + ' ' + self.type


def build_children(cell, possible_cells):
    """
    Fills 'cell.children' with all neighbours of 'cell'
    :param cell: Current cell
    :param possible_cells: All cells
    """
    for c in possible_cells:
        if (c.x == cell.x + 1 and c.y == cell.y) or\
                (c.x == cell.x - 1 and c.y == cell.y) or\
                (c.x == cell.x and c.y == cell.y + 1) or\
                (c.x == cell.x and c.y == cell.y - 1):
            cell.children.append(c)


def a_star_loop(open_nodes, closed_nodes, cells):
    """
    Finds a pretty optimal path, but not always the best one :))

    :param open_nodes: Essentially just a list containing the starting cell,
                       but this is populated as the algorithm runs.
    :param closed_nodes: As above, empty when starting.
    :param cells: All cells in the grid, used to populate the above.
    :return: Boolean, true if the goal is found.
    """
    done = False
    while not done:
        if not open_nodes:
            break  # failure
        current = open_nodes.pop(0)
        closed_nodes.append(current)
        if current.type == 'goal':
            return True
        build_children(current, cells)
        for child in current.children:
            if child not in open_nodes and child not in closed_nodes:  # i.e 'Have we already checked this cell?'
                attach_and_evaluate(current, child)
                open_nodes.append(child)
                open_nodes.sort(key=lambda x: x.h)  # sort by lowest estimated cost
            elif current.g + child.cost < child.g:
                attach_and_evaluate(current, child)
                if child in closed_nodes:
                    propagate(child)
    if not done:
        return False


def attach_and_evaluate(p, c):
    c.parent = p
    c.g = p.g + c.cost
    euclidian_distance_to_goal = sqrt((goal.x - c.x)**2 + (goal.y - c.y)**2)
    c.h = euclidian_distance_to_goal*(c.cost/weight)
    # (euclidian distance to goal)*(cell cost/average cost for all nodes)


def propagate(cell):
    """
    Recursively propagate possible improvements in estimated cost and best path.
    :param cell: Current cell
    """
    for child in cell.children:
        if cell.g + child.cost < child.g:
            child.parent = cell
            child.g = cell.g + child.cost
            propagate(child)


"""
This bit simply builds the grid, iterating over the board to create all cells.
Also maintains a dictionary with the amount of each type of cell, used to calculate the average
cost of all cells in the grid. This is used for weighting purposes in the heuristic function.
Sets some starting parameters for the start and goal.
"""
board = input('filename: ')
cells = []
closed_nodes = []
open_nodes = []
start = None
goal = None
counters = {'w': 0, 'm': 0, 'f': 0, 'g': 0, 'r': 0}
f = open(board, 'r')
lines = [line.strip('\n') for line in f]
for i in range(len(lines)):
    for j in range(len(lines[i])):
        if lines[i][j] == 'w':
            c = Cell(j, i, 100, 'w')
            cells.append(c)
            counters['w'] += 1
        elif lines[i][j] == 'm':
            c = Cell(j, i, 50, 'm')
            cells.append(c)
            counters['m'] += 1
        elif lines[i][j] == 'f':
            c = Cell(j, i, 10, 'f')
            cells.append(c)
            counters['f'] += 1
        elif lines[i][j] == 'g':
            c = Cell(j, i, 5, 'g')
            cells.append(c)
            counters['g'] += 1
        elif lines[i][j] == 'r':
            c = Cell(j, i, 1, 'r')
            cells.append(c)
            counters['r'] += 1
        elif lines[i][j] == 'A':
            start = Cell(j, i, 0, 'start')
        elif lines[i][j] == 'B':
            goal = Cell(j, i, 0, 'goal')
            cells.append(goal)
total_cost_of_all_cells = (counters['w']*100 + counters['m']*50 + counters['f']*10 + counters['g']*5 + counters['r'])
weight = total_cost_of_all_cells / sum(counters.values())

goal.solution = True
goal.h = 0
start.h = sqrt((goal.x - start.x)**2 + (goal.y - start.y)**2)
start.g = 0
open_nodes.append(start)


"""
Runs the algorithm, and then traces back from goal to start using Cell.parent to find the path that was chosen.
Prints a board with the path marked, and sends the string to Tkinter for drawing.
Calculates the total cost of the path, for comparison purposes.
"""
if a_star_loop(open_nodes, closed_nodes, cells):
    lines = [line.strip('\n') for line in open(board, 'r')]
    cell = goal
    total = 0
    height = len(lines)
    width = 0
    print('\n')
    while cell.parent != start:
        total += cell.parent.cost
        row = list(lines[cell.parent.y])
        width = len(row)
        row[cell.parent.x] = 'O'
        lines[cell.parent.y] = ''.join(row)
        cell = cell.parent

    lines = '\n'.join(lines)
    print(lines)
    print(total)
    draw_path(lines, width, height)
else:
    print('Failed')

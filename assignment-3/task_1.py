"""
Produces a simple visualisation of the shortest path from A to B
for boards 1-1 to 1-4, using my own implementation of the a*-algorithm.
"""
from GUI import draw_path


class Cell:
    """
    One 'node' or element in the given string/board.
    """
    def __init__(self, x, y, wall):
        self.x = x
        self.y = y
        self.wall = wall        # boolean
        self.children = []
        self.parent = None
        self.g = float('inf')   # g(s), cost for this path so far
        self.h = None           # h(s), estimated remaining cost for this path
        self.solution = False
        self.cost = 1           # can be changed for later implementations

    def f(self):
        """
        :return: Estimated total cost for a path going through this node.
        """
        return self.g + self.h

    # The following are simply used for comparison and printing purposes
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return str(self.x) + ' ' + str(self.y)

    def __repr__(self):
        return str(self.x) + ' ' + str(self.y)


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
            if not c.wall:
                cell.children.append(c)


def a_star_loop(open_nodes, closed_nodes, cells):
    """
    Finds the optimal path

    :param open_nodes: Essentially just a list containing the starting cell, but this is populated as the algorithm runs.
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
        if current.solution:
            return True
        build_children(current, cells)
        for child in current.children:
            if child not in open_nodes and child not in closed_nodes:  # i.e 'Have we already checked this cell?'
                attach_and_evaluate(current, child)
                open_nodes.append(child)
                open_nodes.sort(key=lambda x: x.f())  # sort by lowest estimated cost
            elif current.g + child.cost < child.g:
                attach_and_evaluate(current, child)
                if child in closed_nodes:
                    propagate(child)
    if not done:
        return False


def attach_and_evaluate(parent, child):
    child.parent = parent
    child.g = parent.g + child.cost
    child.h = abs(goal.x - child.x) + abs(goal.y - child.y)  # Manhattan-distance


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
Sets some starting parameters for the start and goal.
"""
board = input('filename: ')  # i.e. 'board-1-1.txt' etc
cells = []
closed_nodes = []
open_nodes = []
start = None
goal = None
f = open(board, 'r')
lines = [line.strip('\n') for line in f]
for i in range(len(lines)):
    for j in range(len(lines[i])):
        if lines[i][j] == '.':
            c = Cell(j, i, False)
            cells.append(c)
        elif lines[i][j] == 'A':
            start = Cell(j, i, False)
        elif lines[i][j] == 'B':
            goal = Cell(j, i, False)
            cells.append(goal)
        elif lines[i][j] == '#':
            c = Cell(j, i, True)
            cells.append(c)

goal.solution = True
goal.h = 0
start.h = abs(goal.x - start.x) + abs(goal.y - start.y)
start.g = 0
open_nodes.append(start)


"""
Runs the algorithm, and then traces back from goal to start using Cell.parent to find the path that was chosen.
Prints a board with the path marked, and sends the string to Tkinter for drawing.
"""
if a_star_loop(open_nodes, closed_nodes, cells):
    lines = [line.strip('\n') for line in open(board, 'r')]
    cell = goal
    height = len(lines)
    width = 0
    print('\n')
    while cell.parent != start:
        row = list(lines[cell.parent.y])
        width = len(row)
        row[cell.parent.x] = 'O'
        lines[cell.parent.y] = ''.join(row)
        cell = cell.parent
    lines = '\n'.join(lines)
    print(lines)
    draw_path(lines, width, height)
else:
    print('Failed')

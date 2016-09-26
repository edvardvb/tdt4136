class Cell():

    parent = None
    children = []
    g = float('inf')
    h = None
    solution = False
    cost = 1

    def f(self):
        return self.g + self.h

    def __init__(self, x, y, wall):
        self.x = x
        self.y = y
        self.wall = wall
        #self.state = int(str(x)+str(y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return str(self.x) + ' ' + str(self.y)

    def __repr__(self):
        return str(self.x) + ' ' + str(self.y)


def build_children(cell, possible_cells):
    for c in possible_cells:
        if (c.x == cell.x + 1 and c.y == cell.y) or\
                (c.x == cell.x - 1 and c.y == cell.y) or\
                (c.x == cell.x and c.y == cell.y + 1) or\
                (c.x == cell.x and c.y == cell.y - 1):
            if not c.wall:
                cell.children.append(c)




def a_star_loop(open_nodes, closed_nodes, cells):
    done = False
    counter = 0
    while not done:
        counter += 1
        if not open_nodes:
            break
        current = open_nodes.pop(0)
        #print(current)
        closed_nodes.append(current)
        if current.solution:
            return True
        build_children(current, cells)
        for child in current.children:
            if child not in open_nodes and child not in closed_nodes:
                attach_and_evaluate(current, child)
                open_nodes.append(child)
                open_nodes.sort(key= lambda x: x.h)

            elif current.g + child.cost < child.g:
                attach_and_evaluate(current, child)
                if child in closed_nodes:
                    propagate(child)
        #print(open_nodes, closed_nodes)
        #print([c.h for c in open_nodes])
    #print(counter)
    if not done:
        return False

def attach_and_evaluate(p, c):
    c.parent = p
    c.g = p.g + c.cost
    c.h = abs(goal.x - c.x) + abs(goal.y - c.y)

def propagate(cell):
    for child in cell.children:
        if cell.g + child.cost < child.g:
            child.parent = cell
            child.g = cell.g + child.cost
            propagate(child)

cells = []
closed_nodes = []
open_nodes = []
start = None
goal = None
f = open('board-1-1.txt', 'r')
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

print(a_star_loop(open_nodes, closed_nodes, cells))


from tkinter import *

def draw_path(s, w, h, open_nodes, closed_nodes):
    master = Tk()
    rec_size = 50
    offset = 10

    w = Canvas(master, width=w*rec_size, height=h*rec_size)

    x = 0
    y = 0
    for symbol in s:
        if symbol == '\n':
            y += 1
            x = 0
        else:
            if symbol == 'A': color = 'red'
            elif symbol == 'B': color = 'green'
            elif symbol == 'O': color = 'blue'
            elif symbol == '#': color = 'black'
            else: color = 'white'

            w.create_rectangle(x*rec_size, y*rec_size, \
                    x*rec_size + rec_size, y*rec_size + rec_size, fill=color)

            x += 1

    for node in closed_nodes: 
        w.create_line(node.x*rec_size + offset, node.y*rec_size + offset, node.x*rec_size \
                + rec_size - offset, node.y*rec_size + rec_size - offset, width="2")

        w.create_line(node.x*rec_size + rec_size - offset , node.y*rec_size + offset, \
                node.x*rec_size + offset, node.y*rec_size + rec_size - offset , width="2")

    for node in open_nodes:
        w.create_oval(node.x*rec_size + offset, node.y*rec_size + offset, \
                node.x*rec_size + rec_size - offset, node.y*rec_size + rec_size - offset, width="2")

    w.pack()
    master.mainloop()

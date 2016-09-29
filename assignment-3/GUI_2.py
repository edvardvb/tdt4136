from tkinter import *

def draw_path(s, w, h):
    master = Tk()
    rec_size = 40

    w = Canvas(master, width=w*rec_size, height=h*rec_size)

    x = 0
    y = 0
    for symbol in s:
        if symbol == '\n':
            y += 1
            x = 0
        else:
            if symbol == 'A': color = 'red'
            elif symbol == 'B': color = 'chartreuse'
            elif symbol == 'O': color = 'cyan'
            elif symbol == 'w': color = 'blue'
            elif symbol == 'm': color = 'grey'
            elif symbol == 'f': color = 'dark green'
            elif symbol == 'g': color = 'light green'
            else: color = 'peru'

            w.create_rectangle(x*rec_size, y*rec_size, \
                    x*rec_size + rec_size, y*rec_size + rec_size, fill=color)

            x += 1

    w.pack()
    master.mainloop()

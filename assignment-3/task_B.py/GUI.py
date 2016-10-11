from tkinter import *

rec_size = 100

def draw_path(state, fill_value):
    master = Tk()
    w = Canvas(master, width=6*rec_size, height=6*rec_size)

    for y, row in enumerate(state.board):
        for x, value in enumerate(row):
            if value == 0: color = 'lawn green'
            elif value == fill_value: color = ''
            elif value == 1: color = 'salmon'
            elif value == 2: color = 'royal blue'
            elif value == 3: color = 'deep pink'
            elif value == 4: color = 'tomato'
            elif value == 5: color = 'pale green'
            elif value == 6: color = 'light sky blue'
            elif value == 7: color = 'gold'
            elif value == 8: color = 'wheat'
            elif value == 9: color = 'dark violet'
            elif value == 10: color = 'light sea green'
            elif value == 11: color = 'chocolate'
            elif value == 12: color = 'medium purple'
            else: color = 'white'

            if color != '':
                w.create_rectangle(x*rec_size, y*rec_size, \
                        x*rec_size + rec_size, y*rec_size + rec_size, fill=color, outline=color)

    w.pack()
    master.mainloop()

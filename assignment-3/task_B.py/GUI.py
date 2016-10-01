from tkinter import *

def draw_path(s, rec_size, fill_value):
    master = Tk()
    w = Canvas(master, width=6*rec_size, height=6*rec_size)

    x = 0
    y = 0
    for symbol in s:
        if symbol == '\n':
            y += 1
            x = 0
        else:
            if symbol == '0': color = 'lawn green'
            elif symbol == fill_value: color = 'white'
            elif symbol == '1': color = 'salmon'
            elif symbol == '2': color = 'royal blue'
            elif symbol == '3': color = 'deep pink'
            elif symbol == '4': color = 'tomato'
            elif symbol == '5': color = 'pale green'
            elif symbol == '6': color = 'light sky blue'
            elif symbol == '7': color = 'gold'
            elif symbol == '8': color = 'wheat'
            elif symbol == '9': color = 'dark violet'
            elif symbol == '10': color = 'snow 2'
            elif symbol == '11': color = 'seashell'
            elif symbol == '12': color = 'medium purple'
            else: color = 'light sky blue'

            w.create_rectangle(x*rec_size, y*rec_size, \
                    x*rec_size + rec_size, y*rec_size + rec_size, fill=color)

            x += 1

    w.pack()
    master.mainloop()

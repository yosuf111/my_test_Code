#!/usr/bin/env python
# coding:utf-8
from matplotlib.pyplot import xlim, xticks, ylim, yticks
import numpy as np
from tkinter import *
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

t_x = []
t_y = []
t = 0


def drawpic():
    global t_x, t_y, t
    t += 0.1
    t_x.append(t)
    t_y.append(np.sin(t))
    plt.clf()
    if t < 10:
        xlim(0, 11)
    else:
        xlim(t-10, t+1)
    ylim(-1.5, 1.5)
    plt.plot(t_x, t_y)

    drawpic_canvas.draw()
    root.after(10, drawpic)


if __name__ == '__main__':
    matplotlib.use('TkAgg')
    root = Tk()
    root.geometry('1200x800')
    drawpic_f = plt.figure(figsize=(10, 5))
    drawpic_canvas = FigureCanvasTkAgg(drawpic_f, master=root)
    root.resizable(FALSE, FALSE)

    drawpic_canvas.draw()
    drawpic_canvas.get_tk_widget().pack(side=TOP)

    Button(root, text='开始', width=10, height=3, command=drawpic).pack()
    Button(root, text='退出', width=10, height=3, command=root.quit).pack()
    root.protocol('WM_DELETE_WINDOW', root.quit)
    root.mainloop()

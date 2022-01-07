from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
counter = False

window = Tk()
img = PhotoImage(file='D:\\文档\\停止.gif')
img1 = PhotoImage(file='D:\\文档\\运行.gif')
label_img = Label(image= img)
label_img.pack()
entry1 = Entry(window)
entry1.pack()
def getText1():
    global counter
    try:
        float(entry1.get())
        l1.config(text=entry1.get())
        counter = not counter
        print(counter)
        if counter:
            label_img.configure(image=img1)
        else:
            label_img.configure(image=img)
            
    except:
        messagebox.showwarning('警告','请输入数字')

button2 = Button(window, text='test', command=getText1)
button2.pack()

l1 = Label(window, text='只能数字')
l1.pack()
window.mainloop()
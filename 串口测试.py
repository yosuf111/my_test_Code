from matplotlib.pyplot import text
import serial
from tkinter import *
from tkinter import messagebox
counter = False
Load_V_query = [0XA1,0XA2,0X00,0X11,0X00,0X00,0X00,0X54,0X73,0X74] 
#输出负载转换成数值
def load_mechine_in(lmi):
    lmi = int(lmi, 16)
    lmi = lmi/1000
    lmi = round(lmi, 3)
    return lmi
window = Tk()
img = PhotoImage(file='D:\\文档\\停止.gif')
img1 = PhotoImage(file='D:\\文档\\运行.gif')
def test1():
    global ser_load
    try:
        portx_load = 'COM5' #负载串口号
        bps_load = 9600
        timex_load = None
        ser_load = serial.Serial(portx_load, bps_load, timeout = timex_load)
        label_img.configure(image=img1)
        messagebox.showinfo('warning', '负载设备连接成功')
    except:
        if ser_load.is_open:
            messagebox.showinfo('warning','设备已经连接')
        else:
            label_img.configure(image=img)
            messagebox.showerror('warning', '负载设备连接失败')
            
button1 = Button(window,text='click', command=test1).pack()
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
            #label_img.configure(image=img1)
            print('hello')
        else:
            label_img.configure(image=img)
            
    except:
        messagebox.showwarning('警告','请输入数字')

button2 = Button(window, text='test', command=getText1)
button2.pack()
def test2():
    global ser_load
    ser_load.flushInput()  #清空缓冲区
    ser_load.write(Load_V_query)
    load_V_out = ser_load.read(10).hex()[8:14]
    load_V = load_mechine_in(load_V_out)
    print(load_V)
button2 = Button(window, text='ceshi', command=test2).pack()
l1 = Label(window, text='只能数字')
l1.pack()

window.mainloop()
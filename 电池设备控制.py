# encoding = utf-8
from tkinter import Message, messagebox
from tkinter.constants import BOTH, TOP
from typing import Text
import matplotlib.pyplot as plt
import serial
import struct
from tkinter import Button, Canvas, Tk
import pandas as pd
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from tkinter.messagebox import askyesno

save_counter = True
counter = False
load_vdata_list = []
load_idata_list = []
charge_vdata_list = []
charge_idata_list = []

Load_V_query = [0XA1,0XA2,0X00,0X11,0X00,0X00,0X00,0X54,0X73,0X74]  #负载器电压查询方法
Load_I_query = [0XA1,0XA2,0X00,0X12,0X00,0X00,0X00,0X55,0X73,0X74]  #负载器电流查询方法
Charge_V_query = [0X01,0X03,0X0B,0XBC,0X00,0X02,0X07,0XCB]          #充电器电压查询方法
Charge_I_query = [0X01,0X03,0X0B,0XBE,0X00,0X02,0XA6,0X0B]          #充电器电流查询方法


#充电器计算方法
def charge_mechine_in(cmi):
    s = ''
    s = s+cmi
    cm_out = struct.unpack('!f', bytes.fromhex(s))[0]
    cm_out = round(cm_out, 3)
    return cm_out

#输出负载转换成数值
def load_mechine_in(lmi):
    lmi = int(lmi, 16)
    lmi = lmi/1000
    lmi = round(lmi, 3)
    return lmi

def Vout_Serial():

    global load_vdata_list
    global load_idata_list
    global charge_vdata_list
    global charge_idata_list
    
    try:
        
        ############################################################负载器连接#####################################################
        portx_load = 'COM5' #负载串口号
        bps_load = 9600
        timex_load = None
        ser_load = serial.Serial(portx_load, bps_load, timeout = timex_load)
        ######################负载器电压绘图###################################################
        
        ser_load.flushInput()  #清空缓冲区
        ser_load.write(Load_V_query)
        load_V_out = ser_load.read(10).hex()[8:14]
        load_V = load_mechine_in(load_V_out)
        load_vdata_list.append(load_V)
        print(load_vdata_list)
        
        ######################负载器电流绘图####################################################
        ser_load.flushInput()  #清空缓冲区
        ser_load.write(Load_I_query)
        load_I_out = ser_load.read(10).hex()[8:14]
        load_I = load_mechine_in(load_I_out)
        load_idata_list.append(load_I)
        print(load_idata_list)


        ############################################################充电器连接#####################################################
        portx_charge = 'COM4' #负载串口号
        bps_charge = 38400
        timex_charge = None
        ser_charge = serial.Serial(portx_charge, bps_charge, timeout = timex_charge)

        ######################充电器电流绘图####################################################
        ser_charge.flushInput()  #清空缓冲区
        ser_charge.write(Charge_I_query)
        charge_I_out = ser_charge.read(9).hex()[6:14]
        charge_I = charge_mechine_in(charge_I_out)
        charge_idata_list.append(charge_I)
        print(charge_idata_list)

    except Exception as e:
        print('error!', e)

def my_mainloop():
    global counter
    if (counter):
        Vout_Serial()
        a.plot(charge_idata_list, color='red')
        canvas.draw()
        window.after(1000, my_mainloop)

def counter_juge():
    global counter
    if(counter):
        counter=False
    else:
        counter = True
        window.after(1000, my_mainloop)

def to_text():
    global counter
    global save_counter #保存数据计数器 当 save_counter=1 时默认保存最后一次数据并结束
    save_counter = True
    ans = askyesno(title='Warning', message='是否暂停并写入数据')
    if ans:
        counter=False
        global load_vdata_list
        global load_idata_list
        global charge_vdata_list
        global charge_idata_list
        
        data_load_vdata_list = pd.DataFrame(load_vdata_list)  #负载电压结果
        data_load_vdata_list.to_csv('负载电压结果.csv')
        
        data_load_idata_list = pd.DataFrame(load_idata_list)  #负载电流结果
        data_load_idata_list.to_csv('负载电流结果.csv')

        data_charge_idata_list = pd.DataFrame(charge_idata_list) #充电电流结果
        data_charge_idata_list.to_csv('充电电流.csv')
        messagebox.showinfo(title='提示', message='保存成功')
        save_counter=False
        
        
    else:
        return

def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas, toolbar)

def closeWindow():
    global counter
    ans = askyesno(title='Warning', message='Close the window?')
    if ans:
        if not(counter or save_counter): #counter 为 真 值程序未停止
            window.destroy()
        else:
            messagebox.showinfo(title='提示', message='您还未停止并保存数据')
            return
               
    else:
        return

if __name__ == '__main__':
    window = Tk()
    window.title('控制界面')
    window.geometry('300x200')
    button_on =Button(window, text='开始',command=lambda: counter_juge())
    button_on.pack()
    button_off = Button(window, text = '数据写入', command=lambda:to_text())
    button_off.pack()
    fig = Figure(figsize=(5, 4), dpi=100)
    a = fig.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack()
    canvas.mpl_connect("key_press_event", on_key_press)
    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()
    canvas.get_tk_widget().pack()
    window.protocol('WM_DELETE_WINDOW', closeWindow)
    window.mainloop()






    
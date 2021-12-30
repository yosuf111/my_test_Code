# encoding = utf-8
import matplotlib.pyplot as plt
import multiprocessing
import pyqtgraph as pg
import serial
import struct
from tkinter import Button, Tk
import pandas as pd

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
        portx_load = 'COM2' #负载串口号
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
        portx_charge = 'COM5' #负载串口号
        bps_charge = 57600
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
    Vout_Serial()
    window.after(1000, my_mainloop)

def stop():
    global load_vdata_list
    global load_idata_list
    global charge_vdata_list
    global charge_idata_list
    window.quit()
    data_load_vdata_list = pd.DataFrame(load_vdata_list)  #负载电压结果
    data_load_vdata_list.to_csv('负载电压结果.csv')
    
    data_load_idata_list = pd.DataFrame(load_idata_list)  #负载电流结果
    data_load_idata_list.to_csv('负载电流结果.csv')

    data_charge_idata_list = pd.DataFrame(charge_idata_list) #充电电流结果
    data_charge_idata_list.to_csv('充电电流.csv')

    print('结束')

if __name__ == '__main__':
    window = Tk()
    window.title('控制界面')
    window.geometry('300x200')
    button_on =Button(window, text='开始',command=lambda: my_mainloop())
    button_on.grid(row=0, column=1)
    button_off = Button(window, text = '结束', command=lambda:stop())
    button_off.grid(row=0, column=2)

    window.mainloop()

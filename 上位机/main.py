"""
-*- coding: UTF-8 -*-
date: 2022.01.11
readme:这是一个上位机程序，可以控制电池实验设备
"""
from tkinter import *
from tkinter import messagebox
from binascii import *
import crcmod
import serial
import struct

counter_charge = False
counter_discharge = False
counter_charge_running = False
counter_discharge_running = False
ser_charge = 0
ser_discharge = 0
Load_V_query = [0XA1, 0XA2, 0X00, 0X11, 0X00, 0X00, 0X00, 0X54, 0X73, 0X74]  # 负载器电压查询方法
Load_I_query = [0XA1, 0XA2, 0X00, 0X12, 0X00, 0X00, 0X00, 0X55, 0X73, 0X74]  # 负载器电流查询方法
Charge_V_query = [0X01, 0X03, 0X0B, 0XBC, 0X00, 0X02, 0X07, 0XCB]  # 充电器电压查询方法
Charge_I_query = [0X01, 0X03, 0X0B, 0XBE, 0X00, 0X02, 0XA6, 0X0B]  # 充电器电流查询方法
Charge_running = [0X01, 0X06, 0X0B, 0XC2, 0X00, 0X01, 0XEB, 0XD2]  # 充电器开始运行
Charge_stop = [0X01, 0X06, 0X0B, 0XC2, 0X00, 0X00, 0X2A, 0X12]  # 充电器停止运行
disCharge_running = [0XA1, 0XA2, 0X00, 0X01, 0X00, 0X00, 0X01, 0X45, 0X73, 0X74]  # 放电器开始运行
disCharge_stop = [0XA1, 0XA2, 0X00, 0X01, 0X00, 0X00, 0X00, 0X44, 0X73, 0X74]  # 放电器停止运行

root = Tk()
img_stop = PhotoImage(file='停止.gif')
img_run = PhotoImage(file='运行.gif')

root.title('电池设备控制上位机')
root.geometry('800x600')
root.resizable(False, False)

# 充电电流图像显示
frame1 = Frame(root, width=300, height=300, bg='blue')
frame1.grid(column=1, row=1)
# 充电器控制框架
frame_charge = Frame(root)
frame_charge.grid(column=2, row=1)
# 充电器串口连接按钮
label_in_img = Label(frame_charge, image=img_stop)
label_in_img.grid(column=1, row=1)


def charge_serial():
    global counter_charge
    global ser_charge
    if not counter_charge:
        # noinspection PyBroadException
        try:
            portx_charge = 'COM4'  # 负载串口号
            bps_charge = 57600
            timex_charge = None
            ser_charge = serial.Serial(portx_charge, bps_charge, timeout=timex_charge)
            if ser_charge.isOpen():
                label_in_img.configure(image=img_run)
                counter_charge = not counter_charge
        except Exception as e:
            messagebox.showinfo('警告', '串口连接失败')
            print('错误明细', e)
    else:
        messagebox.showinfo('警告', '串口已连接')


Button(frame_charge, text='充电器设备连接', command=charge_serial).grid(column=2, row=1)


# 浮点型转为16进制
def float_to_hex(f):
    f = float(f)
    x = hex(struct.unpack('<I', struct.pack('<f', f))[0])
    x1 = x[2:4]
    x2 = x[4:6]
    x3 = x[6:8]
    x4 = x[8:10]
    return x1, x2, x3, x4


# 生成校验码
def crc16Add(read):
    crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
    data = read.replace(' ', '')
    read_crc_out = hex(crc16(unhexlify(data))).upper()
    str_list = list(read_crc_out)
    if len(str_list) == 5:
        str_list.insert(2, '0')
    crc_data = ''.join(str_list)
    crc16_1 = crc_data[4:]
    crc16_2 = crc_data[2:4]
    return crc16_1, crc16_2


def gen_modbus_code(x, switch):
    x1, x2, x3, x4 = float_to_hex(x)
    if switch == 1:
        y = '01 10 0B BA 00 02 04'
    else:
        y = '01 10 0B B8 00 02 04'
    y = y + ' ' + x1 + ' ' + x2 + ' ' + x3 + ' ' + x4
    z1, z2 = crc16Add(y)
    y = y + ' ' + z1 + ' ' + z2
    y = y.split(' ')
    list1 = []
    for _ in range(len(y)):
        by = '0X' + y[_]
        by = int(by, 16)
        list1.append(by)
    return list1


# 充电器设置Frame
def get_ipt_charge_entry():
    global ipt_charge
    global ser_charge
    global clear_i_charge_entry
    # noinspection PyBroadException
    try:
        _ = float(ipt_char_entry.get())
        if _ <= 0 or _ >= 5:
            messagebox.showinfo('警告', '电流输入错误')
            clear_i_charge_entry.set('')
        elif counter_charge:
            ipt_charge.set(str(round(_, 2)))
            clear_i_charge_entry.set('')
            i_charge_num = gen_modbus_code(str(round(_, 2)), 1)  # 设置电流为1 电压为2
            ser_charge.flush()
            ser_charge.write(i_charge_num)
        else:
            messagebox.showinfo('警告', '放电设备未连接')
    except Exception as e:
        messagebox.showinfo('警告', '请输入数字')
        clear_i_charge_entry.set('')
        print('错误明细', e)


# 设置充电电流
ipt_charge = StringVar()  # 输入电流显示
ipt_charge.set('电流')
clear_i_charge_entry = StringVar()
Label(frame_charge, text='充电电流(A)：').grid(column=1, row=2)
Label(frame_charge, textvariable=ipt_charge, width=8, height=1).grid(column=2, row=2)
ipt_char_entry = Entry(frame_charge, textvariable=clear_i_charge_entry, width=5)
ipt_char_entry.grid(column=3, row=2)
Button(frame_charge, text='设置充电电流', command=get_ipt_charge_entry).grid(column=4, row=2)


def get_dpt_charge_entry():
    global vpt_charge
    global ser_charge
    global clear_v_charge_entry
    # noinspection PyBroadException
    try:
        _ = float(vpt_char_entry.get())
        if _ <= 0 or _ >= 32:
            messagebox.showinfo('警告', '电流输入错误')
            clear_v_charge_entry.set('')
        elif counter_charge:
            vpt_charge.set(str(round(_, 2)))
            clear_v_charge_entry.set('')
            v_charge_num = gen_modbus_code(str(round(_, 2)), 2)  # 设置电流为1 电压为2
            ser_charge.flush()
            ser_charge.write(v_charge_num)
        else:
            messagebox.showinfo('警告', '放电设备未连接')
    except Exception as e:
        messagebox.showinfo('警告', '请输入数字')
        clear_v_charge_entry.set('')
        print('错误明细', e)


# 设置充电电压
vpt_charge = StringVar()  # 输入电压显示
vpt_charge.set('电压')
clear_v_charge_entry = StringVar()
Label(frame_charge, text='充电电压(V)：').grid(column=1, row=3)
Label(frame_charge, textvariable=vpt_charge, width=8, height=1).grid(column=2, row=3)
vpt_char_entry = Entry(frame_charge, textvariable=clear_v_charge_entry, width=5)
vpt_char_entry.grid(column=3, row=3)
Button(frame_charge, text='设置充电电压', command=get_dpt_charge_entry).grid(column=4, row=3)


# 充电开始和停止按钮
def charge_run():
    global ser_charge
    global Charge_running
    global Charge_stop
    global counter_charge_running
    if not counter_charge_running:
        if ser_charge:
            label_charge_running.configure(image=img_run)
            counter_charge_running = not counter_charge_running
            messagebox.showinfo('警告', '开始充电')
            ser_charge.flushInput()
            ser_charge.write(Charge_running)
        else:
            messagebox.showinfo('警告', '充电器串口未连接')
    else:
        _ = messagebox.askyesno('警告', '充电暂停')
        if _:
            counter_charge_running = not counter_charge_running
            label_charge_running.configure(image=img_stop)
            ser_charge.flushInput()
            ser_charge.write(Charge_stop)


Button(frame_charge, text='运行\\暂停', command=charge_run).grid(column=2, row=4)
label_charge_running = Label(frame_charge, image=img_stop)
label_charge_running.grid(column=1, row=4)

# 放电设备控制
frame_discharge = Frame(root)
frame_discharge.grid(column=2, row=2)
# 放电器串口连接按钮
label_dis_img = Label(frame_discharge, image=img_stop)
label_dis_img.grid(column=1, row=1)


def discharge_serial():
    global counter_discharge
    global ser_discharge
    if not counter_discharge:
        # noinspection PyBroadException
        try:
            portx_charge = 'COM3'  # 负载串口号
            bps_charge = 9600
            timex_charge = None
            ser_discharge = serial.Serial(portx_charge, bps_charge, timeout=timex_charge)
            if ser_discharge.isOpen():
                label_dis_img.configure(image=img_run)
                counter_discharge = not counter_discharge
                ser_discharge.flush()
        except Exception as e:
            messagebox.showinfo('警告', '串口连接失败')
            print('错误明细', e)
    else:
        messagebox.showinfo('警告', '串口已连接')


# 设置电流输入转换算法，设置停止电压算法
def trans_discharge(x, switch):
    x = x * 100
    x = hex(int(x))[2:]
    x = x.rjust(4, '0')
    if switch == 1:
        discharge_switch = [0XA1, 0XA2, 0X00, 0X02, 0X00, 0X0, 0Xc8, 0X0D, 0X73, 0X74]  # 电流设置
    else:
        discharge_switch = [0XA1, 0XA2, 0X00, 0X03, 0X00, 0X0, 0Xc8, 0X0D, 0X73, 0X74]  # 停止电压
    x = x.upper()
    a = x[0:2]
    a = int(a, 16)
    b = x[2:4]
    b = int(b, 16)
    discharge_switch[5] = a
    discharge_switch[6] = b
    t = 0
    for _ in range(7):
        t += discharge_switch[_]
    t = bin(t)
    t = t[-8:]
    t = int(t, 2)
    discharge_switch[7] = t
    x = discharge_switch
    return x


# 放电器设置Frame
def get_ipt_discharge_entry():
    global ipt_discharge
    global ser_discharge
    global counter_discharge
    global clear_i_discharge_entry
    # noinspection PyBroadException
    try:
        _ = float(ipt_discharge_entry.get())
        if _ <= 0 or _ >= 10:
            messagebox.showinfo('警告', '电流输入错误')
            clear_i_discharge_entry.set('')
        elif counter_discharge:
            ipt_discharge.set(str(round(_, 2)))
            clear_i_discharge_entry.set('')
            _ = round(_, 2)
            _ = trans_discharge(_, 1)  # 设置电流为 1 终止电压为 2
            ser_discharge.flush()
            ser_discharge.write(_)
        else:
            messagebox.showinfo('警告', '放电设备未连接')

    except Exception as e:
        messagebox.showinfo('警告', '请输入数字')
        clear_i_discharge_entry.set('')
        print('错误明细', e)


# 设置放电电流
ipt_discharge = StringVar()
clear_i_discharge_entry = StringVar()
ipt_discharge.set('电流')
Button(frame_discharge, text='放电器设备连接', command=discharge_serial).grid(column=2, row=1)
Label(frame_discharge, text='放电电流(A)：').grid(column=1, row=2)
Label(frame_discharge, textvariable=ipt_discharge, width=8, height=1).grid(column=2, row=2)
ipt_discharge_entry = Entry(frame_discharge, textvariable=clear_i_discharge_entry, width=5)
ipt_discharge_entry.grid(column=3, row=2)
Button(frame_discharge, text='设置放电电流', command=get_ipt_discharge_entry).grid(column=4, row=2)


# 设置放电截至电压
def get_v_discharge_end_entry():
    global v_discharge_end
    global ser_discharge
    global counter_discharge
    global clear_v_discharge_end
    # noinspection PyBroadException
    try:
        _ = float(v_discharge_end_entry.get())
        if _ <= 0 or _ >= 10:
            messagebox.showinfo('警告', '电流输入错误')
            clear_v_discharge_end.set('')
        elif counter_discharge:
            v_discharge_end.set(str(round(_, 2)))
            clear_v_discharge_end.set('')
            _ = round(_, 2)
            _ = trans_discharge(_, 2)  # 设置电流为 1 终止电压为 2
            ser_discharge.write(_)
        else:
            messagebox.showinfo('警告', '放电设备未连接')

    except Exception as e:
        messagebox.showinfo('警告', '电流输入错误')
        clear_v_discharge_end.set('')
        print('错误明细', e)


v_discharge_end = StringVar()
v_discharge_end.set('截止电压')
clear_v_discharge_end = StringVar()
Label(frame_discharge, text='放电截止电压(V)：').grid(column=1, row=3)
Label(frame_discharge, textvariable=v_discharge_end, width=8, height=1).grid(column=2, row=3)
v_discharge_end_entry = Entry(frame_discharge, textvariable=clear_v_discharge_end, width=5)
v_discharge_end_entry.grid(column=3, row=3)
Button(frame_discharge, text='设置截止电压', command=get_v_discharge_end_entry).grid(column=4, row=3)


# 充电开始和停止按钮
def discharge_run():
    global ser_discharge
    global disCharge_running
    global disCharge_stop
    global counter_discharge_running
    if not counter_discharge_running:
        if ser_discharge:
            label_discharge_running.configure(image=img_run)
            counter_discharge_running = not counter_discharge_running
            messagebox.showinfo('警告', '开始放电')
            ser_discharge.flushInput()
            ser_discharge.write(disCharge_running)
        else:
            messagebox.showinfo('警告', '放电器串口未连接')
    else:
        _ = messagebox.askyesno('警告', '放电暂停')
        if _:
            counter_discharge_running = not counter_discharge_running
            label_discharge_running.configure(image=img_stop)
            ser_discharge.flushInput()
            ser_discharge.write(disCharge_stop)


Button(frame_discharge, text='运行\\暂停', command=discharge_run).grid(column=2, row=4)
label_discharge_running = Label(frame_discharge, image=img_stop)
label_discharge_running.grid(column=1, row=4)


# 关闭窗口事件
def on_closing():
    global counter_charge_running
    global counter_discharge_running
    _ = messagebox.askyesno('警告', '您是否要离开？')
    if _:
        if not counter_charge_running and not counter_discharge_running:
            root.destroy()
        else:
            if not counter_charge_running:
                messagebox.showinfo('警告', '您未关闭放电器')
            else:
                messagebox.showinfo('警告', '您未关闭充电器')


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

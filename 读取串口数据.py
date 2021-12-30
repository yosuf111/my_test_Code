# encoding = utf-8
import struct
import serial
import time

#充电器计算方法
def V_OUT(V_out):
    s = ''
    s = s+V_out
    vout = struct.unpack('!f', bytes.fromhex(s))[0]
    vout = round(vout, 3)
    print(vout)

input_data = [0X01,0X03,0X0B,0XBE,0X00,0X02,0XA6,0X0B]
input_V = [0XA1,0XA2,0X00,0X11,0X00,0X00,0X00,0X54,0X73,0X74]

try:
    portx = 'COM5'
    bps = 57600
    timex = None

    ser = serial.Serial(portx, bps, timeout = timex)
    while True:
        ser.write(input_data)


        V_out = ser.read(9).hex()[6:14]
        V_OUT(V_out)
        time.sleep(1)

    ser.close()

except Exception as e:
    print('error!', e)
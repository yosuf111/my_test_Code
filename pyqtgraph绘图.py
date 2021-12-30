# encoding = utf-8
import pyqtgraph as pg
import serial
import struct

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
    print(cm_out)
    return cm_out

#输出负载转换成数值
def load_mechine_in(lmi):
    lmi = int(lmi, 16)
    lmi = lmi/1000
    return lmi

def Vout_Serial():

    global load_vdata_list
    global load_idata_list
    global charge_vdata_list
    global charge_idata_list
    
    try:
        '''
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
        plot.setData(load_vdata_list, pen='r')
        
        ######################负载器电流绘图####################################################
        ser_load.flushInput()  #清空缓冲区
        ser_load.write(Load_I_query)
        load_I_out = ser_load.read(10).hex()[8:14]
        load_I = load_mechine_in(load_I_out)
        load_idata_list.append(load_I)
        print(load_idata_list)
        plot.setData(load_idata_list, pen='g')
        '''
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
        plot.setData(charge_idata_list, pen='g')


    except Exception as e:
        print('error!', e)

if __name__ == '__main__':
    data_list = []
    app = pg.mkQApp() #建立app
    win = pg.GraphicsWindow() #建立窗口
    win.setWindowTitle(u'负载电压波形图')
    win.resize(800, 600)
    historyLength = 100 #横坐标长度
    p = win.addPlot(colspan=2) #把图P加入到窗口中
    p.showGrid(x=True, y=True)
    p.setRange(xRange=[0, historyLength], yRange=[0, 5], padding=0)#设置x轴和y轴坐标
    p.setLabel(axis='left', text='电压') #y轴名字
    p.setLabel(axis='bottom', text='时间') #x轴名字
    p.setTitle('负载电压监测')
    plot = p.plot()
    timer = pg.QtCore.QTimer()
    timer.timeout.connect(Vout_Serial)
    timer.start(1000)
    app.exec_()
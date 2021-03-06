%功能：一阶RC滤波器仿真

%说明：

%1、分析了一阶RC滤波器的幅值衰减特性和相移特性

%2、分析了一阶RC滤波器的频域特性

%3、使用lsim对系统进行仿真

%4、使用FFT对原始输入信号和滤波器输出信号进行分析

%传递函数：sys=1/(1+sRC)

%==========================================================================

close all;

clear all;

f=1:1:5000;%频率序列

w=2*pi*f;

R=1;%电阻值

C=0.47e-6;%电容值


for m=1:length(f)
Re=R/(1+(R*2*pi*w(m)*C)^2);%电容阻抗
Im=-w(m)*R^2*C/(1+(R*2*pi*w(m)*C)^2);

end
plot(Re,Im);


title('电容阻抗');

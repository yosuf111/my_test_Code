import itertools as its

words = 'abcdefghijklmnopqrstuvwxyz1234567890'
r = its.product(words, repeat=4)  # repeat要生成多少位的字典
with open("pwd.txt", "a")as f:
	for i in r:
		f.write("".join(i))
		f.write("".join("\r"))

import zipfile
#import rarfile
import threading
# 判断线程是否需要终止
flag = True
 
def extract(password, file):
    try:
        password = str(password)
        file.extractall(pwd=password.encode('utf-8'))#zip解压缩
        #file.extractall(pwd=password)#rar解压缩
        print("压缩包的密码是：{}".format(password))
        global flag
        flag = False
    except Exception:
        pass		#密码错误则跳过 
def main():
    file = zipfile.ZipFile("test2.zip")#压缩文件
    #file = rarfile.RarFile("pwd.rar")
    passwords = open('pwd.txt')				#密码字典
    for line in passwords.readlines():#逐行读取密码
        if flag is True:
        		password = line.strip('\n')		#去掉回车
        		print(line,end="")						#逐个查看当前密码
        		t = threading.Thread(target=extract, args=(password, file))
        		t.start()	#开始
        		t.join()	#Parent父线程会等待child子线程运行完再继续运行
if __name__ == '__main__':	
    main()
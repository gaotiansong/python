# -*- coding: utf-8 -*-
import time
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import QThread,pyqtSignal,QTimer,QEventLoop
from PyQt6.QtWidgets import QApplication,QFileDialog
from PyQt6.QtGui import QTextCursor
import sys,os
from set import cread_ini,read_ini
from one_caiji import *

class Ui_Form(object):
    def __init__(self):
        super().__init__()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(480, 352)
        self.n=0
        self.lineEdit_driver = QtWidgets.QLineEdit(Form)
        self.lineEdit_driver.setGeometry(QtCore.QRect(50, 20, 371, 30))
        self.lineEdit_driver.setObjectName("lineEdit_driver")

        self.toolButton_driver = QtWidgets.QToolButton(Form)
        self.toolButton_driver.setGeometry(QtCore.QRect(420, 20, 26, 30))
        self.toolButton_driver.setObjectName("toolButton_driver")
        self.toolButton_driver.clicked.connect(self.setBrowerPath)

        self.toolButton_asin = QtWidgets.QToolButton(Form)
        self.toolButton_asin.setGeometry(QtCore.QRect(420, 90, 26, 30))
        self.toolButton_asin.setObjectName("toolButton_asin")
        self.toolButton_asin.clicked.connect(self.setBrowerPath)

        self.lineEdit_asin = QtWidgets.QLineEdit(Form)
        self.lineEdit_asin.setGeometry(QtCore.QRect(50, 90, 371, 30))
        self.lineEdit_asin.setObjectName("lineEdit_asin")

        self.toolButton_procsv = QtWidgets.QToolButton(Form)
        self.toolButton_procsv.setGeometry(QtCore.QRect(420, 150, 26, 30))
        self.toolButton_procsv.setObjectName("toolButton_procsv")
        self.toolButton_procsv.clicked.connect(self.setBrowerPath)

        self.lineEdit_procsv = QtWidgets.QLineEdit(Form)
        self.lineEdit_procsv.setGeometry(QtCore.QRect(50, 150, 371, 30))
        self.lineEdit_procsv.setObjectName("lineEdit_procsv")
        self.pushButton_save = QtWidgets.QPushButton(Form)
        self.pushButton_save.setGeometry(QtCore.QRect(90, 200, 113, 50))
        self.pushButton_save.setObjectName("pushButton_save")
        self.pushButton_save.clicked.connect(self.setBrowerPath)

        self.pushButton_clear = QtWidgets.QPushButton(Form)
        self.pushButton_clear.setGeometry(QtCore.QRect(250, 200, 113, 50))
        self.pushButton_clear.setObjectName("pushButton_clear")
        self.pushButton_clear.clicked.connect(self.setBrowerPath)

        self.pushButton_start = QtWidgets.QPushButton(Form)
        self.pushButton_start.setGeometry(QtCore.QRect(50, 250, 400, 50))
        self.pushButton_start.setObjectName("pushButton_start")
        self.pushButton_start.clicked.connect(self.setBrowerPath)

        self.label1=QtWidgets.QLabel(Form)
        self.label1.setGeometry(QtCore.QRect(50, 300, 371, 50))
        self.label1.setText("采集中......")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        #读取配置文件信息，如果不存在则创建配置文件后读取
        data=[
            "配置driver位置",
            "配置要采集的asin列表",
            "配置保存位置",
        ]
        self.ini_path=r"./seting.ini"
        print("配置文件地址:",self.ini_path)
        if os.path.exists(self.ini_path):
            #如果存在,读取文件
            data=read_ini(self.ini_path)
        else:
            #不存在,创建后再读取
            cread_ini(self.ini_path,data)
            data=read_ini(self.ini_path)
        _translate = QtCore.QCoreApplication.translate
        #配置各组件信息
        Form.setWindowTitle(_translate("Form", "采集亚马逊2021"))
        self.lineEdit_driver.setText(_translate("Form", data[0]))
        self.toolButton_driver.setText(_translate("Form", "..."))
        self.toolButton_asin.setText(_translate("Form", "..."))
        self.lineEdit_asin.setText(_translate("Form", data[1]))
        self.toolButton_procsv.setText(_translate("Form", "..."))
        self.lineEdit_procsv.setText(_translate("Form", data[2]))
        self.pushButton_save.setText(_translate("Form", "保存配置"))
        self.pushButton_clear.setText(_translate("Form", "重新填写"))
        self.pushButton_start.setText(_translate("Form", "开始采集"))

    def setBrowerPath(self):
        sender=MainWindow.sender()#获取是哪个控件给他发消息
        if r"toolButton_driver" == sender.objectName():
            download_path = QFileDialog.getOpenFileName(None, "选取文件", os.getcwd(), "All Files(*);;Text Files(*.txt)")
            self.lineEdit_driver.setText(download_path[0])
        if r"toolButton_asin" == sender.objectName():
            download_path = QFileDialog.getOpenFileName(None, "选取文件", os.getcwd(), "All Files(*);;Text Files(*.txt)")
            self.lineEdit_asin.setText(download_path[0])
        if r"toolButton_procsv" == sender.objectName():
            download_path = QFileDialog.getExistingDirectory(None, "选择存储文件",os.getcwd())
            self.lineEdit_procsv.setText(download_path+self.lineEdit_driver.text())
        if r"pushButton_save" == sender.objectName():
            data=[]
            data.append(self.lineEdit_driver.text())
            data.append(self.lineEdit_asin.text())
            data.append(self.lineEdit_procsv.text())
            #print("data:",data)
            cread_ini(self.ini_path,data)
            #保存配置文件
        if r"pushButton_clear" == sender.objectName():
            data=[
                "重新配置driver位置",
                "重新配置要采集的asin列表",
                "重新配置保存位置",
            ]
            self.lineEdit_driver.setText(data[0])
            self.lineEdit_asin.setText(data[1])
            self.lineEdit_procsv.setText(data[2])
            cread_ini(self.ini_path,data)
        if r"pushButton_start" == sender.objectName():
            print("开始执行采集任务")
            #执行子线程
            self.Star_myThread()
            self.pushButton_start.setEnabled(False)
            self.pushButton_start.setText("采集中···")
    
    def Star_myThread(self):
        print("执行子线程")
        self.th = MyThread() #创建线程
        self.th.signalForText.connect(self.change_label)#链接一个改变数字的函数
        self.th.start()
    
    def change_label(self,msg):
        nowtime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        self.label1.setText(str(nowtime)+"  正在采集:"+msg)
        print("msg:",msg)
        if msg=="End":
            self.th.terminate()
            del self.th
            print("恢复按钮")
            self.pushButton_start.setEnabled(True)

class MyThread(QThread):
    signalForText = pyqtSignal(str) #定义一个参数是str的信号 
    def __init__(self):
        super(MyThread, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        # 工作代码
        head_csv=["types","asin","title","price","weight","desc","var_colour","var_style","count","var_size","Pattern","material","size","pk_size","Fabric Type","imges","Parent"]
        if os.path.exists(find_path()[2])==False:
            wt_head_csv(head_csv)
        
        mo=re.compile("dp/[0-9A-Z]{10}")
        all_asin=[]

        with open(find_path()[1],"r") as f1:
            datas=f1.readlines()
            for i in datas:
                if r"#" in i:
                    print("跳过{}".format(i))
                    continue
                asins=mo.findall(i)
                if len(asins)>0:
                    for asin in asins:
                        #print(asin[3:])
                        all_asin.append(asin[3:])
        print(all_asin)
        asins=list(set(all_asin))
        all_asin=[]
        for asin in asins:
            if asin in []:
                continue
            #开始采集一个产品
            self.signalForText.emit(str(asin))
            time.sleep(1)
            try:
                if asin in all_asin:
                    print("{asin}已采集过，跳过".format(asin=asin))
                    self.signalForText.emit(str(asin)+"采集过，跳过")
                    continue
                find_pro_n(asin,all_asin)
                print("采集完所有变体:",asin)
            except Exception as e:
                print("采集",asin,"失败",e)
        self.signalForText.emit("End") #发送结束信号

if __name__ == '__main__':
    app = QApplication(sys.argv)#创建app
    MainWindow = QtWidgets.QMainWindow() #创建主界面
    ui = Ui_Form()#实例化
    ui.setupUi(MainWindow)#和主界面绑定
    MainWindow.show() #显示
    sys.exit(app.exec())

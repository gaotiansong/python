# -*- coding: utf-8 -*-
# 增加动态开关加载图片功能
# 增加动态切换前后台功能
# 2021年09月24日
import time
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import QThread, pyqtClassInfo,pyqtSignal,QTimer,QEventLoop
from PyQt6.QtWidgets import QApplication,QFileDialog
from PyQt6.QtGui import QTextCursor
import sys,os
from set import cread_ini,read_ini
from one_caiji import *
import re

class Ui_Form(object):
    def __init__(self):
        super().__init__()
        self.th = MyThread() #创建线程
    
    def change_back(self):
        sender_back=MainWindow.sender()#获取是哪个控件给他发消息

        if "后台" in sender_back.text():
            print("后台切换前台")
            self.QRButton_1.setText("前台")
            self.th.ok=False
        else:
            print("前台切换后台")
            self.QRButton_1.setText("后台")
            self.th.ok=True
    def change_pic(self):
        sender_pic=MainWindow.sender()#获取是哪个控件给他发消息
        if "有图" in sender_pic.text():
            self.QRButton_2.setText("无图")
            self.th.pic=True
        else:
            self.QRButton_2.setText("有图")
            self.th.pic=False

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(480, 500)
        self.n=0
        self.lineEdit_driver = QtWidgets.QLineEdit(Form)
        self.lineEdit_driver.setGeometry(QtCore.QRect(50, 20, 371, 30))
        self.lineEdit_driver.setObjectName("lineEdit_driver")

        self.QRButton_1=QtWidgets.QToolButton(Form)
        self.QRButton_1.setGeometry(QtCore.QRect(50, 50, 150, 30))
        self.QRButton_1.setObjectName("QRButton_1")
        self.QRButton_1.setText("后台")
        self.QRButton_1.clicked.connect(self.change_back)

        self.QRButton_2=QtWidgets.QToolButton(Form)
        self.QRButton_2.setGeometry(QtCore.QRect(210, 50, 150, 30))
        self.QRButton_2.setObjectName("QRButton_2")
        self.QRButton_2.setText("有图")
        self.QRButton_2.clicked.connect(self.change_pic)


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

        self.lineEdit1=QtWidgets.QLineEdit(Form)
        self.lineEdit1.setGeometry(QtCore.QRect(50, 320, 400, 30))
        self.lineEdit1.setText("母体信息")


        self.lineEdit2=QtWidgets.QLineEdit(Form)
        self.lineEdit2.setGeometry(QtCore.QRect(50, 370, 400, 30))
        self.lineEdit2.setText("变体信息")

        self.lineEdit3=QtWidgets.QLineEdit(Form)
        self.lineEdit3.setGeometry(QtCore.QRect(50, 420, 400, 30))
        self.lineEdit3.setText("内部信息")

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
            old_download_path=self.lineEdit_driver.text()
            download_path = QFileDialog.getOpenFileName(None, "选取文件", os.getcwd(), "All Files(*);;Text Files(*.txt)")
            if download_path[0]=='':
                self.lineEdit_driver.setText(old_download_path)
            else:
                self.lineEdit_driver.setText(download_path[0])
        if r"toolButton_asin" == sender.objectName():
            old_download_path=self.lineEdit_asin.text()
            download_path = QFileDialog.getOpenFileName(None, "选取文件", os.getcwd(), "All Files(*);;Text Files(*.txt)")
            if download_path[0]=='':
                self.lineEdit_asin.setText(old_download_path)
            else:
                self.lineEdit_asin.setText(download_path[0])
        if r"toolButton_procsv" == sender.objectName():
            old_download_path=self.lineEdit_procsv.text()
            download_path = QFileDialog.getExistingDirectory(None, "选择存储文件",os.getcwd())
            if download_path=='':
                self.lineEdit_procsv.setText(old_download_path)
            else:
                self.lineEdit_procsv.setText(download_path+download_path[0]+"new.csv")
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
            self.lineEdit_driver.setEnabled(False)
            self.lineEdit_asin.setEnabled(False)
            self.lineEdit_procsv.setEnabled(False)
            self.pushButton_start.setText("采集中···")
    
    def Star_myThread(self):
        print("执行子线程")
        
        self.th.signalForText.connect(self.change_label)#链接一个改变数字的函数
        self.th.signalForText2.connect(self.change_label2)#链接一个改变数字的函数
        self.th.signalForText3.connect(self.change_label3)
        self.th.start()
    
    def change_label(self,msg):
        if msg=="End":
            #self.th.terminate()
            del self.th
            print("恢复按钮")
            self.pushButton_start.setEnabled(True)
            self.lineEdit_driver.setEnabled(True)
            self.lineEdit_asin.setEnabled(True)
            self.lineEdit_procsv.setEnabled(True)
            self.lineEdit1.setText("采集完毕")
            self.pushButton_start.setText("开始采集")
        else:
            nowtime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            self.lineEdit1.setText(str(nowtime)+"  正在采集母体:"+msg)
    
    def change_label2(self,msg2):
        nowtime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        self.lineEdit2.setText(str(nowtime)+"  正在采集变体:"+msg2)

    def change_label3(self,msg3):
        self.lineEdit3.setText(msg3)


class MyThread(QThread):
    signalForText = pyqtSignal(str) #定义一个参数是str的信号
    signalForText2 = pyqtSignal(str)
    signalForText3=pyqtSignal(str)
    ok=False
    pic=True
    def __init__(self):
        super(MyThread, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        #工作代码
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
                self.find_pro_n(asin,all_asin)
                print("采集完所有变体:",asin)
            except Exception as e:
                print("采集",asin,"失败",e)
        self.signalForText.emit("End") #发送结束信号

    def find_pro_n(self,home_asin,all_asin):
        import csv
        url="https://www.amazon.com/dp/"+home_asin
        html1,html2=self.find_html(url,page="")
        try:
            asins=find_asins(html1,html2)
        except Exception as e:
            print("没获取到变体,认为该商品木有变体",e)
            asins=[]
        
        if asins==[]:
            asins.append(home_asin)
        n=0
        datas=[]
        b=0
        for asin in asins:
            print("所有变体：",asins)
            print("采集变体",asin)
            n=n+1
            self.signalForText2.emit(str(asin)+"--"+str(len(asins))+"->"+str(n))
            if b>15 and len(asins)>3:
                break
            if asin=="":
                continue
            url="https://www.amazon.com/dp/"+asin
            a=0
            nature=[] #属性列表 当采集到的属性很多 而个别属性拿不到时 判断该产品就是木有这个属性
            while len(nature)<2:
                a=a+1
                b=b+1
                if a>10:
                    break
                print("请求:",a,"次",url)
                self.signalForText3.emit("请求"+str(a)+"次 "+url+"")
                html1,html2=self.find_html(url,page="")
                #通过价格形式判断是否在url后面增加 ?th=1&psc=1
                price=find_price(html1,html2)
                if "-" in price:
                    #如果价格中包括"-"，就在URL后面加?th=1&psc=1重写请求
                    url=url+r"?th=1&psc=1"
                    self.signalForText3.emit("请求"+str(a)+"次 "+url+"")
                    html1,html2=self.find_html(url,page="")
                fromship=find_fromShips(html1,html2)
                print("卖家:",fromship)
                stock=find_stock(html1,html2)
                print("库存为：",stock)
                if fromship=="" or "mazon" not in fromship:
                    print("卖家不是 Amazon 跳过")
                    break
                '''判断是否跳过代码结束'''
                print("品牌:",find_brand(html1,html2))
                brand=find_brand(html1,html2)
                if brand=="":
                    continue
                nature.append(brand) #品牌写入
                print("标题:",find_title(html1,html2))
                title=find_title(html1,html2)
                title=re.sub(brand,"",title)
                if title=="":
                    continue
                nature.append(title)#标题写入
                print("价格:",find_price(html1,html2))
                price=find_price(html1,html2)
                if price=="":
                    continue
                nature.append(price) #价格写入

                material=find_material(html1,html2)
                print("材料:",material)
                
                var_color=find_colour(html1,html2)
                print("颜色变量:",var_color)

                var_style=find_style(html1,html2)
                print("样式变量:",var_style)

                var_size=find_var_size(html1,html2)
                print("变量尺寸:",var_size)
                count=find_count(html1,html2)
                print("件数变量:",count)

                size=find_size(html1,html2)
                print("商品尺寸:",size)

                pk_size=find_Package_size(html1,html2)
                if pk_size=="":
                    pk_size=find_LxWxH(html1,html2)
                try:
                    pk_size=to_lwh(pk_size)
                except Exception as e:
                    print(e)
                    pk_size=""

                print("包装尺寸:",pk_size)
                
                Pattern=find_pattern(html1,html2)
                print("图案:",Pattern)
                Fabric_Type=find_Fabric_Type(html1,html2)
                print("织物类型:",Fabric_Type)

                
                weight=find_weight(html1,html2)
                print("重量:",weight)
                
                desc=find_des(html1,html2)
                desc="\n".join(desc)
                print("描述:",desc)

                nature.append(desc) #描述写入
                print("图片:",find_imges(html1,html2))
                imges=find_imges(html1,html2)
                if imges=="":
                    continue
                nature.append(imges)#图片写入
                parent=""
                types="simple"
                data=[types,asin,title,price,weight,desc,var_color,var_style,count,var_size,Pattern,material,size,pk_size,Fabric_Type,",".join(imges),parent]
                datas.append(data)
                all_asin.append(asin)
                break
        n=0
        index_asin=""
        if len(datas)==0:
            pass
        for data in datas:
            with open(find_path()[2],"a",newline="",encoding="utf-8-sig") as f:
                wt=csv.writer(f)
                if len(datas)==1:
                    data[0]="simple"
                elif len(datas)>1 and n==0:
                    data[0]="variable"
                    index_asin=data[1]
                else:
                    data[0]="variation"
                    data[16]=index_asin
                wt.writerow(data)
                self.signalForText3.emit("成功采集:"+data[1])
                print("成功写入:",data[1])
            n=n+1

    def find_driver(self,ok,pic):
        options = webdriver.ChromeOptions()
        if pic:
            print("无图模式")
            prefs = {"profile.managed_default_content_settings.images": 2}  #设置无图模式
            options.add_experimental_option("prefs", prefs)
        options.add_argument("--lang=en")
        if ok:
            print("无头模式")
            options.add_argument("--headless")
        options.add_experimental_option("excludeSwitches",["enable-logging"])
        options.add_argument('ignore-certificate-errors')

        driver=webdriver.Chrome(options=options,executable_path=find_path()[0])
        return driver

    #获取html
    def find_html(self,url,page):
        print("请求{url}".format(url=url))
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By
        driver=self.find_driver(self.ok,self.pic)
        driver.get(url)
        #调出输入框
        try:
            button1=driver.find_element_by_xpath("//*[@id='glow-ingress-block']")
        except Exception as e:
            print("查找邮编输入:",e)
            print("开始关闭浏览器")
            driver.close()
            driver.quit()
            print("成功关闭浏览器")
            return find_html(url,page)

        button1.click()
        #输入邮编
        wait = WebDriverWait(driver, 10, 0.5)
        element = wait.until(EC.presence_of_element_located((By.ID, "GLUXZipUpdateInput")))#等待
        element.send_keys("10041")
        #点击发送
        button2=driver.find_element_by_xpath("//*[@id='GLUXZipUpdate']/span/input")
        WebDriverWait(driver,10,0.2).until(lambda driver:button2.is_displayed())#显式等待
        button2.click()
        time.sleep(0.5)
        print("一次刷新")
        driver.refresh()
        try:
            driver.implicitly_wait(30)
            driver.set_script_timeout(30)
            driver.set_page_load_timeout(30)
        except Exception as e:
            print("超时:",e)
            print("开始关闭浏览器")
            driver.close()
            driver.quit()
            print("成功关闭浏览器")
            return find_html(url,page)

        a=0
        while a<1:
            try:
                print("下拉",a)
                a=a+1
                
                driver.execute_script("window.scrollTo(document.body.scrollHeight, document.body.scrollHeight*1/5); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
                time.sleep(0.01)
                driver.execute_script("window.scrollTo(document.body.scrollHeight, document.body.scrollHeight*2/5); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
                time.sleep(0.01)
                driver.execute_script("window.scrollTo(document.body.scrollHeight, document.body.scrollHeight*3/5); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
                time.sleep(0.01)
                driver.execute_script("window.scrollTo(document.body.scrollHeight, document.body.scrollHeight*4/5); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
                time.sleep(0.01)
                driver.execute_script("window.scrollTo(document.body.scrollHeight, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
                
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
                time.sleep(0.01)
                
                
                #上拉到顶部
                print("上拉")
                driver.execute_script("window.scrollTo(document.body.scrollHeight, document.body.scrollHeight*4/5); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
                time.sleep(0.01)
                
            except Exception as e:
                print("拉动:",e)
                print("开始关闭浏览器")
                driver.close()
                driver.quit()
                print("成功关闭浏览器")
                return find_html(url,page)
            ''''''
            if page=="ok":
                print("采集列表")
                #wait = WebDriverWait(driver, 10, 0.5)
                #element = wait.until(EC.presence_of_element_located((By.ID, "search")))
                #element.send_keys("selenium")
            ''''''
        #print("二次刷新")
        #driver.refresh()
        try:
            driver.implicitly_wait(5)
            driver.set_script_timeout(5)
            driver.set_page_load_timeout(5)
        except Exception as e:
            print("超时:",e)
            print("开始关闭浏览器")
            driver.close()
            driver.quit()
            print("成功关闭浏览器")
            return find_html(url,page)
        try:
            html=driver.page_source
        except Exception as e:
            print("获取html:",e)
            print("开始关闭浏览器")
            driver.close()
            driver.quit()
            print("成功关闭浏览器")
            return find_html(url,page)

        print("html=",len(html))
        print("开始关闭浏览器")
        driver.close()
        driver.quit()
        print("成功关闭浏览器")
        html2=etree.HTML(html)
        return html,html2


if __name__ == '__main__':
    app = QApplication(sys.argv)#创建app
    MainWindow = QtWidgets.QMainWindow() #创建主界面
    ui = Ui_Form()#实例化
    ui.setupUi(MainWindow)#和主界面绑定
    MainWindow.show() #显示
    sys.exit(app.exec())

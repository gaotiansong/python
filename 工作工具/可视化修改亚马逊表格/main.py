# file: absolute.py
# !/usr/bin/python
import sys

import requests
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QLabel, QApplication, QTextEdit, QPushButton, QLineEdit, QFileDialog,QInputDialog,QComboBox

import ReadExec
import ConMysql

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.open_th = None
        self.th_get_im = None
        self.button_next = QPushButton("下一条", self)
        self.path_edit = QLineEdit(self)
        self.ok_path_button = QPushButton("确定", self)
        self.opt_path_button = QPushButton("选择文件", self)
        self.button_up = QPushButton("上一条", self)
        self.cwd = None
        self.n = 1
        self.all_page = 0
        self.rd = ReadExec.ReadExec()
        self.photo = QPixmap()
        self.name = ""
        self.new_name = ""
        self.url = ""
        # 显示图片
        self.img1 = QLabel("", self)
        self.img2 = QLabel("", self)
        self.img3 = QLabel("", self)
        # 标题
        self.lb_name = QTextEdit(self)
        self.lb_name.setPlaceholderText("标题")
        self.lb_name.move(60, 270)
        self.lb_name.setFixedSize(500, 100)  # 大小
        # 显示标题长度
        self.size_name_t = QLabel("标题长:", self)
        self.size_name_t.move(561, 270)
        self.size_name = QLabel("0", self)
        self.size_name.move(620, 270)
        self.size_name.setFixedSize(40, 20)
        self.size_name.setText(str(len(self.lb_name.toPlainText())))
        # 显示页码
        self.page_t = QLabel("总页码:", self)
        self.page_t.move(563, 320)

        self.page_all = QLabel("0", self)
        self.page_all.move(620, 320)
        self.page_all.setFixedSize(40, 20)

        self.page_t2 = QLabel("当前:", self)
        self.page_t2.move(563, 350)
        self.page_t2.setFixedSize(40, 20)

        self.page_name = QLabel("0", self)
        self.page_name.move(620, 350)
        self.page_name.setFixedSize(40, 20)
        self.page_name.setText(self.page_name.text())

        self.th = MyThread(self)  # 重写的多线程对象
        self.lb_name.textChanged.connect(self.th.run)  # 当内容发生变化时触发此信号，

        self.init_ui()
        self.resize(1000, 700)  # 设置窗口大小
        self.move(100, 0)

    def change_page(self, sigin):
        self.button_next.setEnabled(False)
        self.button_up.setEnabled(False)
        self.img2.setText("图片加载中...")
        print("self.name1=", self.name)
        print("self.name2=", self.new_name)
        print("当标题发生改变时，触发保存函数")
        if self.name != self.new_name:
            print("执行保存")
            self.save_excl()
        print("sigin=", sigin)
        if sigin == "next":
            print("执行get_next")
            self.n = self.n + 1
        if sigin == "up":
            print("执行get_up")
            self.n = self.n - 1
        if sigin == "rest":
            print("执行刷新")
        img_url, name = self.rd.get_image(self.n)
        self.name = name
        self.lb_name.setText(name)  # 设置文本内容
        self.page_name.setText(str(self.n))  # 设置当前页码
        self.th_get_im = GetTh(img_url, self.n, self.all_page)
        self.th_get_im.start()  # 启动线程
        self.th_get_im.signal_photo.connect(self.change_img)  # 接受来自线程的图片数据
        self.th_get_im.signal_next.connect(self.change_next)
        self.th_get_im.signal_up.connect(self.change_up)
        self.th_get_im.exit()

    def change(self, msg):
        self.lb_name.setText(msg)

    def change_img(self, msg):
        print("图片数据:", msg)
        if msg["msg"]=="no":
            self.img2.setText("图片加载失败")
        else:
            self.img2.setPixmap(msg["im"])  # 设置图片

    def change_next(self, msg):
        self.button_next.setEnabled(msg)

    def change_up(self, msg):
        self.button_up.setEnabled(msg)

    def save_excl(self):
        tx = self.lb_name.toPlainText()
        self.size_name.setText(str(len(tx)))
        self.rd.sava_f(self.n, tx)

    def init_ui(self):
        self.setMaximumSize(1000, 1200)
        # 显示图片
        self.img2.move(270, 5)  # 位置
        self.img2.setFixedSize(250, 250)  # 大小
        self.img2.setScaledContents(True)  # 设置图片自适应窗口大小
        # 商品标题
        lb_name1 = QLabel("标题:", self)
        lb_name1.move(20, 285)
        # 保存按钮
        button_save = QPushButton("保存", self)
        button_save.setFixedSize(100, 50)
        button_save.move(650, 270)
        button_save.clicked.connect(self.save_excl)
        # 刷新
        button_res = QPushButton("刷新", self)
        button_res.setFixedSize(100, 50)
        button_res.move(750, 270)
        button_res.clicked.connect(lambda: self.change_page("rest"))
        # 下一条按钮
        self.button_next.setFixedSize(100, 50)
        self.button_next.move(650, 320)
        self.button_next.clicked.connect(lambda: self.change_page("next"))
        # 上一条按钮
        self.button_up.setFixedSize(100, 50)
        self.button_up.move(750, 320)
        self.button_up.clicked.connect(lambda: self.change_page("up"))
        # 文件选择区域
        # 标题
        path_name = QLabel("文件:", self)
        path_name.move(20, 456)
        # 单行文本
        self.path_edit.move(60, 450)
        self.path_edit.setFixedSize(500, 30)

        # 选择文件
        self.opt_path_button.move(570, 450)
        self.opt_path_button.clicked.connect(self.select_f)

        # 确定按钮
        self.ok_path_button.move(660, 450)
        self.ok_path_button.clicked.connect(self.ok_select_f)

        #测试按钮
        self.test_button=QPushButton("测试",self)
        self.test_button.move(720,450)
        #self.test_button.clicked.connect(self.show_child)
        self.le=QLineEdit(self)

        #品牌名
        self.brand_t=QLabel("品牌:",self)
        self.brand_t.move(20,505)
        self.brand_e=QLineEdit(self)
        self.brand_e.move(60,500)
        #核心词
        self.core_word_t=QLabel("核心关键词:",self)
        self.core_word_t.move(220,505)
        #核心关键词库
        self.cord_word_ls = QComboBox(self)
        self.cord_word_ls.move(300,500)
        # 从数据库获取关键词列表
        for i in range(10):
            self.cord_word_ls.addItem(str(i)+"关键词")
        self.cord_word_ls.addItem("添加")
        self.cord_word_ls.textActivated[str].connect(self.addKeyWord)
        #添加核心关键词
        self.add_keyword_buttom=QPushButton("添加",self)
        self.add_keyword_buttom.move(400,500)
        self.add_keyword_buttom.clicked.connect(self.addKeyWord)

        #场景词
        #self.for_word_t=QLabel("适合场景:",self)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('亚马逊商品修改')
        self.show()

    def addKeyWord(self):
        self.child_window = Child()
        self.child_window.show()

    def showDialog(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog',
                                        'Enter your name:')
        if ok:
            self.le.setText(str(text))

    def select_f(self):
        # 获取表格文件地址
        self.ok_path_button.setEnabled(True)
        f_name, _ = QFileDialog.getOpenFileName(self, "选取文件", self.cwd,  # 起始路径
                                                "All Files (*);;Text Files (*.txt)")  # 设置文件扩展名过滤,用双分号间隔
        self.path_edit.setText(f_name)
        print(f_name)

    def ok_select_f(self):
        path = self.path_edit.text()
        self.open_th = OpenExcel(path)

        # 启动线程用来加载文件
        self.open_th.start()  # 创建线程
        self.open_th.SignalExcel_data.connect(self.get_exec_data)  # 链接信号到函数 用函数接受来自线程的信号
        self.open_th.exit()

    def get_exec_data(self, msg):
        # 获取子线程读取的表格数据
        print("getExecData  msg=", msg)
        self.rd = msg
        self.page_all.setText(str(self.rd.max_r))
        self.all_page = self.rd.max_r
        self.page_all.setText(str(self.all_page - 3))
        self.button_up.setEnabled(False)
        self.page_name.setText("1")
        self.n = 1
        self.change_page("rest")

#子窗体
class Child(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("我是子窗口啊")
        self.setMinimumSize(500,500)
        self.type_e_txt=""

        #类别
        self.name_t=QLabel("类  别:",self)
        self.name_t.move(20,30)
        self.name_e=QLineEdit(self)
        self.name_e.setPlaceholderText("例:枕头套")
        self.name_e.move(100,30)
        #类型
        self.type_t=QLabel("类  型:",self)
        self.type_t.move(20,60)
        self.type_e=QComboBox(self)
        type_s=["核心","场景","风格"]
        for i in type_s:
            self.type_e.addItem(i)
        self.type_e.move(100,60)
        self.type_e_txt = self.type_e.currentText()
        self.type_e.textActivated.connect(self.getType)
        #内容
        self.words_t=QLabel("关键词:",self)
        self.words_t.move(20,90)
        self.words_e=QTextEdit(self)
        self.words_e.setPlaceholderText("一行一个关键词")
        self.words_e.move(100,90)
        # 确定
        self.add_b=QPushButton("确定",self)
        self.add_b.move(300,280)
        self.add_b.clicked.connect(self.add_keyword)
    def getType(self):
        self.type_e_txt=str(self.type_e.currentText())
    def add_keyword(self):
        print("类别：",self.name_e.text())
        print("类型：", self.type_e_txt)
        print("内容：",self.words_e.toPlainText())
        cm=ConMysql.ConMysql()
        curses,db=cm.find_cursor()
        print(curses,db)
        #把获取的内容写入数据库
        #刷新主窗口关键词列表
        self.close()


class MyThread(QThread):
    def __init__(self, pa=None):
        super().__init__(pa)
        self.pa = pa

    def run(self):
        md = self.pa.lb_name.toPlainText()  # 获取标签上用户输入的内容。
        self.pa.new_name = md
        self.pa.size_name.setText(str(len(md)))  # 将获取的长度赋值给size_name
        pg = self.pa.page_name.text()  # 获取页码数
        self.pa.page_name.setText(str(pg))  # 把页码数设置到页码上


class GetTh(QThread):
    print("go GetTh")
    signal = pyqtSignal(str)  # 定义信号
    signal_next = pyqtSignal(bool)
    signal_up = pyqtSignal(bool)
    signal_photo = pyqtSignal(dict)

    def __init__(self, img_url, n, all_page):
        super(QThread, self).__init__()
        self.photo = QPixmap()
        self.rd = ReadExec.ReadExec()  # 实例化
        self.img_url = img_url
        self.n = n
        self.all_page = all_page

    # 下载图片，下载完后显示图片
    def run(self):
        print("go image")
        photo = QPixmap()
        # 获取图片链接和图片地址
        # 获取图片内容
        pho_msg = {"im": photo, "msg": ""}
        try:
            photo.loadFromData(requests.get(self.img_url, timeout=3).content)
            pho_msg = {"im": photo, "msg": "ok"}
            self.signal_photo.emit(pho_msg)  # 把图片发送到主框架并显示出来
        except Exception as e:
            print(e)
            pho_msg["msg"] = "no"
            self.signal_photo.emit(pho_msg)
            self.exit()
        # 恢复按钮状态
        print("self.n=", self.n)
        print("self.all_page - 3=", self.all_page - 3)
        if 1 < self.n < self.all_page - 3:
            self.signal_next.emit(True)
            self.signal_up.emit(True)
        if self.n == self.all_page - 3:
            self.signal_next.emit(False)
            self.signal_up.emit(True)
        if self.n == 1:
            self.signal_next.emit(True)
            self.signal_up.emit(False)
        print("ok image\n\n")
        self.exit()

# 用来打开表格
class OpenExcel(QThread):
    SignalExcel_data = pyqtSignal(ReadExec.ReadExec)
    RE = ReadExec.ReadExec()  # 实例化

    def __init__(self, path):
        super(OpenExcel, self).__init__()
        self.path = path

    def __del__(self):
        self.wait()

    def run(self):
        print("使用多线程==", self.path)
        self.RE.open_excl(self.path)  # 执行函数获得一系列数据
        self.SignalExcel_data.emit(self.RE)  # 把实列传入主函数


def main():
    app = QApplication(sys.argv)
    _ = MyApp()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

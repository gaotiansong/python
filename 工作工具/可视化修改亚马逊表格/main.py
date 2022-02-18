# file: absolute.py
# !/usr/bin/python
import sys
from PyQt6.QtWidgets import QWidget, QLabel, QApplication, QTextEdit, QPushButton, QLineEdit, QFileDialog
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QThread, pyqtSignal
import requests
import read_exec

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.cwd = None
        self.n = 0
        self.all_page = 0
        self.rd = read_exec.Read_exec()
        self.photo = QPixmap()
        self.name = ""
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

        self.initUI()
        self.resize(1000, 500)  # 设置窗口大小
        self.move(100, 0)

    def get_next(self):
        # 检查过，不可能出错
        self.th_get_im = GetTh(self)
        self.n = self.n + 1
        self.th_get_im.start()  # 启动线程
        self.th_get_im.signal.connect(self.change)  # 信号链接到函数 函数可以接收到传递过来到信号
        self.th_get_im.signal_next.connect(self.change_next)
        self.th_get_im.signal_up.connect(self.change_up)

        self.page_name.setText(str(self.n))
        self.th_get_im.exit()

    def get_up(self):
        self.n = self.n - 1
        self.th_get_im.start()  # 创建线程实列
        self.th_get_im.signal.connect(self.change)  # 信号链接到函数 函数可以接收到传递过来到信号
        self.th_get_im.signal_next.connect(self.change_next)
        self.th_get_im.signal_up.connect(self.change_up)
        self.page_name.setText(str(self.n))
        self.th_get_im.exit()

    def get_rest(self):
        self.th_get_im.start()
        self.th_get_im.signal.connect(self.change)
        self.th_get_im.signal_next.connect(self.change_next)
        self.th_get_im.signal_up.connect(self.change_up)
        self.page_name.setText(str(self.n))
        self.th_get_im.exit()

    def change(self, msg):
        self.lb_name.setText(msg)

    def change_next(self, msg):
        self.button_next.setEnabled(msg)

    def change_up(self, msg):
        self.button_up.setEnabled(msg)

    def save_excl(self):
        tx = self.lb_name.toPlainText()
        self.size_name.setText(str(len(tx)))
        self.rd.sava_f(self.n, tx)

    def initUI(self):
        self.setMaximumSize(1000, 1000)
        # 显示图片
        # self.img1.move(60, 5)  # 位置
        # self.img1.setFixedSize(200, 200)  # 大小
        # self.img1.setScaledContents(True)  # 设置图片自适应窗口大小

        self.img2.move(270, 5)  # 位置
        self.img2.setFixedSize(250, 250)  # 大小
        self.img2.setScaledContents(True)  # 设置图片自适应窗口大小

        # self.img3.move(480, 5)  # 位置
        # self.img3.setFixedSize(200, 200)  # 大小
        # self.img3.setScaledContents(True)  # 设置图片自适应窗口大小

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
        button_res.clicked.connect(self.get_rest)

        # 下一条按钮
        self.button_next = QPushButton("下一条", self)
        self.button_next.setFixedSize(100, 50)
        self.button_next.move(650, 320)
        # button_next.clicked.connect(self.get_next)
        self.button_next.clicked.connect(self.save_excl)
        self.button_next.clicked.connect(self.get_next)

        # 上一条按钮
        self.button_up = QPushButton("上一条", self)
        self.button_up.setFixedSize(100, 50)
        self.button_up.move(750, 320)
        self.button_up.clicked.connect(self.save_excl)
        self.button_up.clicked.connect(self.get_up)

        # 文件选择区域
        # 标题
        path_name = QLabel("文件:", self)
        path_name.move(20, 456)
        # 单行文本
        self.path_edit = QLineEdit(self)
        self.path_edit.move(60, 450)
        self.path_edit.setFixedSize(500, 30)

        # 确定按钮
        self.ok_path_button = QPushButton("确定", self)
        self.ok_path_button.move(660, 450)
        self.ok_path_button.clicked.connect(self.ok_select_f)

        self.opt_path_button = QPushButton("选择文件", self)
        self.opt_path_button.move(570, 450)
        self.opt_path_button.clicked.connect(self.Select_f)

        # self.test_button = QPushButton("测试",self)
        # self.test_button.move(720,450)
        # self.test_button.clicked.connect(self.get_next)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('亚马逊商品修改')
        self.show()

    def Select_f(self):
        self.ok_path_button.setEnabled(True)
        f_Name, _ = QFileDialog.getOpenFileName(self, "选取文件", self.cwd,  # 起始路径
                                                "All Files (*);;Text Files (*.txt)")  # 设置文件扩展名过滤,用双分号间隔
        self.path_edit.setText(f_Name)
        print(f_Name)

    def ok_select_f1(self):
        # 加载图片
        path_excel = self.path_edit.text()
        self.rd.open_excl(path_excel)
        self.n = 0
        self.all_page = self.rd.max_r
        self.page_all.setText(str(self.all_page - 3))
        self.button_up.setEnabled(False)
        print("self.rd.max_r=", self.rd.max_r)
        self.get_next()

    def ok_select_f(self):
        self.open_th = OpenExcel(self)
        # 启动线程用来加载文件
        self.open_th.start()

class MyThread(QThread):
    def __init__(self, pa=None):
        super().__init__(pa)
        self.pa = pa

    def run(self):
        md = self.pa.lb_name.toPlainText()  # 获取标签上用户输入的内容。
        self.pa.size_name.setText(str(len(md)))  # 将获取的长度赋值给size_name
        pg = self.pa.page_name.text()  # 获取页码数
        self.pa.page_name.setText(str(pg))  # 把页码数设置到页码上

class GetTh(QThread):
    print("go GetTh")
    signal = pyqtSignal(str)  # 定义信号
    signal_next = pyqtSignal(bool)
    signal_up = pyqtSignal(bool)
    signal_photo = pyqtSignal(QPixmap)
    def __init__(self, pa=None):
        super().__init__(pa)
        self.ge = pa
    # 下载图片，下载完后显示图片
    def run(self):
        global reg
        print("go image")
        print("n=", self.ge.n)
        # 设置按钮为不可点击
        self.signal_next.emit(False)  # 发射信号
        self.signal_up.emit(False)
        self.signal_photo.emit(QPixmap())
        self.ge.img2.setPixmap(QPixmap())  # 设置图片
        self.ge.url, self.ge.name = self.ge.rd.get_image(self.ge.n)
        self.signal.emit(self.ge.name)  # 发射信号
        self.ge.photo = QPixmap()
        try:
            reg = requests.get(self.ge.url, timeout=20)
        except Exception as e:
            print(e)
        self.ge.photo.loadFromData(reg.content)
        self.ge.img2.setPixmap(self.ge.photo) #设置图片

        if 1 < self.ge.n < self.ge.all_page - 3:
            self.signal_next.emit(True)  # 发射信号
            self.signal_up.emit(True)
        if self.ge.n == self.ge.all_page - 3:
            self.signal_next.emit(False)
            self.signal_up.emit(True)
        if self.ge.n == 1:
            self.signal_next.emit(True)
            self.signal_up.emit(False)

        print("ok image\n\n")
        self.exit()

class OpenExcel(QThread):
    SignalExcel = pyqtSignal(str)  # 定义信号
    def __init__(self, pa=None):
        super().__init__(pa)
        self.go = pa
    # 加载完文件后 所有按钮可用
    def run(self):
        print("使用多线程加载表格")
        self.go.ok_path_button.setEnabled(False) #改变按钮状态
        path_excel = self.go.path_edit.text() #获取输入多文件地址
        self.go.rd.open_excl(path_excel)
        self.go.n = 0
        self.go.all_page = self.go.rd.max_r #最大页码
        self.go.page_all.setText(str(self.go.all_page - 3)) #设置最大页码
        self.go.button_up.setEnabled(False) #设置按钮状态
        print("self.rd.max_r=", self.go.rd.max_r)
        self.go.get_next()
        self.go.ok_path_button.setEnabled(True)
        self.exit()

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

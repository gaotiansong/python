import sys
import time

from PySide6.QtWidgets import *
from PySide6.QtCore import *
class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("我的软件")
        self.resize(500,300)
        self.n=0

        self.led=QLCDNumber(self)
        self.led.resize(100,50)
        self.led.move(int(self.width()/2-self.led.width()/2),10)
        self.led.display(0)

        self.ok_button=QPushButton("确定",self)
        self.ok_button.resize(100,50)
        self.ok_button.move(int(self.width()/2-self.ok_button.width()/2),self.led.height()+30)
        self.ok_button.clicked.connect(lambda:self.start())

        self.stop_button=QPushButton("暂停",self)
        self.stop_button.resize(100,50)
        self.stop_button.move(self.ok_button.x(),self.ok_button.y()+40)
        self.stop_button.clicked.connect(lambda:self.stop())

    def start(self):
        self.ok_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.th = Myth(self.n)
        self.th.signalA.connect(self.change)
        self.th.start()
    def stop(self):
        self.stop_button.setEnabled(False)
        self.ok_button.setEnabled(True)
        self.th.stop()

    def change(self,msg):
        print("msg=",msg)
        self.n=msg
        self.led.display(self.n)

class Myth(QThread):
    signalA=Signal(int)
    def __init__(self,n):
        super(Myth,self).__init__()
        self.n=n
        self.ok=None
    def __del__(self):
        self.wait()
    def stop(self):
        self.ok=False
    def run(self):
        self.ok = True
        while self.ok:
            self.n=self.n+1
            print(self.n)
            self.signalA.emit(self.n)
            time.sleep(1)

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec())

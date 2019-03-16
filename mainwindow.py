#coding: utf-8

#此文件用于测试windows_base窗口

import sys
from window_base import *

class main_Window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(main_Window, self).__init__() #继承父类
        super().setupUi(self)  #调用父类setUi方法
        super().createUi(self) #调用父类createUi方法


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mywindow = main_Window()
    mywindow.show()  # 显示界面
    sys.exit(app.exec_())
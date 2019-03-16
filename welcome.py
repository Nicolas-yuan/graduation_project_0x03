#coding: utf-8

#欢迎窗体，打开软件后显示本窗体

import sys
from window_base import *


class welcome_Window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(welcome_Window, self).__init__()
        super().setupUi(self)
        #设置垂直布局控件
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setGeometry(QtCore.QRect(50, 20, 921, 681))
        self.verticalLayout.setObjectName("verticalLayoutWidget")
        #标签1
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("华文新魏")
        font.setPointSize(35)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.label.setFont(font)
        self.label.setMouseTracking(False)
        self.label.setStyleSheet("color:rgb(87, 147, 200);")
        self.label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label.setText('Welcome to Y\'s Application') #标签内容
        #标签2
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_2.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_2.setText('\n本软件采用pyQt设计，使用AGNES层次聚类算法，\n进行无监督的流量分类，对未知协议具有很好的识别效果。') #标签内容
        #标签3
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("方正舒体")
        font.setPointSize(15)
        self.label_3.setFont(font)
        self.label_3.setTextFormat(QtCore.Qt.AutoText)
        self.label_3.setScaledContents(False)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.label_3.setText('Maker：Mr.Y     Version：1.0     Time:2019.1.1') #标签内容

        #显示控件
        self.setCentralWidget(self.centralwidget)

        super().createUi(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mywindow = welcome_Window()
    mywindow.show()
    sys.exit(app.exec_())
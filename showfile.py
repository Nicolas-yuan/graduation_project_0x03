#coding: utf-8

#显示文件内容窗体，打开文件后显示本窗体

import sys
from window_base import *
from readfile import *
from showDatastream import *
from cleaningData import *
from PyQt5.QtWidgets import QAbstractItemView, QHeaderView
from PyQt5.QtGui import QFont
from operator import itemgetter

class show_file_Window(QtWidgets.QMainWindow, Ui_MainWindow):
    Packet = ''
    def __init__(self):
        super(show_file_Window, self).__init__()
        super().setupUi(self)

        self.child = show_Datastream_Window()

        # 设置垂直布局
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        # 设置水平布局
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        # 表格控件
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(10, 20, 1001, 421))
        self.tableView.setObjectName("tableView")
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置表格内容不可更改
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)  # 整行选中的方式
            # 下面代码让表格100填满窗口
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            # 设置表格控件的缩放比
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(3)
        self.tableView.setSizePolicy(sizePolicy)
            # 加入布局
        self.verticalLayout.addWidget(self.tableView)

        # 文本控件1
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName("textBrowser")
            # 设置文本控件的缩放比
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        self.textBrowser.setSizePolicy(sizePolicy)
        self.textBrowser.setFont(QFont('SansSerif', 15))
            # 加入布局
        self.horizontalLayout.addWidget(self.textBrowser)

        # 文本控件2
        self.textBrowser2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser2.setObjectName("textBrowser")
            # 设置文本控件的缩放比
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHeightForWidth(self.textBrowser2.sizePolicy().hasHeightForWidth())
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        self.textBrowser2.setSizePolicy(sizePolicy)
        self.textBrowser2.setFont(QFont('SansSerif', 15))
            # 加入布局
        self.horizontalLayout.addWidget(self.textBrowser2)

        # 水平布局加入垂直布局中
        self.verticalLayout.addLayout(self.horizontalLayout)
        # 布局初始化
        self.setCentralWidget(self.centralwidget)

        # 加载事件
        self.action_event()

        super().createUi(self)

    def tableView_set(self):
        # 添加表头：
        self.model = QtGui.QStandardItemModel(self.tableView)
        # 设置表头
        self.model.setHorizontalHeaderLabels(['时间', '源IP', '目的IP', '源端口号', '目的端口号', '协议',
                                              'Data长度',  'SEQ', 'TCP_Flags', '数据'])
        len_Packet = len(self.Packet)
        for j in range(0,len_Packet):
            for i in range(0,10): # range取头不取尾
                self.model.setItem(j, i, QtGui.QStandardItem(self.Packet[j][i]))
                # 设置字符颜色
                self.model.item(j, i).setForeground(QtGui.QBrush(QtGui.QColor(0, 0, 255)))
                # 设置字符位置
                self.model.item(j, i).setTextAlignment(QtCore.Qt.AlignCenter)

        # 显示数据
        self.tableView.setModel(self.model)

    def action_event(self):
        # 二级菜单事件
        self.actionData_Cleaning.triggered.connect(self.Data_reassembling)
        # 设置表格点击事件
        self.tableView.clicked['QModelIndex'].connect(self.textBrowser_set)

    def textBrowser_set(self):
        indexs = self.tableView.currentIndex()
        text = self.model.item(indexs.row(), 9).text()
        self.textBrowser.clear()
        self.textBrowser2.clear()
        self.textBrowser.insertPlainText(text)
        self.textBrowser2.insertPlainText(text.encode(encoding='utf-8', errors='ignore').hex())


    def Data_reassembling(self):
        # 对数据包按照'源IP', '目的IP', '源端口号', '目的端口号', 'SEQ'排序
        self.Packet = sorted(self.Packet, key=itemgetter(1,2,3,4,7))

        # 实例化cleaningData
        data_cleaning = cleaning_function()
        data_cleaning.cleaning_Data(self.Packet)

        # 将清洗后的数据显示
        self.Packet = data_cleaning.Packet_cleaning
        self.tableView_set()

        # 将重组后的数据显示
        self.child.Packet_reassemble = data_cleaning.Packet_reassemble
        self.child.tableView_set()
        self.child.show()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mywindow = show_file_Window()
    mywindow.Packet = read_function().read_file('tcp.pcap')
    mywindow.tableView_set()
    mywindow.show()
    app.exec_()
    sys.exit()
#coding: utf-8

#本程序用于显示数据清理和流重组后的数据

import sys
from window_base import *
from PyQt5.QtWidgets import QAbstractItemView, QHeaderView
from PyQt5.QtGui import QFont

class show_Dataclustering_Window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(show_Dataclustering_Window, self).__init__()
        super().setupUi(self)

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
        #sizePolicy.setHorizontalStretch(4)
        #sizePolicy.setVerticalStretch(3)
        self.tableView.setSizePolicy(sizePolicy)
            # 加入布局
        self.verticalLayout.addWidget(self.tableView)

        # 文本控件1
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName("textBrowser")
            # 设置文本控件的缩放比
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        #sizePolicy.setHorizontalStretch(1)
        #sizePolicy.setVerticalStretch(1)
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
        #sizePolicy.setHorizontalStretch(1)
        #sizePolicy.setVerticalStretch(1)
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
        self.model.setHorizontalHeaderLabels([ '簇标记', '完整性', '源IP', '目的IP', '源端口', '目的端口',  '流长度', '流数据'])

        clustering_num = 0 # 用于记录簇标记
        row = 0            # 用于记录行数
        # color初始化
        color = QtGui.QColor(0, 0, 0)
        num = 0
        # 遍历簇类
        for clusters_data in self.Packet_clustering.items():
            len_cluster = len(clusters_data[1])
            # 遍历同簇流数据
            for i in range(0,len_cluster):   # range取头不取尾
                # 遍历流数据，tableview列数比clusters_data[i]长度多1，
                for j in range(1,8):
                    self.model.setItem(row, 0, QtGui.QStandardItem(str(clustering_num)))
                    # 设置字符颜色
                    self.model.item(row, 0).setForeground(QtGui.QBrush(color))
                    # 设置字符位置
                    self.model.item(row, 0).setTextAlignment(QtCore.Qt.AlignCenter)

                    self.model.setItem(row, j, QtGui.QStandardItem(clusters_data[1][i][j-1]))
                    # 设置字符颜色
                    self.model.item(row, j).setForeground(QtGui.QBrush(color))
                    # 设置字符位置
                    self.model.item(row, j).setTextAlignment(QtCore.Qt.AlignCenter)
                row += 1
            # 不同簇采用不同的颜色区分
            if num == 0:
                # 绿
                color = QtGui.QColor(50, 255, 50)
                num += 1
            elif num == 1:
                # 蓝
                color = QtGui.QColor(50, 50, 255)
                num += 1
            elif num == 2:
                # 红
                color = QtGui.QColor(255, 50, 50)
                num +=1
            else:
                # 黑
                color = QtGui.QColor(0, 0, 0)
                num = 0
            # 簇标记更新
            clustering_num += 1

        # 显示数据
        self.tableView.setModel(self.model)

    def action_event(self):
        # 设置表格点击事件
        self.tableView.clicked['QModelIndex'].connect(self.textBrowser_set)
        pass

    def textBrowser_set(self):
        indexs = self.tableView.currentIndex()
        text = self.model.item(indexs.row(), 7).text()
        self.textBrowser.clear()
        self.textBrowser2.clear()
        self.textBrowser.insertPlainText(text)
        self.textBrowser2.insertPlainText(text.encode(encoding='utf-8', errors='ignore').hex())
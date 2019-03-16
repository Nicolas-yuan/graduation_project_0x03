#coding: utf-8

#所有窗体基础

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap,QIcon
from icon import * # 导入这个文件，会自动调用资源初始化函数

class Ui_MainWindow(object):
    def setupUi(self,MainWindow):
        # 创建主窗口
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.WindowModal)
        # 大小
        MainWindow.resize(1024, 768)

        #设置顶层布局
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        # 设置顶层布局控件的自由缩放
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        #设置菜单
        MainWindow.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        # 设置图标
        icon=QIcon(':/icon.jpg')
        MainWindow.setWindowIcon(icon)
        #菜单栏一级
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 26))
        self.menubar.setObjectName("menubar")
        self.menufile = QtWidgets.QMenu(self.menubar)
        self.menufile.setObjectName("menufile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuCapture = QtWidgets.QMenu(self.menubar)
        self.menuCapture.setObjectName("menuCapture")
        self.menuAnalyse = QtWidgets.QMenu(self.menubar)
        self.menuAnalyse.setObjectName("menuAnalyse")
        MainWindow.setMenuBar(self.menubar)
        #状态栏
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        #菜单栏二级
        self.actionopen = QtWidgets.QAction(MainWindow)
        self.actionopen.setObjectName("actionopen")
        self.actionsave = QtWidgets.QAction(MainWindow)
        self.actionsave.setObjectName("actionsave")
        self.actionsave_2 = QtWidgets.QAction(MainWindow)
        self.actionsave_2.setObjectName("actionsave_2")
        self.actionData_Cleaning = QtWidgets.QAction(MainWindow)
        self.actionData_Cleaning.setObjectName("actionData_Cleaning")
        self.actionSeparate = QtWidgets.QAction(MainWindow)
        self.actionSeparate.setObjectName("actionSeparate")
        #一级菜单添加二级菜单
        self.menufile.addAction(self.actionopen)
        self.menufile.addAction(self.actionsave)
        self.menufile.addAction(self.actionsave_2)
        self.menuAnalyse.addAction(self.actionData_Cleaning)
        self.menuAnalyse.addAction(self.actionSeparate)
        self.menubar.addAction(self.menufile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuCapture.menuAction())
        self.menubar.addAction(self.menuAnalyse.menuAction())

    def createUi(self,MainWindow):
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self,MainWindow):
        _translate = QtCore.QCoreApplication.translate
        #窗体标题
        MainWindow.setWindowTitle(_translate("MainWindow", "Y"))
        #一级菜单内容
        self.menufile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menuCapture.setTitle(_translate("MainWindow", "Capture"))
        self.menuAnalyse.setTitle(_translate("MainWindow", "Analyse"))
        #二级菜单内容
        self.actionopen.setText(_translate("MainWindow", "Open"))
        self.actionsave.setText(_translate("MainWindow", "Save"))
        self.actionsave_2.setText(_translate("MainWindow", "Save As"))
        self.actionData_Cleaning.setText(_translate("MainWindow", "Data Cleaning"))
        self.actionSeparate.setText(_translate("MainWindow", "Separate"))



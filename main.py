#coding: utf-8

#主函数

from welcome import *
from showfile import *
from readfile import *
from PyQt5.QtWidgets import QFileDialog

class main_function(welcome_Window): #主窗口类
    def __init__(self):
        super(main_function, self).__init__()
        super().createUi(self)
        self.action_event()

        self.child = show_file_Window()

    def action_event(self):
        # 二级菜单事件
        self.actionopen.triggered.connect(self.open_file)
        self.actionsave.triggered.connect(self.save_file)
        self.actionsave_2.triggered.connect(self.save2_file)

    def open_file(self):
        fileName1, filetype1 = QFileDialog.getOpenFileName(self, "选取文件", "C:/", "Pcap Files (*.pcap);;All Files (*)")
        if fileName1:
            self.child.Packet = read_function().read_file(fileName1)
            self.child.tableView_set()
            self.close()
            self.child.show()
        else:
            pass


    def save_file(self):
        fileName2, ok2 = QFileDialog.getSaveFileName(self,"文件保存","C:/","Pcap Files (*.pcap);;All Files (*)")
        fpcap2 = open(fileName2, 'w')
        fpcap2.write('')
        fpcap2.close()

    def save2_file(self):
        fileName3, ok3 = QFileDialog.getSaveFileName(self,"文件保存","C:/","Pcap Files (*.pcap);;Pcapng Files (*.pcapng);;All Files (*)")
        fpcap3 = open(fileName3, 'w')
        fpcap3.write('')
        fpcap3.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mywindow = main_function()
    mywindow.show()
    sys.exit(app.exec_())
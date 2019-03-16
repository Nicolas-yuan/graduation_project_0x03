#coding: utf-8

#数据清洗和流重组，将除tcp外的报文全部清洗

import struct
from operator import itemgetter

# 测试用
from readfile import *

class cleaning_function():

    Packet_cleaning = []    # 初始化list，用于存放清洗后的数据
    Packet_reassemble = []  # 初始化list，用于存放重组后的数据
    #Packet_reassemble = [('1','1','1','1','1','1','1')]  # 初始化list，用于存放重组后的数据
    datastream = []
    datastream2 = []
    stream_len = ''  # 流长度
    stream_Data = ''  # 流数据

    def cleaning_Data(self,Packet):

        # 清洗，非TCP的报文删除，通过倒序删除，不必考虑删完后列表长度改变问题
        for i in range(len(Packet)-1, -1, -1):     # range取头不取尾，所以倒序开始为长度减一，结束为-1
            if Packet[i][5] != 'TCP':
                Packet.pop(i)
            else:
                pass

        self.Packet_cleaning = Packet

        self.Packet_cleaning.pop(30) # 用于测试数据包丢失

        # 流重组
        # 考虑乱序、重复、丢失
        # 乱序在之前的排序后已经解决
        # 重复，seq一样，data也一样
        # 丢失，检验前后seq是否吻合，不过不吻合，记录缺失的seq号，利用下一个包的seq判断丢失包的大小，然后构造假包填充，如0000000
        SYN_flag = False    # 判断SYN是否为1
        FIN_flag = False    # 判断FIN是否为1
        complete_flag = 0   # 0表示不完整，有SYN就+2，有FIN就-1，则1为完整，2为有SYN，-1为有FIN
        complete_text = ''
        seq_before = ''     # 记录上一个报文的seq
        seq_now = ''        # 记录本报文的seq
        len_before = ''     # 记录上一个报文的长度
        len_now = ''        # 记录本报文的长度
        len_total = ''      # 记录流的总长度
        for j in range(0, len(self.Packet_cleaning)):
            # 首先将源IP等信息存入变量
            if self.datastream == [] :
                # 将源IP、目的IP等信息复制到新的包中
                for i in range(1, 5):
                    self.datastream.append(self.Packet_cleaning[j][i])
                # datastream2初始化
                self.datastream2 = self.datastream
                seq_now = int(self.Packet_cleaning[j][7])
                len_now = int(self.Packet_cleaning[j][6])
            else:
                # 将新报文的源IP等信息存储在datastream2中，用于和datastream进行比较，如果一样，则可能属于同一条流
                self.datastream2 = []
                for i in range(1, 5):
                    self.datastream2.append(self.Packet_cleaning[j][i])
                seq_before = seq_now
                len_before = len_now
                seq_now = int(self.Packet_cleaning[j][7])
                len_now = int(self.Packet_cleaning[j][6])

            # 判断数据包的类型：SYN、FIN、ACK、数据包
            if self.Packet_cleaning[j][9] == '':
                if self.Packet_cleaning[j][8][4] == '1':
                    # 如果流数据不是空的，则意味着上一条流已经结束，下面开始是新的流
                    if self.stream_Data != '':
                        # 上一个流已经结束,完成此流重组
                        # 加入完整性信息
                        if complete_flag == 1:
                            self.datastream.insert(0, '完整')
                        elif complete_flag == 0:
                            self.datastream.insert(0, '不完整')
                        elif complete_flag == 2:
                            self.datastream.insert(0, '有SYN标志')
                        elif complete_flag == -1:
                            self.datastream.insert(0, '有FIN标志')
                        else:
                            self.datastream.insert(0,complete_text)
                        # 完整性信息初始化
                        complete_flag = 0
                        # 记录流总长
                        len_total = len(self.stream_Data)
                        # 将流总长度添加进来
                        self.datastream.append(str(len_total))
                        # 将流数据添加进来
                        self.datastream.append(self.stream_Data)
                        # 将列表转化为元组
                        tuple(self.datastream)
                        # 将重组后的流存入变量中
                        self.Packet_reassemble.append(self.datastream)
                        # 将元组转化为列表,将新的源IP等信息存入datastream
                        list(self.datastream)
                        self.datastream = []
                        self.datastream = self.datastream2
                        # 流数据初始化
                        self.stream_Data = ''
                    else:
                        pass
                    # 有SYN，完整性标志就+2,
                    complete_flag += 2
                elif self.Packet_cleaning[j][8][5] == '1':
                    # 有FIN，完整性标志就-1,
                    complete_flag -= 1
                    if self.stream_Data != '':
                        # 上一个流已经结束,完成此流重组
                        # 加入完整性信息
                        if complete_flag == 1:
                            self.datastream.insert(0, '完整')
                        elif complete_flag == 0:
                            self.datastream.insert(0, '不完整')
                        elif complete_flag == 2:
                            self.datastream.insert(0, '有SYN标志')
                        elif complete_flag == -1:
                            self.datastream.insert(0, '有FIN标志')
                        else:
                            self.datastream.insert(0,complete_text)
                        # 完整性信息初始化
                        complete_flag = 0
                        # 记录流总长
                        len_total = len(self.stream_Data)
                        # 将流总长度添加进来
                        self.datastream.append(str(len_total))
                        # 将流数据添加进来
                        self.datastream.append(self.stream_Data)
                        # 将列表转化为元组
                        tuple(self.datastream)
                        # 将重组后的流存入变量中
                        self.Packet_reassemble.append(self.datastream)
                        # 将元组转化为列表,将新的源IP等信息存入datastream
                        list(self.datastream)
                        self.datastream = []
                        self.datastream = self.datastream2
                        # 流数据初始化
                        self.stream_Data = ''
                    else:
                        pass
                else:
                    # 纯ack报文或其他报文，无意义
                    pass
                # 空包丢弃
            else:
                # 数据包类型为数据包时
                # 开始进行流重组
                if self.datastream == self.datastream2:
                    if self.stream_Data == '':
                        # 这是一个有开始标志的新的流，并且之前没有流数据遗留在变量中
                        # 将流数据存入变量中
                        self.stream_Data += self.Packet_cleaning[j][9]
                    else:
                        # 判断seq
                        if seq_now == seq_before + len_before:
                            # 将流数据存入变量中
                            self.stream_Data += self.Packet_cleaning[j][9]
                        elif seq_now > seq_before + len_before:
                            # 报文丢失
                            # 生成填充数据以替代丢失报文
                            padding_len = seq_now - (seq_before + len_before)
                            padding_data = ['0' for _ in range(padding_len)]
                            padding_data = ''.join(padding_data)
                            self.stream_Data += padding_data
                            # 将流数据存入变量中
                            self.stream_Data += self.Packet_cleaning[j][9]
                            # 完整性标识记为丢失数据
                            complete_text = '丢失数据'+str(seq_before+len_before)+'-'+str(seq_now-1)
                            complete_flag += 4
                        elif seq_now == seq_before:
                            # 报文重复
                            pass

                else:
                    if self.stream_Data != '':
                        # 上一个流已经结束,完成此流重组
                        # 加入完整性信息
                        if complete_flag == 1:
                            self.datastream.insert(0, '完整')
                        elif complete_flag == 0:
                            self.datastream.insert(0, '不完整')
                        elif complete_flag == 2:
                            self.datastream.insert(0, '有SYN标志')
                        elif complete_flag == -1:
                            self.datastream.insert(0, '有FIN标志')
                        else:
                            self.datastream.insert(0,complete_text)
                        # 完整性信息初始化
                        complete_flag = 0
                        # 记录流总长
                        len_total = len(self.stream_Data)
                        # 将流总长度添加进来
                        self.datastream.append(str(len_total))
                        # 将流数据添加进来
                        self.datastream.append(self.stream_Data)
                        # 将列表转化为元组
                        tuple(self.datastream)
                        # 将重组后的流存入变量中
                        self.Packet_reassemble.append(self.datastream)
                        # 将元组转化为列表,将新的源IP等信息存入datastream
                        list(self.datastream)
                        self.datastream = []
                        self.datastream = self.datastream2
                        # 流数据初始化
                        self.stream_Data = ''
                        self.stream_Data += self.Packet_cleaning[j][9]
                    else:
                        # 这是一条新的流，并且流的四元组不同
                        self.datastream = []
                        self.datastream = self.datastream2
                        # 流数据初始化
                        self.stream_Data = ''
                        self.stream_Data += self.Packet_cleaning[j][9]




if __name__ == '__main__':
    Packet = read_function().read_file('tcp.pcap')
    Packet = sorted(Packet, key=itemgetter(1, 2, 3, 4, 7))
    cleaning_function().cleaning_Data(Packet)
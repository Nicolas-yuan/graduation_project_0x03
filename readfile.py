#coding: utf-8

#读文件和解析文件
#本程序只解析 linktype = 1 的pcap文件,重点关注TCP、UDP报文

import struct

class read_function():

    def read_file(self,fileName):

        fpcap = open(fileName, 'rb')  # 以二进制打开

        pcapheadlen=24      # pcap头部有24字节
        packetheadlen=16    # 数据包头部，16字节
        Ethheadlen=14       # 802.3以太网帧头，14字节
        LLClen = 8          # 802.2LLC头部
        ipheadlen=20        # ip数据包头部
        tcpheadlen=20       # tcp数据包头部
        udpheadlen=8        # udp首部
        Packet = []         # 初始化list
        FrameType_dic = {b'\x08\x00': 'IPv4', b'\x08\x06': 'ARP', b'\x88\x64': 'PPPoE',
                         b'\x81\x00': '802.1Q tag', b'\x86\xDD': 'IPv6', b'\x88\x47': 'MPLS Label'}
        protocol_dic = {1: 'ICMP', 2: 'IGMP', 6: 'TCP', 17: 'UDP', 88: 'IGRP', 89: 'OSPF'}

        try:
            # 读取pcap文件头
            pcapheaddata = fpcap.read(pcapheadlen)
            (magic, v_major, v_minor, tzone, sigfigs, packetmaxsize, linktype) = struct.unpack("<IHHLLLL", pcapheaddata)

            # 循环读取数据包
            packetheaddata = fpcap.read(packetheadlen) # 读数据包头
            while(packetheaddata):
                data = b'\x00'      # 应用层数据存储区初始化
                data_decode = ''
                srcIP = ''
                dstIP = ''
                srcport = ''         # 初始化源端口
                dstport = ''         # 初始化目的端口
                seqNo = ''          # 序列号初始化
                ackNo = ''          # 确认号初始化
                TCP_flags = ''      # TCP标志位初始化

                # 解析packet包头
                (second, micorsecond, caplen, originallen) = struct.unpack("<LLLL",packetheaddata)
                    # 计算时间
                time = str(second)+'.'+str(micorsecond)

                # 读取链路层帧头
                if linktype == 1:
                    # 读取802.3以太网帧头
                    Ethdata = fpcap.read(Ethheadlen)
                    # 解析以太网帧头
                    (dstMAC, srcMAC, FrameType) = struct.unpack("6s6s2s", Ethdata)
                    # 解析以太网帧类型字段
                    FrameType_dic.setdefault(FrameType, '')  # 设置键默认值，如果键不存在，输出空值
                elif linktype == 100:
                    # 读取802.2LLC数据帧头
                    LLCdata = fpcap.read(LLClen)
                    # 解析帧头
                    (DSAP, SSAP, Control_data, FrameType) = struct.unpack("ss4s2s", LLCdata)
                    # 解析以太网帧类型字段
                    FrameType_dic.setdefault(FrameType, '')  # 设置键默认值，如果键不存在，输出空值

                if FrameType_dic[FrameType] == 'IPv4':
                    # 读取IP头
                    ipheaddata = fpcap.read(ipheadlen)
                    # 解析IP头
                    (Ver_len, tos, totallen, id, flag_seg, ttl,
                     protocol, check, srcip, dstip) = struct.unpack(">ssHHHssH4s4s", ipheaddata)
                    # 计算头部长度
                    ipIHLdata = ord(Ver_len) & 0x0F  # 保留低位4bit
                    # 上层协议
                    protocol = ord(protocol)
                    protocol_dic.setdefault(protocol, '')  # 设置键默认值，如果键不存在，输出空值
                    # IP地址
                    srcIP = str(srcip[0]) + '.' + str(srcip[1]) + '.' + str(srcip[2]) + '.' + str(srcip[3])
                    dstIP = str(dstip[0]) + '.' + str(dstip[1]) + '.' + str(dstip[2]) + '.' + str(dstip[3])
                    # 读取IP头部可选字段
                    ipheadoptionlen = ipIHLdata*4-ipheadlen
                    ipheadoptional = fpcap.read(ipheadoptionlen)

                    pcktype = protocol_dic[protocol]

                    if protocol == 6:
                        # 读取TCP头
                        tcpheaddata = fpcap.read(tcpheadlen)
                        # 解析TCP头
                        (srcport,dstport,seqNo,ackNo,headlen_flags,
                         window,checksum,urgent_pointer)=struct.unpack('>HHLLHHHH',tcpheaddata)
                        # 计算头部长度
                        tcpreallen = (headlen_flags & 0xF000) >> 12
                        # 解析标志位
                        TCP_flags = (headlen_flags & 0x003F)
                        TCP_flags = '{:06b}'.format(TCP_flags)
                        # 读取TCP头部options内容
                        tcpheadoptions = fpcap.read(tcpreallen*4-tcpheadlen)

                        # 计算应用层数据长度和链路层尾部长度
                        # 用报文的总长度减去以太网首部和ip首部和tcp首部即为tcp payload长度+以太网帧尾长度
                        if linktype == 1:
                            datalen = caplen - Ethheadlen - ipIHLdata * 4 - tcpreallen * 4
                            # 用IP头部totallen字段减去ip首部长度和tcp首部即为tcp payload长度
                            datareallen = totallen - ipIHLdata * 4 - tcpreallen * 4
                        elif linktype == 100:
                            datalen = caplen - LLClen - ipIHLdata * 4 - tcpreallen * 4
                            # 用IP头部totallen字段减去ip首部长度和tcp首部即为tcp payload长度
                            datareallen = totallen - ipIHLdata * 4 - tcpreallen * 4

                    elif protocol == 17:
                        # 读UDP头
                        udpheaddata = fpcap.read(udpheadlen)
                        # 解析UDP头
                        (srcport, dstport,udppcklen,checksum) = struct.unpack('>HHHH', udpheaddata)

                        # 计算应用层数据长度和链路层尾部长度
                        # 用报文总长度减去以太网首部和ip首部和udp首部长度即为udp数据长度+以太网帧尾
                        if linktype == 1:
                            datalen = caplen - Ethheadlen - ipIHLdata * 4 - udpheadlen
                            # udp payload长度
                            datareallen = udppcklen - udpheadlen
                        elif linktype == 100:
                            datalen = caplen - LLClen - ipIHLdata * 4 - udpheadlen
                            # udp payload长度
                            datareallen = udppcklen - udpheadlen

                    else:
                        # 如果报文非TCP和UDP报文，则直接把IP包内容作为Data
                        if linktype == 1:
                            datalen = datareallen = caplen - Ethheadlen - ipIHLdata * 4
                        elif linktype == 100:
                            datalen = datareallen = caplen - LLClen - ipIHLdata * 4
                else:
                    # 如果报文非IPv4报文，则直接把packet包内容作为Data
                    if linktype == 1:
                        datalen = datareallen = caplen - Ethheadlen
                    elif linktype == 100:
                        datalen = datareallen = caplen - LLClen
                    pcktype = FrameType_dic[FrameType]

                # 读取数据区域
                if datalen >= datareallen:
                    data = fpcap.read(datareallen)
                    data_decode = data.decode(encoding='utf-8', errors='ignore')
                    # 读取链路层尾部数据
                    paddingdata = fpcap.read(datalen - datareallen)
                    # 构建解析后的数据包
                    Packet.append((time, srcIP, dstIP, str(srcport), str(dstport), pcktype,
                                   str(datareallen), str(seqNo), TCP_flags, data_decode))
                else:
                    # datalen < datareallen , 表示实际抓包的长度小于包实际长度，则按照实际抓包的长度读取
                    data = fpcap.read(datalen)
                    data_decode = data.decode(encoding='utf-8', errors='ignore')
                    # 构建解析后的数据包
                    Packet.append((time, srcIP, dstIP, str(srcport), str(dstport), pcktype,
                                   str(datalen), str(seqNo), TCP_flags, data_decode))

                packetheaddata = fpcap.read(packetheadlen)
        finally:
            fpcap.close()

        return Packet

if __name__ == '__main__':
    Packet=read_function()
    Packet.read_file('tcp.pcap')

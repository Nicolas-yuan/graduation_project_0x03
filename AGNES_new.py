#coding: utf-8

# 本代码段用于AGNES层次聚类算法，算法采用字符串匹配算法计算距离

from nltk.tokenize import WordPunctTokenizer
import re
import difflib
import Levenshtein
import numpy
from showClustering import *

# 测试用
from readfile import *
from cleaningData import *
from PyQt5.QtWidgets import QFileDialog


class AGNES_function():

    streams = []
    clustering_stream = []
    cluster_words = []
    result_stream_dic = {}

    def Clustering_function(self):
        # 截取用于聚类的前300字节数据
        for stream_data in self.streams:
            self.clustering_stream.append(stream_data[6][0:300])
        # 使用nltk库对流数据进行分词处理
        for stream_str in self.clustering_stream:
            self.cluster_words.append(WordPunctTokenizer().tokenize(stream_str))
        # 用正则表达式过滤非英文字母字符串
        # 倒序删除法
        for stream_words in self.cluster_words:
            for word_index in range(len(stream_words) - 1, -1, -1):
                if re.search(r'[^a-z]',stream_words[word_index] ,re.I)!= None:
                    stream_words.pop(word_index)
                else:
                    pass
        # 对无关单词再过滤，如无意义单词（有效单词库？）、日期？
        pass
        # AGNES层次聚类算法
        # 类簇初始化，每条流作为一个簇
        size = len(self.clustering_stream)
        array_stream = numpy.zeros((size, size), dtype=float)
        # 距离算法
        self.similarword_num(array_stream)

        print(array_stream)

        # AGNES层次聚类
        cluster_num = 0 # 簇标记初始化
        # 类簇初始化
        for item in enumerate(self.streams):
            self.result_stream_dic[cluster_num] = []
            self.result_stream_dic[cluster_num].append(list(item))
            cluster_num += 1
        # 聚类循环
        while(True):
            size = len(self.result_stream_dic)
            if size == 1:
                break
            array_cluster = numpy.zeros((size, size), dtype=float)
            for cluster_num_x in range(size):
                for cluster_num_y in range(size):
                    if cluster_num_x == cluster_num_y:
                        pass
                    else:
                        similar_list = []
                        for stream_data_x in self.result_stream_dic[cluster_num_x]:
                            similar_stream = 0
                            for stream_data_y in self.result_stream_dic[cluster_num_y]:
                                index_x = stream_data_x[0]
                                index_y = stream_data_y[0]
                                # 计算流间距
                                similar_stream += array_stream[index_x][index_y]
                            # 用均值表示cluster1中stream_x对cluster2的相似度
                            similar_stream /= len(self.result_stream_dic[cluster_num_y])
                            similar_list.append(similar_stream)
                        # 用均值表示cluster1对cluster2的相似度
                        for num in similar_list:
                            array_cluster[cluster_num_x][cluster_num_y] += num
                        array_cluster[cluster_num_x][cluster_num_y] = "{:.3f}".format(
                            array_cluster[cluster_num_x][cluster_num_y] / len(self.result_stream_dic[cluster_num_x]))
            # 簇1与簇2的相似度，取簇1对簇2的相似度与簇2对簇1相似度的平均值
            # 取数组对角线，组成一个字典，字典key代表两个簇的index，value代表两个簇的相似度
            similar_dic = {}
            for i in range(size):
                for j in range(i + 1, size):
                    dic_key = str(i) + ' ' + str(j)
                    similar_dic[dic_key] = (array_cluster[i][j] + array_cluster[j][i]) / 2
            # 对字典按照value降序排序
            similar_list = sorted(similar_dic.items(), key=lambda item: item[1], reverse=True)
            #'''
            print('相似度:')
            for i in similar_list:
                print(i)
            #'''
            # 取相似度最大两个簇聚类
            # 符合阈值条件就聚合，不符合结束聚类
            if similar_list[0][1] >= 0.7:
                (index_x, index_y) = similar_list[0][0].split()
                if index_x < index_y:
                    # 把index_y聚类到index_x里，然后把字典最后一项移到index_y里，删去字典最后一项
                    self.result_stream_dic[int(index_x)].extend(self.result_stream_dic[int(index_y)])
                    self.result_stream_dic[int(index_y)] = self.result_stream_dic[size - 1]
                    del self.result_stream_dic[size - 1]
                else:
                    # 把index_x聚类到index_y里，然后把字典最后一项移到index_x里，删去字典最后一项
                    self.result_stream_dic[int(index_y)].extend(self.result_stream_dic[int(index_x)])
                    self.result_stream_dic[int(index_x)] = self.result_stream_dic[size - 1]
                    del self.result_stream_dic[size - 1]
            else:
                break

        for i in self.result_stream_dic:
            for j in range(len(self.result_stream_dic[i])):
                # 删去流数据的index标识
                self.result_stream_dic[i][j] = self.result_stream_dic[i][j][1]


    def similarword_num(self,array):
        # 字符串相似度比较---方法三 自编算法
        # 计算每一个分词在其他字符串中出现的个数
        for i, stream_words1 in enumerate(self.cluster_words):
            for j, stream_words2 in enumerate(self.cluster_words):
                if i != j:
                    similar_num = 0
                    for word in stream_words1:
                        if word in stream_words2:
                            similar_num += 1
                        else:
                            pass
                    # 相似度归一化处理，为stream1在stream2中出现的分词数占stream1分词总数的比例
                    stream_words1_len = len(stream_words1)
                    if stream_words1_len >0:
                        array[i][j] = similar_num / len(stream_words1)
                    else:
                        array[i][j] = 0
                    '''
                    # 取stream长度小的相似度作为stream1与stream2的相似度
                    if len(stream_words1) < len(stream_words2):
                        array[j][i] = array[i][j]
                    else:
                        array[i][j] = array[j][i]
                    '''
                else:
                    pass







if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mywindow = show_Dataclustering_Window()
    # 打开文件
    fileName, filetype = QFileDialog.getOpenFileName(mywindow, "选取文件", "E:/bishe/test/GUI_test/data", "Pcap Files (*.pcap);;All Files (*)")
    Packet = read_function().read_file(fileName)
    # 排序
    Packet = sorted(Packet, key=itemgetter(1, 2, 3, 4, 7))
    # 数据清洗
    stream = cleaning_function()
    stream.cleaning_Data(Packet)
    # print(stream.Packet_reassemble[0])
    # 聚类
    AGNES_instance = AGNES_function()
    AGNES_instance.streams = stream.Packet_reassemble
    AGNES_instance.Clustering_function()
    # 显示结果
    mywindow.Packet_clustering = AGNES_instance.result_stream_dic
    mywindow.tableView_set()
    mywindow.show()
    app.exec_()
    sys.exit()
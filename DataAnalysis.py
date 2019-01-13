# coding: utf-8
import matplotlib.pyplot as plt
import matplotlib
from collections import Counter
import jieba.analyse
from pylab import mpl

class DataAnalysis:
    def __init__(self):
        '''
        - self.stopwords是补充通用词列表
        - self.stopwordTxt会从txt文件加载停用词
        '''
        self.stopwords = ['围观','微博','问答','全文','网页','回答','一起','问题','话筒','收起','一键','支付','抽取','赠送','抽奖','开奖','展开','粉丝','小哏',',','月','日','年','安','秋山君','时间','名','用户','派','视频','转发','关注','说']
        self.stopwordTxt = []

    def Initialization(self):
        '''
        - 设置matplotlib字体，黑体
        - 加载停用词
        - 将停用词字符转化为数组
        - 打印个数
        :return:
        '''
        mpl.rcParams['font.sans-serif'] = ['SimHei']
        file = open('Settings/stopwords.txt', encoding='utf-8', errors='ignore').read()
        self.stopwordTxt = file.split(',') + self.stopwords
        print('停用词个数：'+str(len(self.stopwordTxt)))

    def process(self,text,stopwords = []):
        '''
        :param text: 将要进行分词处理的文本
        :param stopwords: 停用词数组
        :return: 取出停用词后的文本数组
        '''
        words = jieba.cut_for_search(text)
        return [word for word in words if word not in stopwords]

    def readFile(self,str):
        '''
        :param str: 决定加载Data文件夹下的哪个分目录
        :return: 返回file对象
        '''
        file = open('Data/'+str+'/txt.txt', encoding='GBK', errors='ignore').read()
        return file

    def startAnalysis(self,str,num):
        '''
        :param str: 为process函数提供的目录参数
        :param num: 显示的词数
        :return: 控制台输出
        '''
        wordList = self.process(self.readFile(str),self.stopwordTxt)
        wordCount = Counter()
        wordCount.update(wordList)
        for tag,count in wordCount.most_common(num):
            print("{}: {}".format(tag,count))

    def graph(self,str,num):
        '''
        :param str: 为process函数提供的目录参数
        :param num: 显示的词数
        :return: 绘图显示
        - 加载过滤停用词后的汉字数组
        - 生成wordCount对象
        - 获得技数列
        - 获得标签列
        - 生成x轴数组
        - 开始绘图
        - 设置title
        - 设置为柱状图
        - 为x轴添加标签
        - 设置保存位置
        - 显示
        '''
        wordList = self.process(self.readFile(str),self.stopwordTxt)
        wordCount = Counter()
        wordCount.update(wordList)
        y = [count for tag,count in wordCount.most_common(num)]
        tag = [tag for tag,count in wordCount.most_common(num)]
        x = range(1,len(y)+1)
        plt.bar(x,y)
        plt.title('比特币主题微博热词')
        plt.ylabel('Frequency')
        plt.xticks(x,tag)  #加label
        plt.savefig('picture/'+str+'.png')
        plt.show()



da = DataAnalysis()
da.Initialization()
#通过选择不同的参数：up,down,done来统计不同时期的数据
da.startAnalysis('down',30)
#da.graph('up',30)


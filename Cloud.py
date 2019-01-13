# coding: utf-8
from os import path
from PIL import Image
import numpy as np
from wordcloud import WordCloud, STOPWORDS
from Python3.DataAnalysis import *


class Cloud:

    def __init__(self):
        '''
        - 通过self.site控制分析方向，选择文件夹
        - 生成DataAnalysis实例，借用jieba分词部分代码
        - 加载文本字符串和底片
        '''
        self.site = 'up'
        self.d = path.dirname(__file__)
        self.text_ = open(path.join(self.d,'Data/'+self.site+'/txt.txt')).read()

        da = DataAnalysis()
        da.Initialization()

        self.text = ','.join(str(i) for i in da.process(self.text_,da.stopwordTxt))
        self._mask = np.array(Image.open(path.join(self.d,"Settings/bit_mask.png")))

    def getCloud(self):
        '''
        - 生成WordCloud对象，设置背景色，云词数量，底片，及中文字体
        - 使用WordCloud处理文本
        - 输出图像
        - 运行时显示结果图片
        - 运行时显示底片

        :return:
        '''

        wc = WordCloud(background_color="white", max_words=100, mask=self._mask,font_path="Settings/simsun.ttf")
        wc.generate(self.text)
        wc.to_file(path.join(self.d, "picture/bit.png"))

        plt.imshow(wc, interpolation='bilinear')
        plt.axis("off")
        plt.figure()
        plt.imshow(self._mask, cmap=plt.cm.gray, interpolation='bilinear')
        plt.axis("off")
        plt.show()

cl = Cloud()
cl.getCloud()
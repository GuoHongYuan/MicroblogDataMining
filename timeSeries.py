# coding: utf-8
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

class timeSeries:

    def __init__(self):
        '''
        - self.str 通过指定不同的文件夹名称，来分析不同的时间序列
        - self.timeList 用来储存规范化的时间字符串
        - self.dataScreen 与self.str对应，用来过滤异常时间，如查询范围为2018年，过滤掉除2018年的数据
        '''
        self.str = 'down'

        self.timearr = np.load('E:\DataAnalysis\\tools\python3\project\Python3\Data\\'+self.str+'\\timeList.npy')
        self.timeList = []
        self.dataScreen = {
            'up':['2017','12'],
            'down':['2017','12'],
            'done':['2018','02']
        }

    def getTime(self):
        '''
        - 原始时间为 年 月 日 形式，需要将年，月，日，转换为 ‘-’ 才能进而转换为时间 如 2000年01月01日 转换为 2000-01-01
        - 使用split方法分隔 如 split('年') 可将 2000年01月01日 分为 ['2000','01月01日']的数组，继而对后面的'月','日'继续分组。
        - if语句为过滤不正常时间
        :return:
        '''

        try:
            for timestr in self.timearr:
                yearSplit = timestr.split('年')
                year = yearSplit[0]
                if year == self.dataScreen[self.str][0]:
                    monthSplit = yearSplit[1].split('月')
                    month = monthSplit[0]
                    if month == self.dataScreen[self.str][1] :
                        daySplit = monthSplit[1].split('日')
                        day = daySplit[0]
                        hourSplit = daySplit[1].split(':')
                        hour = hourSplit[0].strip()
                        min = hourSplit[1]
                        time = year+'-'+month+'-'+day+' '+hour+':'+min
                        self.timeList.append(time)
        except:
            print('数据无法转换成时间')

    def Rsampling(self):
        '''
        - index_ 是转换为DatetimeIndex的时间序列，将作为timeSeries_的索引，timeSeries_的值清一色为1，便于核算。
        :return:
        '''
        index_ = pd.DatetimeIndex(self.timeList)
        timeSeries_ = pd.Series(1,index=index_)
        timeSeries__ = timeSeries_.resample('H').sum()
        print(timeSeries__)
        ax = timeSeries__.plot()
        plt.show()
        ax.get_figure().savefig('picture/' + self.str + '_time.png')

ts = timeSeries()
ts.getTime()
ts.Rsampling()








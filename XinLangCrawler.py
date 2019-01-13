import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import urllib.request as urllib2
import numpy
import re
from lxml import etree
from bs4 import BeautifulSoup
import json
from urllib import parse
import re
import time


class XinLangCrawler:

    def __init__(self):
        '''
        - key是url中的汉字，需要编码才能进行request访问
        - url_UP是比特币暴涨时间段的微博url
        - url_Down是比特币开始暴跌时间段的微博url
        - url_Done是比特币完全暴跌时间段的微博url
        - pageCount是微博页数，一般历史数据为50页
        '''

        key = '比特币'
        self.url_UP = 'https://s.weibo.com/weibo/' + urllib.parse.quote(key) + '?q=' + urllib.parse.quote(key) + '&typeall=1&suball=1&timescope=custom:2017-12-15:2017-12-18&Refer=g&page='
        self.url_Down = 'https://s.weibo.com/weibo/' + urllib.parse.quote(key) + '?q=' + urllib.parse.quote(key) + '&typeall=1&suball=1&timescope=custom:2017-12-18:2017-12-25&Refer=g&page='
        self.url_Done = 'https://s.weibo.com/weibo/' + urllib.parse.quote(key) + '?q=' + urllib.parse.quote(key) + '&typeall=1&suball=1&timescope=custom:2018-02-04:2018-02-06&Refer=g&page='
        self.pageCount = 50

        self.txt = ''
        self.timeList = {}
        self.fromTxt = ''


    def Initialization(self):
        '''
        初始化函数，每调用一次清空容器
        :return:
        '''
        self.txt = ''
        self.timeList = []
        self.fromList = ''

    def getHtml(self,url,pageCount):
        '''
        :param url: 要访问的url
        :param pageCount: 第几页
        :return: 返回html
        '''

        request = urllib2.Request(url=url+str(pageCount),headers={})
        response = urllib2.urlopen(request)
        html = response.read().decode('UTF-8')
        return html

    def getText(self,url,site):
        '''
        - 迭代产生url
        - 获取html
        - 使用BeautifulSoup解析网页
        :return: 无返回值
        '''
        self.Initialization() #清空数据

        for i in range(self.pageCount+1):
            html = self.getHtml(url,i)
            soup = BeautifulSoup(html, 'html.parser')
            for div in soup.find_all('div',class_="card-wrap"):
                try:
                    contectArraay = div.find('div',class_="content").find_all('p',class_="txt")
                    contextStr = ','.join(str(i) for i in contectArraay)
                    contextText = self.getChinese(contextStr)
                    timeText = div.find('p',class_="from").find_all('a')[0].string.strip() #strip为字符串去空格函数
                    fromText = div.find('p', class_="from").find_all('a')[1].string.strip()
                    self.txt = self.txt + ','.join(str(i) for i in contextText)
                    self.timeList.append(timeText)
                    self.fromList = self.fromList+fromText+','
                except:
                    print('None')
        self.SaveData(site)
    def getChinese(self,str):
        '''
        :param str: 传入要处理的字符串
        :return: 通过正则表达式仅获得其中中文部分
        '''
        pattern = "[\u4e00-\u9fa5]+"
        regex = re.compile(pattern)
        results = regex.findall(str)
        return results

    def SaveData(self,site):
        '''
        :param site: 文件夹位置
        :return: 储存后的文件
        '''
        file1 = open("E:\DataAnalysis\\tools\python3\project\Python3\Data\\"+site+"\\txt.txt", 'w')
        file1.write(self.txt)
        file1.close()
        numpy.save("E:\DataAnalysis\\tools\python3\project\Python3\Data\\"+site+"\\timeList.npy", self.timeList)
        file2 = open("E:\DataAnalysis\\tools\python3\project\Python3\Data\\"+site+"\\fromList.txt", 'w',encoding='utf-8')
        file2.write(self.fromList)
        file2.close()
    def StartCrawler(self):
        '''
        :return: 启动爬虫，并将结果保存到不同位置
        '''
        self.getText(self.url_UP,'up')
        self.getText(self.url_Down,'down')
        self.getText(self.url_Done,'done')


xl = XinLangCrawler()
xl.StartCrawler()


# -*- coding: utf-8 -*-
# @Time    : 2020/7/16 14:18
# @Author  : suhong
# @File    : zgjkjy.py
# @Software: PyCharm
import json


import requests
from parsel import Selector
import re
import parent

Parent = parent.Parent()


class zgjk(object):
    def __init__(self):
        self.url = "http://www.zgjkjy.org/Magazine/Default.aspx"
        self.ero = 0
        self.suc = 0
        self.cnt = 0
        self.all_num = 0
        self.title_c = 1
        self.journal = '中国健康教育'
        self.sn = requests.Session()
        self.__VIEWSTATE = None
        self.__EVENTVALIDATION = None
        self.__VIEWSTATEGENERATOR = None
        self.headers = {
            #"Content-Type":"application/x-www-form-urlencoded",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Host": "www.zgjkjy.org",
            "Origin": "http://www.zgjkjy.org",
            "Cookie":"SiteID=zgjkjy",
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
        }

    def get_session(self):
        url = "http://www.zgjkjy.org/UserServer/Login.aspx?SiteID=zgjkjy"
        data = {
            '__VIEWSTATE': '/wEPDwULLTExNzE2MjM2NTVkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYCBQtja2JSZW1lbWJlcgUIYnRuTG9naW76RrmYZYfx1chBwTJknlUtOWAwdg==',
            '__VIEWSTATEGENERATOR': '0FFF2A42',
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__EVENTVALIDATION': '/wEWBQLr1fizDgKl1bKzCQK1qbSRCwLkx4D4DAKC3IeGDHwfxY+PaZLbnyRo23CckJAFUl6k',
            'txtUserName': 'xmyim26@163.com',
            'txtPassword': '728708',
            'btnLogin.x': 65,
            'btnLogin.y': 20,
        }
        try:
            r = self.sn.post(url=url, data=data,headers=self.headers,allow_redirects=False)
            if r.status_code != 302:
                print(r.status_code)
                return 0
            # cookies = r.cookies

        except Exception as e:
            print(e)
            print("登陆失败")

    def get_canshu(self):
        try:
            r = self.sn.get(self.url)
            r.encoding = r.apparent_encoding
            html = Selector(r.text)
            self.__VIEWSTATE = html.xpath("//input[@id = '__VIEWSTATE']/@value").extract_first()
            self.__VIEWSTATEGENERATOR = html.xpath("//input[@id = '__VIEWSTATEGENERATOR']/@value").extract_first()
            self.__EVENTVALIDATION = html.xpath("//input[@id = '__EVENTVALIDATION']/@value").extract_first()
            print("初始化参数成功")
        except Exception as e:
            print(e)




    def down_pdf(self, years, num, pdfRoot):
        years = str(years)
        num = str(num)
        self.get_session()
        self.get_canshu()
        self.get_all_num(years,num)
        # 第一页访问
        data = {
            '__VIEWSTATE': self.__VIEWSTATE,
            '__VIEWSTATEGENERATOR': self.__VIEWSTATEGENERATOR,
            '__EVENTTARGET': 'pageControl',
            '__EVENTARGUMENT': '1',
            '__EVENTVALIDATION': self.__EVENTVALIDATION,

            'ddlYear': years,
            'ddlMagazine': num,
            'ddlMenu': '',
            'ddlType': 'Keywords',
            'txtKey': '',
            'btnSearch': '查询',

        }
        r = self.sn.post(self.url, data=data,headers=self.headers)
        r.encoding = r.apparent_encoding
        self.savepdf(years,num,pdfRoot,r.text)
        del data['btnSearch']
        page = 1
        while True:
            page +=1
            html = Selector(r.text)
            if r.text.find("PageClass") > 1:
                __VIEWSTATE = html.xpath("//input[@id = '__VIEWSTATE']/@value").extract_first()
                __VIEWSTATEGENERATOR = html.xpath("//input[@id = '__VIEWSTATEGENERATOR']/@value").extract_first()
                __EVENTVALIDATION = html.xpath("//input[@id = '__EVENTVALIDATION']/@value").extract_first()
                data['__VIEWSTATE'] = __VIEWSTATE
                data['__VIEWSTATEGENERATOR'] = __VIEWSTATEGENERATOR
                data['__EVENTVALIDATION'] = __EVENTVALIDATION
                data['__EVENTARGUMENT'] = page
            r = self.sn.post(self.url, data=data, headers=self.headers)
            r.encoding = r.apparent_encoding
            self.savepdf(years, num, pdfRoot, r.text)
            if r.text.find("PageClass") < 0:
                return True
                break

    def get_all_num(self, years, num):
        self.get_session()
        self.get_canshu()
        # 第一页访问
        data = {
            '__VIEWSTATE': self.__VIEWSTATE,
            '__VIEWSTATEGENERATOR': self.__VIEWSTATEGENERATOR,
            '__EVENTTARGET': 'pageControl',
            '__EVENTARGUMENT': '1',
            '__EVENTVALIDATION': self.__EVENTVALIDATION,

            'ddlYear': years,
            'ddlMagazine': num,
            'ddlMenu': '',
            'ddlType': 'Keywords',
            'txtKey': '',
            'btnSearch': '查询',

        }
        r = self.sn.post(self.url, data=data, headers=self.headers)
        r.encoding = r.apparent_encoding
        del data['btnSearch']
        page = 0
        while True:
            page += 1
            html = Selector(r.text)
            if r.text.find("PageClass") > 1:
                __VIEWSTATE = html.xpath("//input[@id = '__VIEWSTATE']/@value").extract_first()
                __VIEWSTATEGENERATOR = html.xpath("//input[@id = '__VIEWSTATEGENERATOR']/@value").extract_first()
                __EVENTVALIDATION = html.xpath("//input[@id = '__EVENTVALIDATION']/@value").extract_first()
                data['__VIEWSTATE'] = __VIEWSTATE
                data['__VIEWSTATEGENERATOR'] = __VIEWSTATEGENERATOR
                data['__EVENTVALIDATION'] = __EVENTVALIDATION
                data['__EVENTARGUMENT'] = page
            r = self.sn.post(self.url, data=data, headers=self.headers)
            r.encoding = r.apparent_encoding
            html = Selector(r.text)
            tr_list = html.xpath("//tr[@class='MagazineTitle']")
            self.all_num += len(tr_list)
            if r.text.find("PageClass") < 0:
                break

    def savepdf(self,years,num,pdfRoot,html):
        html = Selector(html)
        tr_list = html.xpath("//tr[@class='MagazineTitle']")
        for tr in tr_list:
            link = tr.xpath(".//a/@href").extract_first()
            info = tr.xpath("./td[@class='PageClass']/text()").extract_first()
            info = info.strip().replace("\r","")
            pattern = '\):(.*)'
            xx = re.findall(pattern,info)
            url = "http://www.zgjkjy.org"+link.replace("Show.aspx","PDFShow.aspx")
            title = xx[0]
            print("pdf下载链接：%s" % url)
            pdfFilePath = Parent.makedir(self.journal, str(years), str(num), title, pdfRoot)
            print('--------开始下载---------: %s' % title)

            if pdfFilePath == 1:
                self.suc += 1
                continue
            fig = Parent.getPdfbysn(self.sn,url, title, pdfFilePath, self.headers)
            if fig == -1:
                self.ero += 1
                line = 'journal: %s, years: %s, issue: %s: %s 下载失败' % (
                    self.journal, years, num, title.strip())
                line = line + '\n'
                Parent.Record(line, self.journal)
            if fig == 1:
                print('%s,pdf下载成功' % title)
                self.suc += 1
                line = 'journal: %s, years: %s, issue: %s。共有文章 %d；下载PDF %d；失败 %d' % (
                    self.journal, years, num, self.all_num, self.suc, self.ero)
                line = line + '\n'
                Parent.Record(line, self.journal)





# if __name__ == '__main__':
#
#     z = zgjk()
#     # z.down_pdf()
#     z.down_pdf(2020,5,'1')

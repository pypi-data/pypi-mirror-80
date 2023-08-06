# -*- coding: utf-8 -*-
# @Time    : 2020/6/10 10:08
# @Author  : suhong
# @File    : wangfang_pdf_down.py
# @Software: PyCharm

# # 同项目调用基础包
# import os
# import sys
#
# filepath = os.path.abspath(__file__)
# pathlist = filepath.split(os.sep)
# pathlist = pathlist[:-5]
# TopPath = os.sep.join(pathlist)
# sys.path.insert(0, TopPath)
# print(TopPath)

import json
import os
from parsel import Selector
from urllib import parse
import requests
import time

import toml
from re_common.baselibrary.utils.basedir import BaseDir




from bs4 import BeautifulSoup


class Down(object):
    def __init__(self):
        self.sn = None
        self.index_url = "http://www.wanfangdata.com.cn/sns/third-web/per/perio/articleList"
        self.perioname = None
        self.publishYear = None
        self.issueNum = None
        self.proxies = None
        self.perioId = None
        self.pdf_path = None
        self.UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'


    def read_toml(self):
        cfgFile = r"./config.toml"
        with open(cfgFile, mode='rb') as f:
            content = f.read()
        if content.startswith(b'\xef\xbb\xbf'):  # 去掉 utf8 bom 头
            content = content[3:]
        config = toml.loads(content.decode('utf8'))
        self.pdf_path = config['pdf_path']
        BaseDir.create_dir(self.pdf_path)
        proxy = config['proxy']
        self.proxies = {
            "http": proxy,
            "https": proxy,
        }
        for info in config['info']['NameList']:
            self.perioname, self.publishYear, self.issueNum = info[0], info[1], info[2]
            print("开始下载{}-{}年-{}期".format(self.perioname, self.publishYear, self.issueNum))
            self.get_id()


    def get_perioid(self):
        url = "http://www.wanfangdata.com.cn/search/searchList.do?searchType=perioInfo&showType=detail&pageSize=20&searchWord={}&isTriggerTag=".format(
            parse.quote(self.perioname))
        r = requests.get(url)
        html = Selector(r.text)
        id_ = html.xpath("//div[@class='title title_h']//a[@class='perInfo_block_title']/@href").extract_first("")
        self.perioId = id_.replace("/perio/detail.do?perio_id=", "")

    def get_id(self):
        self.get_perioid()
        self.Tmp_pdf = r'{}/{}/{}/{}'.format(self.pdf_path,self.perioname, self.publishYear, self.issueNum)
        if not os.path.exists(self.Tmp_pdf):
            os.makedirs(self.Tmp_pdf)
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
            "Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8"
        }
        xxx = {
            "page": 1,
            "pageSize": 60,
            "perioId": self.perioId,
            "title": "",
            "publishYear": self.publishYear,
            "issueNum": self.issueNum,
            "otherYear": ""
        }
        r = requests.post(self.index_url, data=xxx)
        print(r.text)
        json_data = json.loads(r.text)
        all_num = json_data['totalRow']
        print("pdf数量：{}".format(all_num))
        max_page = int(all_num // 60) + 1
        for page in range(1, max_page + 1):
            data = {
                "page": page,
                "pageSize": 60,
                "perioId": self.perioId,
                "title": "",
                "publishYear": self.publishYear,
                "issueNum": self.issueNum,
                "otherYear": ""
            }
            r = requests.post(self.index_url, data=data)
            json_data = json.loads(r.text)
            for info in json_data['pageRow']:
                self.sn = requests.Session()
                self.sn.headers['User-Agent'] = self.UserAgent
                rtn = self.down_one(info)
                if rtn[0] != 1:
                    print("下载失败")
                    continue
                    # return -1 * rtn[0]
                r = rtn[1][0]
                title = rtn[1][1]
                title = BaseDir.replace_dir_special_string(title)
                pdf_path = r"{}/{}.pdf".format(self.Tmp_pdf, title)
                if os.path.exists(pdf_path):
                    print("{}存在".format(pdf_path))
                    continue

                self.sava_pdf(r, title)
                time.sleep(2)

    def sava_pdf(self, res, title):
        pdf_path = r"{}/{}.pdf".format(self.Tmp_pdf, title)
        try:
            with open(pdf_path, mode='wb') as f:
                f.write(res.content)
                print("缓存PDF至本地成功:{}".format(title))
            return 1
        except:
            print("缓存PDF至本地失败:{}".format(title))
            return 0

    def down_one(self, info):
        rawid = info['article_id']
        title = info['title']
        doctype = "perio"

        pdfUrl = r"http://oss.wanfangdata.com.cn/file/download/perio_{}.aspx".format(rawid)
        self.sn.headers['Referer'] = r'http://www.wanfangdata.com.cn/pay/downloadliterature.do?_type=%s&id=%s' % (
        doctype, rawid)
        try:
            r = self.sn.get(url=pdfUrl, proxies=self.proxies, timeout=30)
        except Exception as e:
            print(e)
            return 0,0
        html = r.content.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        aTag = soup.find('iframe', id='downloadIframe')

        if not aTag:
            print('{}所查找的文献详情页无下载链接'.format(rawid))
            return -2, 0
        pdfUrl = aTag.get("src")
        pdfUrl = r"http://oss.wanfangdata.com.cn" + pdfUrl
        try:
            r = self.sn.get(url=pdfUrl, proxies=self.proxies, timeout=30)
        except Exception as e:
            print(e)
            return 0,0
        if r.status_code != 200:
            return 0,0
        return 1, (r, title)


if __name__ == '__main__':

    d = Down()
    d.read_toml()

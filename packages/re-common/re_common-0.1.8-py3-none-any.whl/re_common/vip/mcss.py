# -*- coding: utf-8 -*-
# @Time    : 2020/9/16 13:18
# @Author  : suhong
# @File    : mcss.py
# @Software: PyCharm
from parsel import Selector
class MParsel(object):
    def __init__(self,logger=None):
        if logger is None:
            from re_common.baselibrary import MLogger
            logger = MLogger().streamlogger
        self.logger = logger



    def css_parsel_html(self,html="",css_selector={}):
        if html != "" and css_selector:
            sel = Selector(html)
            dict_ = dict()
            for key,value in css_selector.items():
                dict_[key] = sel.css(value).getall()
            return True,dict_
        else:
            return False,""

    def asd(self):
        pass

if __name__ == '__main__':
    htmlText = r'''
    <body>
        <div class="book">111</div>
        <div class="journal_name">222</div>
        <div class="title">333</div>
        <a class ="link">link1</a>
        <a class ="link">link2</a>
        <a class ="link">link3</a>
    </body>
'''

    mc = MParsel()
    css_selector = {
        'book':'div[class="book"]::text',
        'journal_name':'div[class="journal_name"]::text',
        'title':'div[class="title"]::text',
        'link' :'a[class*="link"]::text'

    }
    bools,new_dict = mc.css_parsel_html(htmlText,css_selector=css_selector)
    print(new_dict)
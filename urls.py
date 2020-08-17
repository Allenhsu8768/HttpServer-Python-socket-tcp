# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 18:54:03 2020

@author: notbo
"""

'''此模塊是設置能夠處理的數據請求(所有可以被訪問的 urls列表)'''


# 導入view 的具體方法使用處理數據請求再將方法結果,傳回給框架 WebFrame訊息
from view import *

#把所有能夠處理的urls 都寫在列表中
#每一個元組都對應一個函數處理
urls = [
        ('/time',show_time),
        ('/hello',say_hello),
        ('/bye',say_bye)]


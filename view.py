# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 18:59:46 2020

@author: notbo
"""

'''此模塊是用來處理 urls.py 中的數據請求函數,
urls.py 元組中的函數都是在此處理


---2.WebFrame --
              |--2.2 views.py(應用處理程序:處理httpserver發來的數據請求)
              
'''



#導入時間模塊
from time import ctime


# 1 .show_time 函數
def show_time():
    return ctime()


# 2. say_hello 函數
def say_hello():
    return 'Hello world'

# 3.say_bye 函數
def say_bye():
    return 'Bye'
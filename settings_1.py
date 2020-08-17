# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 19:23:01 2020

@author: notbo
"""

''' 此模塊 setting 是用來 設置 HttpServer.py 的端口配置

#  project ----1.httpserver --
#                            |-1.2 settings.py(httpserver配置:)

# HTTP Server配置文件
'''


# 配置文件是暴露給後端的,需要什麼配置他會提供給你變量名在提供給妳進行配置就可以了
# HttpServer地址
HOST ='0.0.0.0'
PORT = 8000
ADDR = (HOST,PORT)



#WebFrame的地址
frame_ip = '127.0.0.1'
frame_port = 8080
frame_addr = (frame_ip,frame_port)

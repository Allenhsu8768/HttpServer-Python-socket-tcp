# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 22:01:18 2020

@author: notbo
"""

'''此檔案模塊 此模塊檔案 用來接收 HttpServer.py 的請求訊息
然後根據請求訊息,執行本機的應用程序請求訊息(Httpserver.py服務端接收的瀏覽器訊息)
,在本機器執行後端應用的程序框架

----2.WebFrame --
                |--2.5 WebFrame.py(主程序代碼:通過代碼具體執行功能,其他功能都是用來調用)

#       webFrame:
#             從httpserver接收具體請求(創建套接字,接收請求)
#             根據請求進行邏輯處理和數據處理
#                  * 靜態頁面
#                  * 邏輯數據
#             將需要的數據反饋給httpserver



'''


#1.導入模塊連接socket 連接服務端
from socket import *

#2.導入settings 內中設置的參數
from settings_2 import *

#3.導入time 防止訊息接收產生沾包
from time import sleep


#4.導入traceback 打印錯誤訊息
import traceback 


#5.導入 sys 控制套接字關閉
import sys

#6.導入urls 能夠處理個請求數據(能夠處理的數據列表方法)
from urls import *

#7.導入view 呼叫數據能夠處理的函數 urls元組中的函數(能夠具體處理的方法) 
from view import *


#數據處理也是寫在一個類之中(數據處理)
class Application(object):
    #初始化
    def __init__(self):
        self.sockfd = socket()
        #設置端口
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        #綁定本機的地址,在WeFrame資料夾中一樣有一個setting.py的參數設置可以導入
        self.sockfd.bind(frame_addr)
    
    #寫一個函數start()啟動監聽
    def start(self):
        self.sockfd.listen(5)
        # while True循環收發訊息Httpserver多個請求訊息
        while True:
            #利用try來捕捉錯誤
            try:
                #連接HttpServer的請求客戶socket套接
                #連接的處理只是一次性的(Httpserver請求,因為Httpserver線程
                #接收到框架WeFram的處理數據訊息後,就關閉線程,因此處理只需要一次性即可)
                print('----------Listen port ------ %s' % frame_addr[1])
                connfd,addr = self.sockfd.accept()
                print('---------Connect for-------- ',addr)
                #1.接收到具體請求方法
                method = connfd.recv(128).decode()
                #2.接收具體請求內容
                path = connfd.recv(128).decode()
                
                #顯打印接收內容確保請求內容能夠被傳過來
                print(method,path)

            except KeyboardInterrupt: #ctil + c退出服務器
                self.sockfd.close()
                sys.exit('服務器退出')
            except Exception:
                traceback.print_exc()
                continue
                
            #寫請求方法和請求內容的判斷:
            if method == 'GET':
                #處理靜態網頁
                if path == '/' or path[-5:] == '.html':
                    #接收傳回來的元組訊息(響應碼,響應體)
                    status,response_body = self.get_html(path)

                #處理數據請求
                else:
                    status,response_body = self.get_data(path)
                    
                #直接把要傳回的訊息放在外面,將結果給HttpServer
                connfd.send(status.encode())
                #防止沾包
                sleep(0.1)
                connfd.send(response_body.encode())
            
    #寫一個函數 get_html() 處理靜態網頁
    def get_html(self,path):
        if path == '/':
            get_file = static_dir + '/index.html'
        else:
            get_file = static_dir + path
        
        #加入try,捕捉打開文件可能發生的錯誤
        try:
            #如果是在linux環境下執行,則直接打開文件就可以
            #f = open(filename)
            #如果不是使用linux環境下執行,在windiws下則必須在開啟文件的後方加入 encoding = 'utf-8'
            #否則會發生編碼的錯誤
            f = open(get_file,'r',encoding = 'utf-8')
        except IOError:
            #只要把響應碼和響應體返回Httpserver就好,其他都是傳回去給HttpServer來組織返回瀏覽器
            response = ('404','============sorry not found the page=========')
        else:
            response = ('200',f.read())
        finally:
            return response
        
            
    #寫一個函數 get_data() 處理數據請求
    def get_data(self,path):
        #用for循環遍歷 urls列表
        for url,handler in urls: # url , handler 遍歷結果為 ('\time',show_time)
            if path == url:
                response_body = handler() # handler = show_time()  
                return '200',response_body
        return '404','Sorry, Not found the data'
    







#啟動程序
if __name__ == '__main__':
    #創建app對象
    app = Application()
    
    #啟動框架等待request
    app.start()


































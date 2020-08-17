# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 19:05:22 2020

@author: notbo
"""

'''此模塊為檔案為 HttpServer.py (主程序:所有的功能處理都是在這個程序來寫)

Project----1.httpserver --
                          |1.1 HttpServer.py(主程序:所有的功能處理都是在這個程序來寫)

#功能:
#       httpserver:
#            獲取http請求
#            解析http請求
#            將請求發送給webFrame
#               從webFrame接收反饋數據
#                   將數據組織為Reponse格式發送給客戶端


coding = utf-8
name : Allen
time : 2020-08-14
'''

#導入模塊
# 1.socket 和客戶端進行通訊
from socket import *
# 2.sys 退出進程需要
import sys
# 3.re 做正則表達式的一個選擇,以請求行為組利用匹配請求內容
import re
# 4.使用多線程併發
from threading import Thread
# 5.HtteServer的配置模塊,需要導入Settings進來
from settings_1 import *
# 6.睡眠或是獲取當前時間
import time
# 7.打印出錯誤訊息
import traceback



#定義一個class HTTPServer類
class HTTPServer(object):
    #初始化函數,addr 設定默認地址,要是不傳參數的話就使用默認地址
    def __init__(self,addr =('0.0.0.0',80)):
        #創建socket套接字、使用tcp套接字
        self.sockfd = socket(AF_INET,SOCK_STREAM)
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1) 
        self.addr = addr
        #綁定地址
        self.bind(addr)

    #綁定地址(假如有其他地址端口則重新設置一次變量綁定地址)
    def bind(self,addr):
        #綁定地址
        self.ip = addr[0]
        self.port = addr[1]
        self.sockfd.bind(addr)
    
    #Http服務器啟動服務器
    def server_forever(self):
        #設置監聽
        self.sockfd.listen(5)        
        #打印端口訊息
        print('---Listen port---%s' % self.port)
        
        #等待客戶端連接
        #循環收發while True
        while True:
            #加入try 捕捉錯誤
            try:
                #connfd 不需要建立類屬性 self.connfd 
                #會有很多客戶端不同連接,如果使用self.connfd 
                #每次連接會被覆蓋就沒有意義
                connfd,addr = self.sockfd.accept()
                print('Connect form',addr,'\n')
            except KeyboardInterrupt: #ctrl + c 退出
                self.socket.close()
                sys.exit('服務器退出')
            except Exception:
                #打印出錯誤訊息
                traceback.print_exc()
                continue
            #創建新的線程處理請求
            clientThread = Thread(target = self.handleRequest,args = (connfd,))
            clientThread.setDaemon(True)
            clientThread.start()





      #新增一個線程函數,處理客戶端瀏覽器請求
    def handleRequest(self,connfd):
        #接收瀏覽器請求
        request = connfd.recv(4096)
        #按行切割
        request_lines = request.splitlines()
        #request_lines[0] 索引0 就是請求行 [b'GET / HTTP/1.1']
        #print(connfd.getpeername(),':',request_lines[0])
        
        #獲取請求行
        request_line = request_lines[0].decode()
        #從請求行提取請求方法和請求內容
        #利用正則表達式,提取出來,請求行內容 GET / HTTP/1.1
        #匹配 GET /內容
        # (?P<>) 將子組取名,\s 取空字符 \S* 非空字符 取兩個子組一個為請求方法(METHOD) 一個為請求內容(PATH)
        # 如果輸入的是 127.0.0.1/abc.html <<< 則會有 GET /abc.html HTTP/1.1  GET 為請求方法 abc.html為請求內容
        pattern = r'(?P<METHOD>[A-Z]+)\s+(?P<PATH>/\S*)'
        
        #利用try 防止萬一匹配不到
        try:
            # 利用match 方法匹配 groupdict 以捕獲組的子組內容為值返回一個字典,取第一個匹配的對象
            # env等於請求方法和請求內容
            env = re.match(pattern,request_line).groupdict()
        except:
            #匹配不出來的時候回發瀏覽器錯誤 500
            response_headlers = 'HTTP/1.1 500 Server Error\r\n'
            response_headlers += '\r\n'
            response_body = 'Server Error'
            response = response_headlers + response_body
            connfd.send(response.encode())
            return 
        print(env) # 返回一個字典{'METHOD': 'GET', 'PATH': '/abc.html'}
        
        #必須要再把env的這個返回內容傳到框架 WebFrame 來做處理
        #此函數是將env獲得的請求內容和請求方法發送給框架 WebFrame ,且接收WebFrame 反饋的數據
        #取字典內的值作為參數傳過去
        #需要一個響應碼,響應體返回值,需要status(響應碼),response_body(數據) 這兩個返回值,
        #當請求內容和請求方法發送給後端框架WebFrame 需要上面兩個變數接收 框架WebFrame 反饋的數據
        # GET /favicon.ico/ 為一個網頁小圖標 這是由瀏覽器發起的請求(開啟網頁時的左上角小標誌)
        status,response_body = self.send_request(env['METHOD'],env['PATH']) 

        #根據組織碼響應反應客戶端內容,傳入參數status響應碼,response_hearlers 接收響應碼組織結果
        #根據響應碼組織響應頭內容
        response_headlers = self.get_headlers(status)
        
        #將結果組織為http response 發送給瀏覽器
        response = response_headlers + response_body
        connfd.send(response.encode())
        
        #關閉線程連接
        connfd.close()
        
        
    #此函數是連接框架WebFrame傳送請求方法和內容,且接收反饋(和框架WeFrame 交互獲取request 獲取 response)
    def send_request(self,method,path):
        #發送請求訊息(method,path)給view.py 
        #1.創建套接字,連接 view的服務端
        sockfd2 = socket()
        #2.連接WeFrame 設定的地址,在Httpserver的setting設置參數中加入
        #  WeFrame的服務端地址 
        sockfd2.connect(frame_addr)
        sockfd2.send(method.encode())
        
        #防止傳送數據產生沾包
        #利用sleep()
        
        time.sleep(0.1)
        sockfd2.send(path.encode())
        
        #接收應用程序接收發回來的結果,接收 WeFrame框架傳回的訊息
        status = sockfd2.recv(128).decode()
        
        #接收的如果是大網頁可以利用while True 來接收,因為一次接收 4096是不全的
        response_body = sockfd2.recv(4096 * 10).decode()
        
        
        #測試返回值
        return status,response_body
    
        
        

    #此函數為組織響應碼,處理響應碼
    def get_headlers(self,status):
        #遇到什麼樣的響應碼就給組織怎麼樣的響應頭
        if status == '200':
            response_headlers = 'HTTP/1.1 200 ok\r\n'
            response_headlers += '\r\n'
        elif status =='404':
            response_headlers = 'HTTP/1.1 400 Not Found\r\n'
            response_headlers += '\r\n'
        
        #最終要把響應頭反應回去
        return response_headlers

#啟動器
if __name__ == '__main__':
    #將settings.py配置導入近來 ADDR 的配置訊息,
    #將來如果要更改地址或是端口直接修改settings,不必修改到主檔案
    #通過類生成對象(傳入參數ADDR)
    httpd = HTTPServer(ADDR)
    #通過對象調用server_forver() 啟動服務器
    httpd.server_forever()




























































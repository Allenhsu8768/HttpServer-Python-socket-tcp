# httpserver3.0 項目結構設計
#  項目結構:
#               |----1.httpserver --
#               |                   |-1.1 HttpServer.py(主程序:所有的功能處理都是在這個程序來寫)
#               |                   |-1.2 setting(httpserver配置:)
#               |
#               |
#   project ----|               
#               |
#               |
#               |----2.WebFrame --
#                                |--2.1 static(存放靜態網頁,不光是存放靜態網頁,(css、js、png )都在這裡面存)
#                                |--2.2 views.py(應用處理程序:處理httpserver發來的請求)
#                                |--2.3 urls.py(存放路由:能處理什麼樣的內容)
#                                |--2.4 settings(框架配置)
#                                |--2.5 WebFrame.py(主程序代碼:通過代碼具體執行功能,其他功能都是用來調用)


# 注意事項
# * 為了降低耦合性要把每個部分分模塊來寫
# * 實際上程序只有 HttpServer.py 和 WebFrame.py 其他功能只是輔助調用

# httpserver3.0 新增功能
#    功能:
#       httpserver:
#            獲取http請求
#            解析http請求
#            將請求發送給webFrame
#               從webFrame接收反饋數據
#                   將數據組織為Reponse格式發送給客戶端

#       webFrame:
#             從httpserver接收具體請求
#             根據請求進行邏輯處理和數據處理
#                  * 靜態頁面
#                  * 邏輯數據
#             將需要的數據反饋給httpserver

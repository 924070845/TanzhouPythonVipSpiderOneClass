'''
测试转码第一步
'''

from urllib import request

url = 'http://httpbin.org/post'  # 要加上http://

resp = request.urlopen(url, data='hello word'.encode())
# 只要加上data，就会转为POST请求，还要.encode()转码

# 通过read读取到的数据是bytes类型的，要看原文，就要decode解码，默认UTF-8
print(resp.read().decode())

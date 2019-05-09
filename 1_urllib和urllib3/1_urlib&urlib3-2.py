'''
伪造请求头，get方式
'''

from urllib import request

url = 'http://httpbin.org/get'  # 要加上http://
headers = {
	#以字典的形式伪造请求头
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"
}
req = request.Request(url,headers=headers)
resp = request.urlopen(req)
# 只要加上data，就会转为POST请求，还要.encode()转码

# 通过read读取到的数据是bytes类型的，要看原文，就要decode解码，默认UTF-8
print(resp.read().decode())

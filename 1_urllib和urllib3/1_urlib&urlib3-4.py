'''
添加Cookies
'''

from http import cookiejar
from urllib import request


url = 'http://httpbin.org/cookies'
# 创建一个cookiejar对象，在http模块里面
cookie = cookiejar.CookieJar()
# 使用HTTPCookieProcessor创建cookie处理器
cookies = request.HTTPCookieProcessor(cookie)
# 并以它为参数创建Opener对象
opener = request.build_opener(cookies)
# 使用这个opener来发起请求
resp = opener.open(url)
print(resp.read().decode())


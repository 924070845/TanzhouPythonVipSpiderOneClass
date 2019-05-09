'''
代理proxy
'''

from urllib import request


url = 'http://httpbin.org/ip'

proxy = {
	#键值对的形式，http和https都写上，端口要写对应的
	'http':'50.233.137.33:80',
	'https':'50.233.137.33:80'
}

# 创建代理处理器
proxies = request.ProxyHandler(proxy)
# 创建opener对象
opener = request.build_opener(proxies)
resp = opener.open(url)
print(resp.read().decode())


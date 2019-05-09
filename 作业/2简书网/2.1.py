"""
__author__ = 'Ding'
__time__ = '2018/11/13'
This code is far away from bugs with the god animal protecting
I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛ ┻━━━┛ ┻┓
            ┃━━━━☃━━━━┃
            ┃  ┳┛   ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓       ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓ ┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
import re

'''
使用request库爬取简书网文章标题和简介
'''
import requests
class JianShu():
	def __init__(self):
		self.url = 'https://www.jianshu.com/'
		self.headers = {  # 请求头
			"user-agent":"Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"
		}

	def get_page_data(self):
		response = requests.get(url=self.url, headers=self.headers)
		if response.status_code == 200:  # 返回一个状态码，判断请求的状态
			print("请求成功")
			return response.text
		else:
			print("请求失败")
			return None

	def parse(self, html):
		title = re.findall(r' <a class="title" target="_blank" href=".*?">(.*?)</a>', html)
		text = re.findall(r'<p class="abstract">(.*?)</p>', html, re.S)  # re.S是忽略换行的意思
		text = [i.strip() for i in text]  # 将字符串开头和结束位置的特殊字符去掉，括号中未指定参数就是所有特殊字符都删除
		fp = open('data.txt', 'a', encoding='utf-8')
		for title, text in list(zip(title, text)):
			fp.write(title + text)
			print(title)
			print(text)
		fp.close()

	def run(self):
		html = self.get_page_data()
		self.parse(html)

if __name__ == '__main__':
	jianshu = JianShu()
	jianshu.run()



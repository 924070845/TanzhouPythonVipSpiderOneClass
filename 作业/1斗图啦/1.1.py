#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = '92407'
__time__ = '2018/11/12'
This code is far away from bugs with the god animal protecting
I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛ ┻━━━┛ ┻┓
            ┃      ☃      ┃
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
from urllib import request
import re

class DouTuLa():
	def __init__(self):
		self.url ='https://www.doutula.com/'
		self.header = {  # 请求头
			"User-Agent":" Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"
		}

	def get_image(self):
		custom_request = request.Request(self.url, headers=self.header)
		response = request.urlopen(custom_request)
		html = response.read().decode()
		image_list = re.findall(r'data-original="(.*?)".*?alt="(.*?)"', html)
		# 加括号是表示将找到的值保留下来，显示在元里面，空格也是数据，不能随意增加或删除
		# 中间原来的有一部分也是时有时无的，所以也将其直接换成.*?
		return image_list

	def image_download(self, image_list):
		for url, title in image_list:  # python拆包的基本操作，将列表中的1号元素给了url，二号元素给了title
			title = title + '.' +url.split('.')[-1]
			# 给图片加上图片该有的后缀，不然还是显示不了
			# 以点号为切分，取出最后一组，切割后的字符串没有点，手动加点
			url = re.sub(r'!dta', '', url)
			title = re.sub(r'[？?，,（）！!]', '', title)
			# 字符串的替换，第一个是需要替换的，第二个参数是备替换的，第三个是替换对象
			# 写在方括号里面的，是元字符的操作方式，就是一个一个读，不会认为里面是一个整体的
			# request.urlretrieve(url, title)  # 将文件写入当前路径
			print(url, title)

	def run(self):
		image_list = self.get_image()  # 在执行本类中的方法时。加上self
		self.image_download(image_list)

if __name__ == '__main__':
	doutula = DouTuLa()  # type: DouTuLa
	doutula.run( )

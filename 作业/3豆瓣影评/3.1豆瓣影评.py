#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'Ding'
__time__ = '2018/11/17'   
              ///////////////////////////////////////////////////
              //                    _ooOoo_                    //
              //                   o8888888o                   //
              //                   88" . "88                   //
              //                   (| -_- |)                   //
              //                   O\  =  /O                   //
              //                ____/`---'\____                //  
              //              .'  \\|     |//  `.              //
              //             /  \\|||  :  |||//  \             //
              //            /  _||||| -:- |||||-  \            //
              //            |   | \\\  -  /// |   |            //
              //            | \_|  ''\---/''  |   |            //
              //            \  .-\__  `-`  ___/-. /            //
              //          ___`. .'  /--.--\  `. . __           //
              //       ."" '<  `.___\_<|>_/___.'  >'"".        //
              //      | | :  `- \`.;`\ _ /`;.`/ - ` : | |      //
              //      \  \ `-.   \_ __\ /__ _/   .-` /  /      //
              // ======`-.____`-.___\_____/___.-`____.-'====== //
              //                    `=---='                    //
              //                佛祖保佑  永无BUG                //
              ///////////////////////////////////////////////////
"""
import re
from lxml import etree
import requests


class DouBan():

	# 初始化函数
	def __init__(self):
		self.url = "https://movie.douban.com/review/best/"
		self.header = {  # 请求头
			"user-agent": "Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"
		}
		self.movie_data = []

	# 得到页面数据
	def get_page_data(self, url):
		response = requests.get(url=url, headers=self.header)
		if response.status_code == 200:  # 返回一个状态码，判断请求状态
			# print("请求成功")
			return response.text
		else:
			print("请求失败")
			return None


	# 解析返回的HTML页面
	def parse_page(self, html):
		page = etree.HTML(html)

		movies_list = page.xpath('//div[@class="review-list chart "]/div')
		for movie in movies_list:
			title = movie.xpath('.//a[@class="subject-img"]/img/@title')[0]
			author = movie.xpath('.//a[@class="name"]/text()')[0]
			content = movie.xpath('string(.//div[@class="short-content"])')
			content = re.search(r' .*?[.]{3豆瓣影评}', content).group().strip()
			content = "\t" + content

			# 定义一个字典，存放当前临时的数据
			data = {
				'title' : title,
				'content' : content
			}

			if data in movies_list:
				continue  # 如果刚拿到的数据已经在movies_list里面的话，就跳过本次循环
			else:  # 否则将数据添加到列表中
				self.movie_data.append(data)


			print("电影：{}".format(title), "\t\t", "影评人：{}".format(author), "\n", "影评：\n{}".format(content), end='\n\n')

	# 执行函数汇总
	def run(self, number):
		for page in range(0, number):
			url = self.url + "?start={}".format(page*20)
			html = self.get_page_data(url)
			self.parse_page(html)


if __name__ == '__main__':
	douban = DouBan()
	douban.run(1)

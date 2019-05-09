#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'Ding'
__time__ = '2018/12/13'   
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
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import re
import requests
from PIL import Image  # python用于图像处理的库
from io import BytesIO  # IO流对象
from selenium.webdriver import ActionChains
import time


class Bilibili():

	def __init__(self):
		chrome_options = Options()  # 实例化一个启动参数对象
		chrome_options.add_argument('--disable-infobars')  # 添加启动参数
		self.driver = webdriver.Chrome(chrome_options=chrome_options)
		self.driver.maximize_window()  # 将窗口最大化
		self.wait = WebDriverWait(self.driver, 5)  # 设置最长等待时间

	# 自动登录
	def login(self):
		self.driver.get('https://passport.bilibili.com/login')
		username = self.driver.find_element_by_id('login-username')
		password = self.driver.find_element_by_id('login-passwd')
		username.send_keys('15534399695')
		password.send_keys('fd987987')

	# 得到验证码
	def get_captcha(self):
		# 缺口图片的列表
		with_gap_image_list = self.wait.until(EC.presence_of_all_elements_located((
			By.XPATH, '//div[@class="gt_cut_bg gt_show"]/div'
		)))
		# 拼接成一张带缺口的完整的图片
		with_gap_image = self.splice_image(with_gap_image_list)
		# 完整图片的列表
		intact_image_list = self.wait.until(EC.presence_of_all_elements_located((
			By.XPATH, '//div[@class="gt_cut_fullbg gt_show"]/div'
		)))
		# 拼接成没有缺口的完整图片
		intact_image = self.splice_image(intact_image_list)
		return (with_gap_image, intact_image)  # 将两张图片返回

	# 拼接图片
	def splice_image(self, image):
		image_url = re.search(r'url\("(.*?)"\)', image[0].get_attribute('style')).group(1)
		# 这里image获取的图片都是一样的，所以下标是几都无所谓
		# 获取到style的属性，变化的数据都用.*?代替，斜杠是转义，括号是取出
		'''
		search方法是可以分组的，在正则中，一个括号表示一个组，
		(0)是所以的
		(1)是第一个括号中的内容
		(2)是第二个括号中的内容
		'''
		# 得到url后，使用requests库向地址发起一个请求，就可以下图片了
		img_content = requests.get(image_url).content  # content方法是获取到原始的二进制的数据

		# print(image[0].get_attribute('style'))
		# 获取到所有小块的位置信息
		image_position_list = [i.get_attribute('style') for i in image]
		# 在非所有字符（*就是所有字符）中，？的意思是匹配前面一个元素，0次或1次
		image_position_list = [re.search(r'position: -(.*?)px -?(.*?)px', i).groups() for i in image_position_list]
		# print(image_position_list)

		old_image = Image.open(BytesIO(img_content))  # 代替图片二进制文件与硬盘直接交互。放在的位置是内存中，通过.show()方法将图片打开
		new_image = Image.new('RGB', (260, 116))  # 生成新的彩色图片，大小为260*116

		count_up = 0    # 将新图片放到上半部分的变量
		count_down = 0  # 将新图片放到下半部分的变量
		# 上半部分
		for i in image_position_list[:26]:
			x = int(i[0])
			y = int(i[1])
			croped = old_image.crop((x, y, x + 10, y + 58))  # crop切割图片，其中的数值是图片的左顶右底的坐标
			new_image.paste(croped, (count_up, 0))
			count_up += 10

		# 下半部分
		for i in image_position_list[26:]:
			x = int(i[0])
			y = int(i[1])
			croped = old_image.crop((x, y, x + 10, y + 58))  # crop切割图片，其中的数值是图片的左顶右底的坐标
			new_image.paste(croped, (count_down, 58))
			count_down += 10
		return new_image

	# 获得缺块图片（这里用不到）
	def gap_image(self):
		# 缺口图片
		gap_image = self.wait.until(EC.presence_of_element_located((
			By.XPATH, '//div[@class="gt_slice gt_show"]'
		)))
		gap_image_url = re.search(r'url\("(.*?)"\)', gap_image.get_attribute('style')).group(1)
		# 得到url后，使用requests库向地址发起一个请求，就可以下图片了
		gap_image_content = requests.get(gap_image_url).content  # content方法是获取到原始的二进制的数据
		gap_image = Image.open(BytesIO(gap_image_content))
		gap_image.show()
		# print(gap_image)
		return gap_image

	# 获得缺口偏移量
	def get_gap_offset(self, with_gap_image, intact_image):
		"""
		获取缺口偏移量
		:param nogap_image: 不带缺口图片
		:param gap_image: 带缺口图片
		:return: left 返回的是缺口距离左边的水平位置
		"""

		# 比较两个像素是否相同
		# 由于是RGB格式，所以需要分别判断每个像素点中的R，G，B值
		# 设置阈值的目的是为了忽略掉假的干扰快
		def is_pixel_equal(pixel1, pixel2, threshold=50):
			for i in range(3):  # RGB三色通道都要比较
				if abs(pixel1[i] - pixel2[i] < threshold):  # 因为不知道哪个值大，所以加上绝对值
					return True
			return False  # 误差过大，表示不相等

		width, height = intact_image.size
		left = 60
		for i in range(left, width):
			for j in range(height):
				# 获取两张图片相同坐标的像素点进行比较
				nogap_pixel = intact_image.getpixel((i, j))
				gap_pixle = with_gap_image.getpixel((i, j))

				# 如果像素不同，返回当前像素的x坐标
				if not is_pixel_equal(nogap_pixel, gap_pixle):
					left = i
					return left
		return left

	# 拖动小滑块
	def slide_button(self, distance):
		button = self.wait.until(EC.presence_of_element_located((
			By.XPATH, '//div[@class="gt_slider_knob gt_show"]'
		)))  # 找到拖动的点

		ActionChains(self.driver).click_and_hold(button).perform()  # 点击并按住
		time.sleep(0.5)
		ActionChains(self.driver).move_by_offset(xoffset=distance - 20, yoffset=0).perform()  # 水平拖动distance的长度
		time.sleep(0.5)
		ActionChains(self.driver).release().perform()  # 释放鼠标

	# 执行函数

	# 伪造执行轨迹
	def get_tracks(self):
		pass

	def run(self):
		self.login()
		with_gap_image, intact_image = self.get_captcha()
		distance = self.get_gap_offset(intact_image, with_gap_image)
		print(distance)
		self.slide_button(distance)


if __name__ == '__main__':
	bilibili = Bilibili()
	bilibili.run()

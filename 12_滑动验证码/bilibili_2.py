import re
import time
from io import BytesIO
import requests
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import random

'''
滑动验证码实战，伪造的滑动轨迹需要时常修改才能免疫 极验 机器学习的训练
'''


class BiliBili:
	def __init__(self):
		self.options = self._set_option()
		self.options.add_argument('--disable-infobars')  # 添加启动参数
		self.driver = webdriver.Chrome(chrome_options=self.options)
		self.driver.maximize_window()
		self.wait = WebDriverWait(self.driver, 10)

	# 设置启动选项
	def _set_option(self):
		options = Options()
		options.add_argument("--window-size=1366,768")
		# options.add_argument("--headless")
		# options.add_argument("--disable-gpu")
		return options

	# 输入账号密码
	def login(self):
		try:
			self.driver.get(r'https://passport.bilibili.com/login')
			user_name = self.driver.find_element(By.XPATH, '//div[@class="input-box"]//li/input')
			user_name.send_keys('15534399695')
			password = self.driver.find_element(By.CSS_SELECTOR, '.input-box li:nth-child(2) > input')
			password.send_keys('fd987987')
		except Exception as e:
			print('进入登陆页面出错：%s' % e)
			self.driver.quit()

	# 获得验证码图片
	def get_captcha(self):
		try:
			# 获得有缺口图片
			gap_image = self.wait.until(EC.presence_of_all_elements_located((
				By.XPATH, '//div[@class="gt_cut_bg gt_show"]/div'
			)))
			gap_image = self._splice_image(gap_image)  # 拼接成完整图片

			# 获得无缺口图片
			nogap_image = self.wait.until(EC.presence_of_all_elements_located((
				By.XPATH, '//div[@class="gt_cut_fullbg gt_show"]/div'
			)))
			nogap_image = self._splice_image(nogap_image)  # 拼接成完整图片

			# 返回拼接好的图片
			return (nogap_image, gap_image)
		except Exception as e:
			print('获取图片出错: %s' % (e))
			self.driver.quit()

	# 将获取的图片重新裁剪拼接为一张完整的图片
	def _splice_image(self, image):
		# 用正则获取元素中的图片url链接
		image_url = re.search(r'url\("(.*?)"\);', image[0].get_attribute('style')).group(1)
		# 这里image获取的图片都是一样的，所以下标是几都无所谓
		# 获取到style的属性，变化的数据都用.*?代替，斜杠是转义，括号是取出
		'''
		search方法是可以分组的，在正则中，一个括号表示一个组，
		(0)是所以的
		(1)是第一个括号中的内容
		(2)是第二个括号中的内容
		'''
		# 得到url后，使用requests库向地址发起一个请求，就可以下图片了
		# 获取列表中每张小图的位置偏移信息
		image_position_list = [i.get_attribute('style') for i in image]
		image_position_list = [re.search(r'position: -(.*?)px -?(.*?)px;', i).groups() for i in image_position_list]
		# 在非所有字符（*就是所有字符）中，？的意思是匹配前面一个元素，0次或1次
		# 访问图片链接，获取图片的二进制数据
		img = requests.get(image_url).content
		# PIL要从二进制数据读取一个图片的话，需要把其转化为BytesIO
		# 代替图片二进制文件与硬盘直接交互。放在的位置是内存中，通过.show()方法将图片打开
		img = Image.open(BytesIO(img))
		# 生成一个新的相同大小的空白图片、彩色图片，大小为260*116
		new_img = Image.new('RGB', (260, 116))

		# 设置一个粘贴坐标，坐标每次循环加10，则从左到右依次粘贴
		count_up = 0
		count_low = 0
		# 图片主要分为上下两个部分，所以分成两个循环分别粘贴
		# image_list前26个为上半部分，后26个为下半部分
		# 每个小图片大小为10，58
		for i in image_position_list[:26]:
			croped = img.crop((int(i[0]), 58, int(i[0]) + 10, 116))  # crop切割图片，其中的数值是图片的左顶右底的坐标
			new_img.paste(croped, (count_up, 0))  # 将切割刀的图片贴到新的图片中
			count_up += 10

		for i in image_position_list[26:]:
			croped = img.crop((int(i[0]), 0, int(i[0]) + 10, 58))
			new_img.paste(croped, (count_low, 58))
			count_low += 10

		return new_img

	# 获取缺口偏移量
	def get_gap_offset(self, nogap_image, gap_image):
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

		width, height = nogap_image.size
		left = 60
		for i in range(left, width):
			for j in range(height):
				# 获取两张图片相同坐标的像素点进行比较
				nogap_pixel = nogap_image.getpixel((i, j))
				gap_pixle = gap_image.getpixel((i, j))

				# 如果像素不同，返回当前像素的x坐标
				if not is_pixel_equal(nogap_pixel, gap_pixle):
					left = i
					return left
		return left

	# 生成滑动轨迹
	def get_tracks(self, distance):
		'''
		由于极验的后台在不断的训练识别模型，所以移动轨迹可能是有实效性的，时常需要修改
		轨迹要尽量的靠近人类的行为习惯
		:param distance: 滑块与缺口的距离
		:return:move_track_list 伪造的移动轨迹列表
		'''
		'''
		来源于物理学中的加速度算距离公式和速度公式：
		s = vt + 1/2 at^2
		v = v_0 + at
		总距离S= 每一次移动的距离之和
		加速度：前3/5S加速度2，后半部分加速度是-3
		'''
		speed = 0  # 初速度
		t = 0.2  # 计算移动距离所需的时间间隔
		mid = distance * 4 / 5  # 减速阈值（改变加速度的时间点）
		current = 0  # 当前位移
		move_track_list = []  # 移动轨迹的列表

		# 方案一
		while current < distance:
			if current < mid:
				a = 3  # 加速度为3
				move_distance = speed * t + 0.5 * a * (t ** 2)  # 距离的计算公式  v0t + 1/2 * a * t^2
				move_track_list.append(round(move_distance))  # 将生成的移动距离添加到轨迹列表中
				speed += (a * t)  # 当前速度v = v0 + at
				current += move_distance  # 当前位移
			else:
				move_track_list.extend([3, 2, 2, 2, 1, 1])  # 当距离大于五分之三的position时，添加减速轨迹，并跳出循环
				break

		# 方案二
		'''
		while current < distance:
			if current < mid:
				a = 2
			else:
				a = -3
			# 移动距离 （距离的计算公式  v0t + 1/2 * a * t^2）
			move_distance = speed * t + 0.5 * a * t * t
			# 将生成的移动距离添加到轨迹列表中
			move_track_list.append(round(move_distance))
			# 当前的速度v = v0 + at
			speed += (a * t)

			# 当前总位移
			current += move_distance
		'''

		# 识别当前总共移动距离是大于还是小于position
		# 大于则补连续的-1，小于则补连续的1
		offset = sum(move_track_list) - distance
		if offset > 0:
			move_track_list.extend([-1 for i in range(offset)])
		elif offset < 0:
			move_track_list.extend([1 for i in range(abs(offset))])

		# 小幅晃动模拟人在终点附近的左右移动
		move_track_list.extend(
			[0, 0, 0, 0, 0, 0, -3, -1, -2, -1, -1, 0, 0, 0, 0, 0, 1, 2, 1])
		return move_track_list

	# 滑动滑块
	def slide_button(self, tracks):
		slide_button = self.wait.until(EC.visibility_of_element_located((
			By.XPATH, '//div[@id="gc-box"]//div[@class="gt_slider"]/div[2]'
		)))
		ActionChains(self.driver).click_and_hold(slide_button).perform()  # 点击并拿起滑块
		# 根据我们生成的移动轨迹，逐步移动鼠标
		for i in tracks:
			ActionChains(self.driver).move_by_offset(xoffset=i, yoffset=0).perform()
		time.sleep(1)
		ActionChains(self.driver).release().perform()  # 松开鼠标

	# 控制整体运行逻辑
	def __call__(self):
		try:
			# 1登陆，输入账号密码
			self.login()
			# 2获得两张验证码图片
			capture_image = self.get_captcha()
			# 3对比两种图片的像素点，找出位移
			distance = self.get_gap_offset(capture_image[0], capture_image[1])
			# 4模拟人的行为习惯，根据总位移得到行为轨迹
			tracks = self.get_tracks(distance)
			# 5滑动滑块
			self.slide_button(tracks)
		finally:
			time.sleep(5)
			self.driver.quit()


if __name__ == '__main__':
	bilbil = BiliBili()
	bilbil()

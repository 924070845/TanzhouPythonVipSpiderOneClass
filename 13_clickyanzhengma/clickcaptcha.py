import time
from io import BytesIO
from clickyanzhengma.chaojiying import Chaojiying_Client
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ClickCaptcha(object):
	def __init__(self, username, password):
		self.username = username
		self.password = password
		self.options = self.get_options()
		self.driver = webdriver.Chrome(chrome_options=self.options)
		self.wait = WebDriverWait(self.driver, 5)
		self.driver.maximize_window()  # 将窗口最大化


	def get_options(self):
		"""设置启动项"""
		options = Options()
		options.add_argument('--window-size=1366,768')
		# options.add_argument("--headless")
		# options.add_argument("--disable-gpu")
		return options

	def start(self):
		self.driver.get('http://dun.163.com/trial/picture-click')
		# 滚动进度条到显示出验证码
		self.driver.execute_script('window.scrollTo(0, 300)')

	def get_captcha_image(self):
		"""获得验证码图片"""
		# 找到左边点击验证弹出验证码
		click_button = self.wait.until(EC.element_to_be_clickable((
			By.XPATH,
			'//div[@class="tcapt_item is-left"]//div[@class="yidun_tips"]'
		)))
		# 将鼠标移动到按钮上
		ActionChains(self.driver).move_to_element(click_button).perform()
		# 获取验证码图片元素
		image = self.wait.until(EC.visibility_of_element_located((
			By.XPATH, '//div[@class="tcapt_item is-left"]//div[@class="yidun_bgimg"]/img[1]'
		)))
		# 获取x, y坐标
		x, y = image.location.values()
		# 获取整个窗口截图，获得图片二进制数据
		window_screen = self.driver.get_screenshot_as_png()
		window_screen = Image.open(BytesIO(window_screen))

		# 图片位置是相对于没有移动滚动条的，要减去滚动的300
		captcha_image = window_screen.crop((x, y - 300, x + 310, y - 80))

		# captcha_image.show()
		# captcha_image为一个img对象，超级鹰需要的是图片的二进制数据
		# 可以先保存到文件，在读出来。也可以通过bytesIO来做
		captcha = BytesIO()
		# save可以把图片保存到文件，也可以保存到bytesIO对象中去
		# format指定保存格式
		captcha_image.save(captcha, format("png"))
		# 获取bytesIO对象中的二进制数据
		return captcha.getvalue()


	def post_image_and_get_position(self, captcha, image_category, id='897357'):
		"""提交图片到超级鹰识别图片返回点击坐标"""
		cjy = Chaojiying_Client(self.username, self.password, id)

		# 返回的是json格式的字典，pic_str里面返回了图片的坐标
		position = cjy.PostPic(captcha, image_category).get('pic_str')
		position_list = [i.split(',') for i in position.split('|')]
		return position_list


	def click_captcha(self, position):
		"""点击验证码图片"""
		# 找到验证码图片的位置
		image = self.wait.until(EC.visibility_of_element_located((
			By.XPATH, '//div[@class="tcapt_item is-left"]//div[@class="yidun_bgimg"]/img[1]'
		)))
		last_position = None  # 记录上一个单词的坐标
		for word_list in position:  # 循环点击
			# 第一次点击
			if not last_position:
				# 鼠标移动过去在点击
				ActionChains(self.driver).move_to_element_with_offset(
					image, int(word_list[0]), int(word_list[1])
				).click().perform()
			else:
				track_list = self._get_track_list(last_position, word_list)  # 获得移动轨迹
				# 循环移动
				for j in track_list:
					ActionChains(self.driver).move_to_element_with_offset(
						image, int(j[0]), int(j[1])
					).perform()
				# 移动到该字处后，点击
				ActionChains(self.driver).click().perform()

			last_position = word_list  # 保留上一个字的坐标，计算下一个字位移的时候使用
			time.sleep(1)


	def _get_track_list(self, last_position, next_position):
		"""获得移动的轨迹列表"""
		# 轨迹列表
		position_list = []
		# 移动距离
		x = (int(next_position[0]) - int(last_position[0])) / 20  # 匀速移动20次
		y = (int(next_position[1]) - int(last_position[1])) / 20
		# 循环移动
		for i in range(1, 21):
			# x*i+last_postion(0)，round求整
			position = [round(x * i) + int(last_position[0]), round(y * i) + int(last_position[1])]
			position_list.append(position)
		return position_list


	def run(self, image_category):
		try:
			self.start()
			while True:
				caption = self.get_captcha_image()
				position = self.post_image_and_get_position(caption, image_category)
				self.click_captcha(position)
				try:
					successful = self.wait.until(EC.text_to_be_present_in_element(
						(By.XPATH, '//div[@class="tcapt_item is-left"]'
								   '//span[@class="yidun_tips__text"]'), '验证成功'
					))
					break  # 识别成功，跳出循环
				except Exception:
					continue  # 验证失败，继续截图，发送图片，验证
		except Exception as e:
			print(e)
		finally:
			print('识别成功!')
			self.driver.quit()


if __name__ == '__main__':
	click = ClickCaptcha('924070845', 'fd987987')
	click.run('9103')

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'Ding'
__time__ = '2019/1/6'   
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
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
import time
from clickyanzhengma.chaojiying import Chaojiying_Client


# 点触验证吗
class ClickCaptcha:
	def __init__(self, username, password, software_id, selective_type):
		self.options = self._set_option()
		self.options.add_argument('--disable-infobars')  # 添加启动参数
		self.driver = webdriver.Chrome(chrome_options=self.options)
		self.driver.maximize_window()  # 将窗口最大化
		self.wait = WebDriverWait(self.driver, 10)#最长等待10秒
		self.username = username  # 账号
		self.password = password  # 密码
		self.software_id = software_id  # 软件id
		self.selective_type = selective_type  # 选择类型

	# 设置启动选项
	def _set_option(self):
		options = Options()
		options.add_argument("--window-size=1366,768")
		return options

	# 开始
	def statr(self):
		'''
		页面的截图从主页面的左上顶点开始计数
		不算浏览器的窗口头
		就算窗口被动的向下拖动了，原点还是最开始的绝对的左上的点
		:return:
		'''
		self.driver.get('http://dun.163.com/trial/picture-click')  # 得到url的页面
		self.driver.execute_script('window.scrollTo(0, 300)')  # 操作js来拖动滚动条，0是左右，300是上下
		click_buttom = self.wait.until(EC.element_to_be_clickable((
			By.XPATH, "//div[@class='yidun_tips']"
		)))  # 判断元素能否点击0

		ActionChains(self.driver).move_to_element(click_buttom).perform()  # 鼠标滑入
		time.sleep(2)
		# 找到图片, 判断图片有没有加载出来
		image = self.wait.until(EC.visibility_of_element_located((
			By.XPATH, '/html/body/main/div/div/div[2]/div[2]/div[2]/div/div[2]/div[3]/div/div/div[1]/div/div[1]'
		)))
		x, y = image.location.values()
		print(image.location)
		windows_screen = self.driver.get_screenshot_as_png()  # 获得页面图片的二进制数据
		windows_screen = Image.open(BytesIO(windows_screen))  # 将这个二进制图片打开
		captcha_image = windows_screen.crop((x, y , x + 320, y + 220))  # 初始的时候，页面自动给滚动了一部分，在这里吗自动滚动的部分减掉
		# windows_screen.show()
		captcha_image.show()
		'''
		localtion方法返回对象的坐标，以字典的形式{x : '1', y : '2'}
		values()返回的是字典的值
		'''
		captcha = BytesIO()  # 获取到二进制流中的图片数据
		captcha_image.save(captcha, format('png'))  # 将二进制保存为png格式的文件，并返回
		return captcha.getvalue() # 返回就可以提交给超级鹰了

	# self.driver.get_screenshot_as_file('test1.png')  # 截图并保存为test1.png

	# 提交图片
	def post_image_and_get_position(self, img):
		chaojiying = Chaojiying_Client(self.username, self.password, self.software_id)
		# im = open('a.jpg', 'rb').read()  # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
		position = chaojiying.PostPic(img, self.selective_type)['pic_str']#返回需要的字的坐标
		print('position:{}'.format(position))
		position_list = [i.split(',') for i in position.split('|')]
		print('position_list:{}'.format(position_list))
		return position_list

	# 1902 验证码类型  官方网站>>价格体系
	def run(self):
		self.statr()
		img = self.statr()  # 接受将要操作的图片
		self.post_image_and_get_position(img)


if __name__ == '__main__':
	clickCaptcha = ClickCaptcha('924070845', 'fd987987', '898335', 9103)
	clickCaptcha.run()

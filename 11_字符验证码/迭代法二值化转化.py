#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'Ding'
__time__ = '2018/12/12'   
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
from PIL import Image


# 最优的就是这个迭代法
def iterGetThreshold(img, pixdata, width, height):
	pixPrs = pixBac = []  # 用于统计前景和背景平均阈值
	threshold = 0
	pixel_min, pixel_max = img.getextrema()  # 获得图片中最大和最小灰度值
	newThreshold = int((pixel_min + pixel_max) / 2)  # 初始阈值

	while True:
		if abs(threshold - newThreshold) < 5:  # 差值小于5,退出
			break
		for y in range(height):
			for x in range(width):
				if pixdata[x, y] >= newThreshold:
					pixBac.append(pixdata[x, y])  # 大于阈值 为背景
				else:
					pixPrs.append(pixdata[x, y])  # 小于， 前景

		avgPrs = sum(pixPrs) / len(pixPrs)
		avgBac = sum(pixBac) / len(pixBac)
		threshold = newThreshold
		newThreshold = int((avgPrs + avgBac) / 2)

	return newThreshold


def binary(img, threshold=None):
	img = img.convert('L')  # 转为灰度图
	pixdata = img.load()
	width, height = img.size

	if not threshold:
		# threshold = sum(img.getdata()) / (width * height)  # 通过平均值给阈值
		threshold = iterGetThreshold(img, pixdata, width, height)  # 通过迭代法求阈值
	# 遍历所有像素，大于阈值的为白色
	# pass
	for y in range(height):
		for x in range(width):
			if pixdata[x, y] < threshold:
				pixdata[x, y] = 0
			else:
				pixdata[x, y] = 255

	return img


img = Image.open('test5.jpg')
img = binary(img)
img = binary(img, 127)
img.show()

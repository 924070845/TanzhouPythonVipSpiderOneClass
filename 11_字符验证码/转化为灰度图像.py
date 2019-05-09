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


def binary(img, threshold=None):
	img = img.convert('L')  # 转为灰度图
	pixdata = img.load()
	width, height = img.size

	if not threshold:
		threshold = sum(img.getdata()) / (width * height)  # 通过平均值给阈值
	# threshold = iterGetThreshold(img, pixdata,width, height)
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
# img = binary(img, 127)
img.show()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'Ding'
__time__ = '2018/11/20'   
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
from Cryptodome import Random
from Cryptodome.Cipher import AES
from binascii import b2a_hex


class MyAES:
	def __init__(self, key):
		self.key = self.cheak_key(key).encode()
		self.iv = Random.new().read(AES.block_size)  # 生成一个随机的，符合iv长度的偏移量
		self.mode = AES.MODE_CFB

	# 判断我们传进来的key 的长度是否符合规定：16或24或32
	def cheak_key(self, key):
		if len(key) in [16, 34, 32]:  # 看所比较的对象是否在列表里面
			return key
		else:
			raise Exception('key 的长度不符合规定')

	# 加密
	def encrypt(self, data):
		cipher = AES.new(self.key, self.mode, self.iv)
		return cipher.encrypt(data.encode())

	# 解密
	def decrypt(self, data):
		cipher = AES.new(self.key, self.mode, self.iv)
		return cipher.decrypt(data)


if __name__ == '__main__':
	myase = MyAES('1234567812345678')
	text = myase.encrypt('测试加密数据')
	# 测试加密
	print(b2a_hex(text))
	# 测试解密
	print(myase.decrypt(text).decode())

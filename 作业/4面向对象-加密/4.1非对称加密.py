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
from binascii import b2a_hex
import rsa


class MyRSA:
	def __init__(self, rsa_n, rsa_e):
		self.rsa_n = int(rsa_n, 16)
		self.rsa_e = int(rsa_e, 16)
		self.publicKey = rsa.PublicKey(self.rsa_n, self.rsa_e)

	def encrypt(self, data):
		return rsa.encrypt(data, self.publicKey)

	def decrypt(self):
		pass


if __name__ == '__main__':
	text = "这是测试用例"
	# 从网页请求中获取
	pubkey_n = '8d7e6949d411ce14d7d233d7160f5b2cc753930caba4d5ad24f923a505253b9c39b09a059732250e56c594d735077cfcb0c3508e9f544f101bdf7e97fe1b0d97f273468264b8b24caaa2a90cd9708a417c51cf8ba35444d37c514a0490441a773ccb121034f29748763c6c4f76eb0303559c57071fd89234d140c8bb965f9725'
	pubkey_e = '1024'
	myrsa = MyRSA(pubkey_n, pubkey_e)

	print(b2a_hex(myrsa.encrypt(text.encode())))

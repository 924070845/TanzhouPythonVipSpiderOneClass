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

publicKey, privateKey = rsa.newkeys(256)  # 生成了一对公私钥
text = "这是测试数据"
print("测试数据：{}".format(text))

# 公钥加密
enrypto_text = rsa.encrypt(text.encode(), publicKey)
print("公钥加密，加密后：{}".format(b2a_hex(enrypto_text)))

# 私有解密
decrypto_text = rsa.decrypt(enrypto_text, privateKey)
print("私钥解，解密后：{}".format(decrypto_text.decode()))

'''
只能公钥加密，私钥解密
'''

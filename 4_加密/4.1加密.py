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

# 导入DES模块
from Cryptodome.Cipher import DES, DES3
import binascii

# 这是密钥，必须是8的位数位，des是8位，des3是16或24位才行
key = b'abcdefghqqqqqqqqwwwwwwww'
# 需要去生成一个DES对象
des = DES3.new(key, DES.MODE_ECB)

# 需要加密的数据，必须是8的位数倍
text = 'python spider!'
text = text + (8 - (len(text) % 8)) * '='
print("原数据是：" + text)


# 加密的过程
encrypto_text = des.encrypt(text.encode())
print("初步加密后是：{}".format(encrypto_text))
print("去掉斜杠之后是：{}".format(binascii.b2a_hex(encrypto_text)))
# 解密的过程
decrypt_text = des.decrypt(encrypto_text)
print("解密之后是：{}".format(decrypt_text))

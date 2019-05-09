#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'Ding'
__time__ = '2018/12/5'   
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
import time

from selenium.webdriver.chrome.options import Options
# 实例化一个启动参数对象
chrome_options = Options()
# 添加启动参数
chrome_options.add_argument('--window-size=1200,880')
# 将参数对象传入Chrome，则启动了一个设置了窗口大小的Chrome
borwser = webdriver.Chrome(chrome_options=chrome_options)



# borwser = webdriver.Chrome()
borwser.get('http://www.w3school.com.cn/tiy/t.asp?f=jseg_prompt')
time.sleep(1)

borwser.switch_to.frame('i')
borwser.find_element_by_xpath('//input').click()  # 点击定位到的按钮

time.sleep(3)
alert = borwser.switch_to.alert  # 得到弹窗对象
alert.send_keys("HelloWorld")  # 为输入框输入值

time.sleep(3)
alert.accept()

time.sleep(3)
borwser.close()



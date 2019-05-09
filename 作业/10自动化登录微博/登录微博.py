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
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# 实例化一个启动参数对象
chrome_options = Options()
# 添加启动参数
chrome_options.add_argument('--window-size=1080,927')
chrome_options.add_argument('--disable-infobars')
# 将参数对象传入Chrome，则启动了一个设置了窗口大小的Chrome
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get('https://weibo.com/')

username = WebDriverWait(browser, 5, 0.1).until(EC.presence_of_element_located((By.ID, 'loginname')))
username.send_keys("15534399695")

password = WebDriverWait(browser, 5, 0.1).until(EC.presence_of_element_located((By.NAME, 'password')))
password.send_keys('fd987987')
time.sleep(4)

browser.find_element_by_xpath('//div[@class="info_list login_btn"]/a').click()

time.sleep(5)
browser.close()

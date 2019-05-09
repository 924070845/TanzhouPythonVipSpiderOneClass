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
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time


# 实例化一个启动参数对象
chrome_options = Options()
# 添加启动参数
chrome_options.add_argument('--window-size=1080,927')
chrome_options.add_argument('--disable-infobars')
# 将参数对象传入Chrome，则启动了一个设置了窗口大小的Chrome
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get('https://www.imooc.com/')

# time.sleep(3)

browser.find_element_by_xpath('//a[@id="js-signin-btn"]').click()

web = WebDriverWait(browser, 5, 0.1)
email = web .until(EC.presence_of_element_located((By.NAME,'email')))
email.send_keys("15534399695")

password = web .until(EC.presence_of_element_located((By.NAME,'password')))
password.send_keys("fd987987")

browser = web .until(EC.presence_of_element_located((By.XPATH, '//*[@id="signup-form"]/div[5]/input')))
browser.click()

print("执行完毕")


time.sleep(3)
browser.close()
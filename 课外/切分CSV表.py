#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'Ding'
__time__ = '2019/5/5'   
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

import csv
import os

# path = '/Users/mac/Desktop/186_3.csv'
path = ''

with open(path, 'r', newline='') as file:
	csvreader = csv.reader(file)
	a = next(csvreader)
	print(a)
	i = j = 1
	for row in csvreader:
		print(row)
		print(f'i is {i}, j is {j}')
		# 没1000个就j加1， 然后就有一个新的文件名
		if i % 1000 == 0:
			j += 1
			print(f"csv {j} 生成成功")
		csv_path = os.path.join('/'.join(path.split('/')[:-1]), '186_3/' + str(j) + '.csv')
		# print('/'.join(path.split('/')[:-1]))
		print(csv_path)
		# 不存在此文件的时候，就创建
		if not os.path.exists(csv_path):
			with open(csv_path, 'w', newline='') as file:
				csvwriter = csv.writer(file)
				csvwriter.writerow(['image_url'])
				csvwriter.writerow(row)
			i += 1
		# 存在的时候就往里面添加
		else:
			with open(csv_path, 'a', newline='') as file:
				csvwriter = csv.writer(file)
				csvwriter.writerow(row)
			i += 1
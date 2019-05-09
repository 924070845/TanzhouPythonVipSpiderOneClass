#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'Ding'
__time__ = '2019/5/6'   
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


# coding=utf-8
def createC1(dataSet):  # 构建所有1项候选项集的集合
	C1 = []
	for transaction in dataSet:
		for item in transaction:
			if [item] not in C1:
				C1.append([item])  # C1添加的是列表，对于每一项进行添加，[[1], [2], [3], [4], [5]]
	# print('C1:',C1)
	return list(map(frozenset, C1))  # 使用frozenset，被“冰冻”的集合，为后续建立字典key-value使用。


###由候选项集生成符合最小支持度的项集L。参数分别为数据集、候选项集列表，最小支持度
###如
###C3: [frozenset({1, 2, 3}), frozenset({1, 3, 5}), frozenset({2, 3, 5})]
###L3: [frozenset({2, 3, 5})]
def scanD(D, Ck, minSupport):
	ssCnt = {}
	for tid in D:  # 对于数据集里的每一条记录
		for can in Ck:  # 每个候选项集can
			if can.issubset(tid):  # 若是候选集can是作为记录的子集，那么其值+1,对其计数
				if not ssCnt.__contains__(can):  # ssCnt[can] = ssCnt.get(can,0)+1一句可破，没有的时候为0,加上1,有的时候用get取出，加1
					ssCnt[can] = 1
				else:
					ssCnt[can] += 1
	numItems = float(len(D))
	retList = []
	supportData = {}
	for key in ssCnt:
		support = ssCnt[key] / numItems  # 除以总的记录条数，即为其支持度
		if support >= minSupport:
			retList.insert(0, key)  # 超过最小支持度的项集，将其记录下来。
			supportData[key] = support
	return retList, supportData


###由Lk生成K项候选集Ck
###如由L2: [frozenset({3, 5}), frozenset({2, 5}), frozenset({2, 3}), frozenset({1, 3})]
###生成
###C3: [frozenset({1, 2, 3}), frozenset({1, 3, 5}), frozenset({2, 3, 5})]
def aprioriGen(Lk, k):
	retList = []
	lenLk = len(Lk)
	for i in range(lenLk):
		for j in range(i + 1, lenLk):
			if len(Lk[i] | Lk[j]) == k:
				retList.append(Lk[i] | Lk[j])
	return list(set(retList))


####生成所有频繁子集
def apriori(dataSet, minSupport=0.5):
	C1 = createC1(dataSet)
	D = list(map(set, dataSet))
	L1, supportData = scanD(D, C1, minSupport)
	L = [L1]  # L将包含满足最小支持度，即经过筛选的所有频繁n项集，这里添加频繁1项集
	k = 2
	while (len(L[k - 2]) > 0):  # k=2开始，由频繁1项集生成频繁2项集，直到下一个打的项集为空
		Ck = aprioriGen(L[k - 2], k)
		Lk, supK = scanD(D, Ck, minSupport)
		supportData.update(supK)  # supportData为字典，存放每个项集的支持度，并以更新的方式加入新的supK
		L.append(Lk)
		k += 1
	return L, supportData


if __name__ == "__main__":
	dataSet = [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]
	D = list(map(set, dataSet))
	L, suppData = apriori(dataSet)
	print('L:', L,'\n')
	print('suppData:', suppData,'\n')

	'''
	C1 = createC1(dataSet)
	L1, supportData1 = scanD(D, C1, 0.5)
	print('C1:',C1)
	print('L1:',L1)
	print('supportData1:',supportData1)
	C2 = aprioriGen(L1, 2)
	L2, supportData2 = scanD(D, C2, 0.5)
	print('C2:',C2)
	print('L2:',L2)
	print('supportData2:',supportData2)
	C3 = aprioriGen(L2, 3)
	L3, supportData3 = scanD(D, C3, 0.5)
	print('C3:',C3)
	print('L3:',L3)
	print('supportData3:',supportData3)
	'''
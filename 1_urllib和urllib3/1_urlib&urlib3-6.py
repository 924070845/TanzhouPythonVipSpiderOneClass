#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = '92407'
__time__ = '2018/11/12'
This code is far away from bugs with the god animal protecting
I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛ ┻━━━┛ ┻┓
            ┃      ☃      ┃
            ┃  ┳┛   ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓       ┏━┛
                ┃      ┗━━━┓
                ┃   神兽保佑   ┣┓
                ┃　 永无BUG！  ┏┛
                ┗┓┓┏━┳┓ ┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
'''
urllib.parse
urllib.parse是urllib中用来解析各种数据格式的模块。
'''
from urllib import parse

keyword = '南北'
parsees = parse.quote(keyword)  #url转码，转成get请求能认识的代码
print(parsees)

params = {'wd': keyword, 'code': '1_urllib和urllib3', 'height': '188'}
print(parse.urlencode(params))
#字典是无序的，即使你的汉字写在最前面，但是在解码时，汉字还是要给数字和英文让位子
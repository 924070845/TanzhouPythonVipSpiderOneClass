#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'Ding'
__time__ = '2018/11/13'
This code is far away from bugs with the god animal protecting
I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛ ┻━━━┛ ┻┓
            ┃      ☃      ┃
            ┃  ┳┛   ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓       ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓ ┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
import requests


url = 'https://api.github.com/'
params = {'key1': 'value1', 'key2': ['value2', 'value3']}
headers = {'user-agent': 'my-app/0.0.1斗图啦'}
resp = requests.get(url, headers=headers)
print(resp.text)

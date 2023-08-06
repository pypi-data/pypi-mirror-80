#! /usr/bin/env python
__author__ = 'Tser'
__email__ = '807447312@qq.com'
__project__ = 'xiaobaiauto2'
__script__ = 'client.py'
__create_time__ = '2020/9/18 13:50'

from typing import DefaultDict
from requests import request
from jmespath import search

class Request(object):
    global vent
    def __init__(self,
                 method: str = 'POST',
                 baseUrl: str = '',
                 vent: dict = dict(),
                 test: dict = {'json': {'data.code': 200}, 're': {'"<code>\d+</code>"': 200}},
                 order: int = 0
                 ):
        self.vent = vent
        self.method = method
        self.baseUrl = baseUrl
        self.verify = verify
        self.test = test
        self.order = order

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            print('run api =>', func.__name__)
            # res = request(
            #     method=self.method,
            #     url=self.baseUrl + func.path,
            #     data=func.data,
            #     headers=func.headers,
            #     verify=self.verify
            # )
            # print(func)  # 通过方法名获取参数
            # print(kwargs)
            print(f'接口地址：{self.baseUrl + kwargs["path"]}')
            print('运行接口')
            print('接口判断')
            # res = request()
            # if self.test.get('json'):
            #     assert search(self.test['json'].keys[0], res.json()) == search(self.test['json'].values[0]
            # elif self.test.get('re'):
            #     assert search(self.test['json'].keys[0], res.json()) == search(self.test['json'].values[0]
            print('返回响应值')
        return wrapper

@Request(baseUrl='https://baidu.com')
def baidu_search_api(**kwargs):
    pass


baidu_search_api(path='/api')
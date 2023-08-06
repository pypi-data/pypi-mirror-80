# coding=utf-8
# /usr/bin/env/ python

"""
Author: AlibabaCloudRPA
Email:
Create time: 2020-04-26 10:42
IDE: PyCharm
desc: 
"""


class Request:

    def __init__(self, path):
        self._path = path
        self._method = "GET"

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, value):
        self._method = value

    @property
    def path(self):
        return self._path

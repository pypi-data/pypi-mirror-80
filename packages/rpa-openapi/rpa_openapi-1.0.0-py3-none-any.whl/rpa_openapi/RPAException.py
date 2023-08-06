# coding=utf-8
# /usr/bin/env/ python

"""
Author: AlibabaCloudRPA
Email:
Create time: 2020-04-27 19:51
IDE: PyCharm
desc: 
"""


class RPAException(Exception):

    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return "<RPAException>: {}".format(self.msg)

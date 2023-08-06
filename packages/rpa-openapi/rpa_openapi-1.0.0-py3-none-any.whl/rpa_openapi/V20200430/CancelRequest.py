# coding=utf-8
# /usr/bin/env/ python

"""
Author: AlibabaCloudRPA
Email:
Create time: 2020-04-26 19:54
IDE: PyCharm
desc: 
"""
from rpa_openapi.V20200430.Request import Request
from rpa_openapi.V20200430.path import CANCEL_PATH
from rpa_openapi.RPAException import RPAException


class CancelRequest(Request):
    """
    创建服务型任务
    """

    def __init__(self):
        super().__init__(CANCEL_PATH)
        self.__apply_id = None
        self.method = "POST"

    def __repr__(self) -> str:
        return "<CancelRequest>: apply_id={}".format(self.__apply_id)

    @property
    def apply_id(self) -> str:
        return self.__apply_id

    @apply_id.setter
    def apply_id(self, value: str) -> None:
        """
        param: value: applyId,申请记录唯一标识符
        """
        self.__apply_id = value

    @property
    def params(self) -> dict:
        d = {}
        if self.__apply_id:
            d["applyId"] = self.__apply_id
        else:
            raise RPAException("applyId参数不能为空")
        return d

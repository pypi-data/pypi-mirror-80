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
from rpa_openapi.V20200430.path import REJECT_PATH
from rpa_openapi.RPAException import RPAException


class RejectRequest(Request):
    """
    创建服务型任务
    """

    def __init__(self):
        super().__init__(REJECT_PATH)
        self.__apply_id = None
        self.__message = None
        self.method = "POST"

    def __repr__(self) -> str:
        return "<RejectRequest>: apply_id={}, message={}".format(self.__apply_id, self.__message)

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
    def message(self) -> str:
        return self.__message

    @message.setter
    def message(self, value: str) -> None:
        """
        param: value: applyId,申请记录唯一标识符
        """
        self.__message = value

    @property
    def params(self) -> dict:
        d = {}
        if self.__apply_id:
            d["applyId"] = self.__apply_id
        else:
            raise RPAException("applyId参数不能为空")
        if self.__message:
            d["message"] = self.__message
        else:
            raise RPAException("message参数不能为空")
        return d

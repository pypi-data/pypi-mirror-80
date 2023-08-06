# coding=utf-8
# /usr/bin/env/ python

"""
Author: AlibabaCloudRPA
Email:
Create time: 2020-04-26 19:38
IDE: PyCharm
desc: 
"""
from rpa_openapi.V20200430.Request import Request
from rpa_openapi.V20200430.path import UPDATE_CLIENT_INFO_PATH
from rpa_openapi.RPAException import RPAException


class UpdateClientInfoRequest(Request):
    """
    更新客户端信息
    """

    def __init__(self):
        super().__init__(UPDATE_CLIENT_INFO_PATH)
        self.__client_id = None
        self.__name = None
        self.method = "POST"

    def __repr__(self) -> str:
        return "<UpdateClientInfoRequest>: client_id={}, name={}".format(self.__client_id, self.__name)

    @property
    def client_id(self) -> str:
        return self.__client_id

    @client_id.setter
    def client_id(self, value: str) -> None:
        """
        param: value: applyId,申请记录唯一标识符
        """
        self.__client_id = value

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        """
        param: value: applyId,申请记录唯一标识符
        """
        self.__name = value

    @property
    def params(self) -> dict:
        d = {}
        if self.__client_id:
            d["clientId"] = self.__client_id
        else:
            raise RPAException("applyId参数不能为空")
        if self.__name:
            d["name"] = self.__name
        else:
            raise RPAException("name参数不能为空")
        return d

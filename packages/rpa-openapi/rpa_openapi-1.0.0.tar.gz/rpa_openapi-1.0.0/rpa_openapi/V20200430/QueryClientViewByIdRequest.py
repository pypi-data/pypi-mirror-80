# coding=utf-8
# /usr/bin/env/ python

"""
Author: AlibabaCloudRPA
Email:
Create time: 2020-04-26 19:48
IDE: PyCharm
desc: 
"""
from rpa_openapi.V20200430.Request import Request
from rpa_openapi.V20200430.path import QUERY_CLIENT_VIEW_BY_ID_PATH
from rpa_openapi.RPAException import RPAException


class QueryClientViewByIdRequest(Request):
    """
    查询客户端信息
    """

    def __init__(self):
        super().__init__(QUERY_CLIENT_VIEW_BY_ID_PATH)
        self.__client_id = None

    def __repr__(self) -> str:
        return "<QueryClientViewByIdRequest>: client_id={}".format(self.__client_id)

    @property
    def client_id(self) -> str:
        return self.__client_id

    @client_id.setter
    def client_id(self, value: str) -> None:
        """
        param: value: clientId,机器人唯一识别符
        """
        self.__client_id = value

    @property
    def params(self) -> dict:
        d = {}
        if self.__client_id:
            d["clientId"] = self.__client_id
        else:
            raise RPAException("appId参数不可为空")
        return d

# coding=utf-8
# /usr/bin/env/ python

"""
Author: AlibabaCloudRPA
Email:
Create time: 2020-04-26 19:55
IDE: PyCharm
desc: 
"""
from rpa_openapi.V20200430.Request import Request
from rpa_openapi.V20200430.path import QUERY_APP_APPLY_PATH
from rpa_openapi.RPAException import RPAException


class QueryAppApplyRequest(Request):
    """
    根据appId参数申请记录
    """

    def __init__(self):
        super().__init__(QUERY_APP_APPLY_PATH)
        self.__app_id = None

    def __repr__(self) -> str:
        return "<QueryRequest>: app_id={}".format(self.__app_id)

    @property
    def app_id(self) -> str:
        return self.__app_id

    @app_id.setter
    def app_id(self, value: str) -> None:
        """
        param: value: appId,应用唯一识别符
        """
        self.__app_id = value

    @property
    def params(self) -> dict:
        d = {}
        if self.__app_id:
            d["appId"] = self.__app_id
        else:
            raise RPAException("appId参数不可为空")
        return d

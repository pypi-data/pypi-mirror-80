# coding=utf-8
# /usr/bin/env/ python

"""
Author: AlibabaCloudRPA
Email:
Create time: 2020-04-26 19:52
IDE: PyCharm
desc: 
"""
from rpa_openapi.V20200430.BaseQueryRequest import BaseQueryRequest
from rpa_openapi.V20200430.path import QUERY_APPS_PATH


class QueryAPPSRequest(BaseQueryRequest):
    """
    获取应用列表
    """

    def __init__(self):
        super().__init__(QUERY_APPS_PATH)
        self.__app_name = None

    def __repr__(self) -> str:
        return "<QueryAPPSRequest>: app_name={}, current_page={}, page_size={}".format(self.__app_name, self.current_page, self.page_size)

    @property
    def app_name(self) -> str:
        return self.__app_name

    @app_name.setter
    def app_name(self, value: str) -> None:
        """
        param: value: app名称,非必选参数
        """
        self.__app_name = value

    @property
    def params(self) -> dict:
        d = {}
        if self.__app_name:
            d["appName"] = self.__app_name
        if self.current_page:
            d["currentPage"] = str(self.current_page)
        if self.page_size:
            d["pageSize"] = str(self.page_size)
        return d

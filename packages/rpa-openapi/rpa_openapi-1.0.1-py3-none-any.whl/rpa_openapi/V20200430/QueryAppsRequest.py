# coding=utf-8
# /usr/bin/env/ python

"""
Author: AlibabaCloudRPA
Email:
Create time: 2020-04-26 19:52
IDE: PyCharm
desc: 
"""
from rpa_openapi.Enums import AppMarketStatus, FromType
from rpa_openapi.V20200430.BaseQueryRequest import BaseQueryRequest
from rpa_openapi.V20200430.path import QUERY_APPS_PATH


class QueryAPPSRequest(BaseQueryRequest):
    """
    获取应用列表
    """

    def __init__(self):
        super().__init__(QUERY_APPS_PATH)
        self.__app_name = None
        self.__app_market_status = None
        self.__app_market_source = None

    def __repr__(self) -> str:
        return "<QueryAPPSRequest>: app_name={}, current_page={}, page_size={}".format(self.__app_name, self.current_page, self.page_size)

    @property
    def app_name(self) -> str:
        return self.__app_name

    @app_name.setter
    def app_name(self, value: str) -> None:
        """
        :param value: 应用名称,非必选参数
        """
        self.__app_name = value

    @property
    def app_market_status(self) -> str:
        return self.__app_market_status

    @app_market_status.setter
    def app_market_status(self, value: AppMarketStatus) -> None:
        """
        :param value: 应用在市场的状态
        """
        self.__app_market_status = value

    @property
    def app_market_source(self) -> str:
        return self.__app_market_source

    @app_market_source.setter
    def app_market_source(self, value: FromType) -> None:
        """
        :param value: 应用来源
        """
        self.__app_market_source = value

    @property
    def params(self) -> dict:
        d = {}
        if self.__app_name:
            d["appName"] = self.__app_name
        if self.__app_market_status:
            d["appMarketStatus"] = self.__app_market_status.value
        if self.__app_market_source:
            d["appMarketSource"] = self.__app_market_source.value
        if self.current_page:
            d["currentPage"] = str(self.current_page)
        if self.page_size:
            d["pageSize"] = str(self.page_size)
        return d

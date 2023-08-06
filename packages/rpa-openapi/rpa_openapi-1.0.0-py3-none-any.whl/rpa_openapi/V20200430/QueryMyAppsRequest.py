# coding=utf-8
# /usr/bin/env/ python

"""
Author: AlibabaCloudRPA
Email:
Create time: 2020-04-26 19:53
IDE: PyCharm
desc: 
"""
from rpa_openapi.V20200430.BaseQueryRequest import BaseQueryRequest
from rpa_openapi.V20200430.path import QUERY_MY_APPS_PATH


class QueryMyAppsRequest(BaseQueryRequest):
    """
    获取用户已获取的应用列表
    """

    def __init__(self):
        super().__init__(QUERY_MY_APPS_PATH)
        self.__name = None

    def __repr__(self) -> str:
        return "<QueryMyAppsRequest>: name={}, current_page={}, page_size={}".format(self.__name, self.current_page,
                                                                                     self.page_size)

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: name) -> None:
        """
        param: value: app名称,非必选参数
        """
        self.__name = value

    @property
    def params(self) -> dict:
        d = {}
        if self.__name:
            d["name"] = self.__name
        if self.current_page:
            d["currentPage"] = str(self.current_page)
        if self.page_size:
            d["pageSize"] = str(self.page_size)
        return d

# coding=utf-8
# /usr/bin/env/ python

"""
Author: AlibabaCloudRPA
Email:
Create time: 2020-04-26 10:41
IDE: PyCharm
desc: 
"""
from rpa_openapi.V20200430.BaseQueryRequest import BaseQueryRequest
from rpa_openapi.V20200430.path import QUERY_CLIENT_VIEWS_PATH


class QueryClientViewsRequest(BaseQueryRequest):
    """
    查询客户端信息
    """

    def __init__(self):
        super().__init__(QUERY_CLIENT_VIEWS_PATH)
        self.__client_name = None

    def __repr__(self) -> str:
        return "<QueryClientViewsRequest>: client_name={}, current_page={}, page_size={}".format(self.__client_name,
                                                                                                 self.current_page,
                                                                                                 self.page_size)

    @property
    def client_name(self) -> str:
        return self.__client_name

    @client_name.setter
    def client_name(self, value: str) -> None:
        """
        param: value: 客户端名称
        """
        self.__client_name = value

    @property
    def params(self) -> dict:
        d = {}
        if self.__client_name:
            d["clientName"] = self.__client_name
        if self.current_page:
            d["currentPage"] = str(self.current_page)
        if self.page_size:
            d["pageSize"] = str(self.page_size)
        return d

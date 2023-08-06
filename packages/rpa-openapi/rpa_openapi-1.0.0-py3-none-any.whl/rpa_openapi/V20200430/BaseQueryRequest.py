# coding=utf-8
# /usr/bin/env/ python

"""
Author: AlibabaCloudRPA
Email:
Create time: 2020-05-11 10:52
IDE: PyCharm
desc: 
"""
from rpa_openapi.V20200430.Request import Request


class BaseQueryRequest(Request):

    def __init__(self, path):
        super().__init__(path)
        self.__current_page = None
        self.__page_size = None

    @property
    def current_page(self) -> str:
        return self.__current_page

    @current_page.setter
    def current_page(self, value: int) -> None:
        """
        param: value: 当前页数
        """
        self.__current_page = value

    @property
    def page_size(self) -> int:
        return self.__page_size

    @page_size.setter
    def page_size(self, value: int) -> None:
        self.__page_size = value


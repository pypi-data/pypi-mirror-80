# coding=utf-8
# /usr/bin/env/ python

"""
Author: AlibabaCloudRPA
Email:
Create time: 2020-04-26 19:49
IDE: PyCharm
desc: 
"""
from rpa_openapi.V20200430.BaseQueryRequest import BaseQueryRequest
from rpa_openapi.V20200430.path import QUERY_MEMBER_CLIENT_VIEWS_PATH
from rpa_openapi.Enums import ConnectStatus, ClientType, DispatchMode


class QueryMemberClientViewsRequest(BaseQueryRequest):
    """
    查询用户登录的客户端列表
    """

    def __init__(self):
        super().__init__(QUERY_MEMBER_CLIENT_VIEWS_PATH)
        self.__key = None
        self.__client_type = None
        self.__status = None
        self.__connect_status = None
        self.__dispatch_mode = None

    def __repr__(self) -> str:
        return "<QueryMemberClientViewsRequest>: key={}, client_type={}, status={}, connect_status={}, " \
               "dispatch_mode={}, current_page={}, page_size={}" \
            .format(self.__key,
                    self.__client_type,
                    self.__status,
                    self.__connect_status,
                    self.__dispatch_mode,
                    self.current_page,
                    self.page_size)

    @property
    def key(self) -> str:
        return self.__key

    @key.setter
    def key(self, value: str) -> None:
        """
        param: value: key: 客户端名字or ip的模糊查询
        """
        self.__key = value

    @property
    def client_type(self) -> ClientType:
        return self.__client_type

    @client_type.setter
    def client_type(self, value: ClientType) -> None:
        """
        param: value: client_type
        """
        self.__client_type = value

    @property
    def status(self) -> str:
        return self.__status

    @status.setter
    def status(self, value: str) -> None:
        """
        param: value: status
        """
        self.__status = value

    @property
    def connect_status(self) -> ConnectStatus:
        return self.__connect_status

    @connect_status.setter
    def connect_status(self, value: ConnectStatus) -> None:
        """
        param: value: connect_status
        """
        self.__connect_status = value

    @property
    def dispatch_mode(self) -> DispatchMode:
        return self.__dispatch_mode

    @dispatch_mode.setter
    def dispatch_mode(self, value: DispatchMode) -> None:
        """
        param: value: dispatch_mode
        """
        self.__dispatch_mode = value

    @property
    def params(self) -> dict:
        d = {}
        if self.__key:
            d["key"] = self.__key
        if self.__client_type:
            d["clientType"] = self.__client_type.value
        if self.__status:
            d["status"] = self.__status
        if self.__connect_status:
            d["connectStatus"] = self.__connect_status.value
        if self.__dispatch_mode:
            d["dispatchMode"] = self.__dispatch_mode.value
        if self.current_page:
            d["currentPage"] = str(self.current_page)
        if self.page_size:
            d["pageSize"] = str(self.page_size)
        return d

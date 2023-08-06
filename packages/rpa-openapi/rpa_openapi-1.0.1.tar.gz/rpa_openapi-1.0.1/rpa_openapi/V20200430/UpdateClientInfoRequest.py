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
        self.__ip = None
        self.__mac_address = None
        self.method = "POST"

    def __repr__(self) -> str:
        return "<UpdateClientInfoRequest>: client_id={}, name={}".format(self.__client_id, self.__name)

    @property
    def client_id(self) -> str:
        return self.__client_id

    @client_id.setter
    def client_id(self, value: str) -> None:
        """
        :param value: clientId 客户端唯一标识符
        """
        self.__client_id = value

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        """
        :param value: name 客户端名称
        """
        self.__name = value

    @property
    def ip(self) -> str:
        return self.__ip

    @ip.setter
    def ip(self, value: str) -> None:
        """
        :param value: ip 客户端IP
        """
        self.__ip = value

    @property
    def mac_address(self) -> str:
        return self.__mac_address

    @mac_address.setter
    def mac_address(self, value: str) -> None:
        """
        :param value: macAddress 客户端Mac地址
        """
        self.__mac_address = value

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
        if self.__ip:
            d["ip"] = self.__ip
        if self.__mac_address:
            d["macAddress"] = self.__mac_address
        return d

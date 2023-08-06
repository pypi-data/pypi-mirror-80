# coding=utf-8
# /usr/bin/env/ python

"""
Author: AlibabaCloudRPA
Email:
Create time: 2020-04-26 19:07
IDE: PyCharm
desc: 
"""
from rpa_openapi.V20200430.Request import Request
from rpa_openapi.V20200430.path import UPDATE_CLIENT_DISPATCH_MODE_PATH
from rpa_openapi.RPAException import RPAException
from rpa_openapi.Enums import ClientDispatchMode


class UpdateClientDispatchModeRequest(Request):
    """
    修改客户端状态
    """

    def __init__(self):
        super().__init__(UPDATE_CLIENT_DISPATCH_MODE_PATH)
        self.__client_id = None
        self.__dispatch_mode = None
        self.method = "POST"

    def __repr__(self) -> str:
        return "<UpdateClientDispatchModeRequest>: client_id={}, dispatch_mode={}".format(self.__client_id, self.__dispatch_mode)

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
    def dispatch_mode(self) -> ClientDispatchMode:
        return self.__dispatch_mode

    @dispatch_mode.setter
    def dispatch_mode(self, value: ClientDispatchMode) -> None:
        """
        param: value: applyId,申请记录唯一标识符
        """
        self.__dispatch_mode = value

    @property
    def params(self) -> dict:
        d = {}
        if self.__client_id:
            d["clientId"] = self.__client_id
        else:
            raise RPAException("applyId参数不能为空")
        if self.__dispatch_mode:
            d["dispatchMode"] = self.__dispatch_mode.value
        else:
            raise RPAException("dispatch_mode参数不能为空")
        return d

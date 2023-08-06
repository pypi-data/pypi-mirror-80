# coding=utf-8
# /usr/bin/env/ python

"""
Author: AlibabaCloudRPA
Email:
Create time: 2020-04-26 17:39
IDE: PyCharm
desc: 
"""
from rpa_openapi.V20200430.Request import Request
from rpa_openapi.V20200430.path import UPDATE_CLIENT_STATUS_PATH
from rpa_openapi.RPAException import RPAException
from rpa_openapi.Enums import ClientStatus


class UpdateClientStatusRequest(Request):
    """
    修改客户端认证状态
    """

    def __init__(self):
        super().__init__(UPDATE_CLIENT_STATUS_PATH)
        self.__client_id = None
        self.__status = None
        self.method = "POST"

    def __repr__(self) -> str:
        return "<UpdateClientStatusRequest>: client_id={}, status={}".format(self.__client_id, self.__status)

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
    def status(self) -> ClientStatus:
        return self.__status

    @status.setter
    def status(self, value: ClientStatus) -> None:
        """
        param: value: applyId,申请记录唯一标识符
        """
        self.__status = value

    @property
    def params(self) -> dict:
        d = {}
        if self.__client_id:
            d["clientId"] = self.__client_id
        else:
            raise RPAException("applyId参数不能为空")
        if self.__status:
            d["status"] = self.__status.value
        else:
            raise RPAException("status参数不能为空")
        return d

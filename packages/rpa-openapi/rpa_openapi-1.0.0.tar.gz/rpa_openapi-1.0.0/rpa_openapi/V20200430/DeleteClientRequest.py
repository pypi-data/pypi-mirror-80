# coding=utf-8
# /usr/bin/env/ python

"""
Author: AlibabaCloudRPA
Email:
Create time: 2020-04-26 19:39
IDE: PyCharm
desc: 
"""
from rpa_openapi.V20200430.Request import Request
from rpa_openapi.V20200430.path import DELETE_CLIENT_PATH
from rpa_openapi.RPAException import RPAException


class DeleteClientRequest(Request):
    """
    删除客户端
    """

    def __init__(self):
        super().__init__(DELETE_CLIENT_PATH)
        self.__client_id = None
        self.__remark = None
        self.method = "POST"

    def __repr__(self) -> str:
        return "<DeleteClientRequest>: client_id={}, status={}".format(self.__client_id, self.__remark)

    @property
    def client_id(self) -> str:
        return self.__client_id

    @client_id.setter
    def client_id(self, value: str) -> None:
        """
        param: value: clientId,机器人唯一标识符
        """
        self.__client_id = value

    @property
    def remark(self) -> str:
        return self.__remark

    @remark.setter
    def remark(self, value: str) -> None:
        """
        param: value: 备注信息
        """
        self.__remark = value

    @property
    def params(self) -> dict:
        d = {}
        if self.__client_id:
            d["clientId"] = self.__client_id
        else:
            raise RPAException("applyId参数不能为空")
        if self.__remark:
            d["remark"] = self.__remark
        else:
            raise RPAException("remark参数不能为空")
        return d

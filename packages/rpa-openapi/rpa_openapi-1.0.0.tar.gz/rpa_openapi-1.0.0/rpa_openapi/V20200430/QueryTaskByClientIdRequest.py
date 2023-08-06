# coding=utf-8
# /usr/bin/env/ python

"""
Author: AlibabaCloudRPA
Email:
Create time: 2020-04-26 19:52
IDE: PyCharm
desc: 
"""
from rpa_openapi.V20200430.Request import Request
from rpa_openapi.V20200430.path import QUERY_TASK_BY_CLIENT_ID_PATH


class QueryTaskByClientIdRequest(Request):
    """
    根绝客户端唯一标识UUID符获取任务
    """

    def __init__(self):
        super().__init__(QUERY_TASK_BY_CLIENT_ID_PATH)
        self.__client_id = None

    def __repr__(self) -> str:
        return "<QueryTaskByClientIdRequest>: client_id={}".format(self.__client_id)

    @property
    def client_id(self) -> str:
        return self.__client_id

    @client_id.setter
    def client_id(self, value: str) -> None:
        """
        param: value: clientId,客户端唯一标识UUID
        """
        self.__client_id = value

    @property
    def params(self) -> dict:
        d = {}
        if self.__client_id:
            d["clientId"] = self.__client_id
        return d

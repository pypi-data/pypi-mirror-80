# coding=utf-8
# /usr/bin/env/ python

"""
Author: AlibabaCloudRPA
Email:
Create time: 2020-04-26 11:14
IDE: PyCharm
desc: 
"""
from rpa_openapi.V20200430.BaseQueryRequest import BaseQueryRequest
from rpa_openapi.V20200430.path import QUERY_TASK_BY_CLIENT_ID_AND_STATUS_PATH


class QueryTaskByClientIdAndStatusRequest(BaseQueryRequest):
    """
    查询指定客户端对应的任务数
    """

    def __init__(self):
        super().__init__(QUERY_TASK_BY_CLIENT_ID_AND_STATUS_PATH)
        self.__client_ids = None
        self.__status = None

    def __repr__(self) -> str:
        return "<QueryTaskByClientIdAndStatusRequest>: client_ids={}, status={}, current_page={}, page_size={}".format(
            self.__client_ids, self.__status, self.current_page, self.page_size)

    @property
    def client_ids(self) -> str:
        return self.__client_ids

    @client_ids.setter
    def client_ids(self, value: list) -> None:
        """
        param: value: clientIds, 客户端UUID
        """
        self.__client_ids = ",".join(value)

    @property
    def status(self) -> str:
        return self.__status

    @status.setter
    def status(self, value: str) -> None:
        """
        param: value: status,客户端运行状态
        """
        self.__status = value

    @property
    def params(self) -> dict:
        d = {}
        if self.__client_ids:
            d["clientIds"] = self.__client_ids
        if self.__status:
            d["status"] = self.__status
        if self.current_page:
            d["currentPage"] = str(self.current_page)
        if self.page_size:
            d["pageSize"] = str(self.page_size)
        return d

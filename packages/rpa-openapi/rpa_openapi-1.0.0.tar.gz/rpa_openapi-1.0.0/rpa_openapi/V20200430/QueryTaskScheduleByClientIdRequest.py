# coding=utf-8
# /usr/bin/env/ python

"""
Author: AlibabaCloudRPA
Email:
Create time: 2020-04-26 19:52
IDE: PyCharm
desc: 
"""
from rpa_openapi.V20200430.BaseQueryRequest import BaseQueryRequest
from rpa_openapi.V20200430.path import QUERY_TASK_SCHEDULE_BY_CLIENT_ID_PATH


class QueryTaskScheduleByClientIdRequest(BaseQueryRequest):
    """
    根据客户端唯一标识符获取计划任务
    """

    def __init__(self):
        super().__init__(QUERY_TASK_SCHEDULE_BY_CLIENT_ID_PATH)
        self.__client_id = None

    def __repr__(self) -> str:
        return "<QueryTaskScheduleByClientIdRequest>: client_id={}, current_page={}, page_size={}".format(self.__client_id, self.current_page, self.page_size)

    @property
    def client_id(self) -> str:
        return self.__client_id

    @client_id.setter
    def client_id(self, value: str) -> None:
        """
        param: value: clientId: 客户端uuid
        """
        self.__client_id = value

    @property
    def params(self) -> dict:
        d = {}
        if self.__client_id:
            d["clientId"] = self.__client_id
        if self.current_page:
            d["currentPage"] = str(self.current_page)
        if self.page_size:
            d["pageSize"] = str(self.page_size)
        return d

# coding=utf-8
# /usr/bin/env/ python

"""
Author: AlibabaCloudRPA
Email:
Create time: 2020-04-26 19:51
IDE: PyCharm
desc: 
"""
from rpa_openapi.V20200430.BaseQueryRequest import BaseQueryRequest
from rpa_openapi.V20200430.path import QUERY_TASK_LOGS_PATH


class QueryTaskLogsRequest(BaseQueryRequest):
    """
    获取任务运行日志
    """

    def __init__(self):
        super().__init__(QUERY_TASK_LOGS_PATH)
        self.__task_id = None

    def __repr__(self) -> str:
        return "<QueryTaskLogsRequest>: task_id={}, current_page={}, page_size={}".format(self.__task_id,
                                                                                          self.current_page,
                                                                                          self.page_size)

    @property
    def task_id(self) -> str:
        return self.__task_id

    @task_id.setter
    def task_id(self, value: str) -> None:
        """
        param: value: taskId,任务UUID
        """
        self.__task_id = value

    @property
    def params(self) -> dict:
        d = {}
        if self.__task_id:
            d["taskId"] = self.__task_id
        if self.current_page:
            d["currentPage"] = str(self.current_page)
        if self.page_size:
            d["pageSize"] = str(self.page_size)
        return d

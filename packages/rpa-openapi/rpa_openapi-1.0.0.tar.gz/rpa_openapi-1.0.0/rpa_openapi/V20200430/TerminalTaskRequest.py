# coding=utf-8
# /usr/bin/env/ python

"""
Author: AlibabaCloudRPA
Email:
Create time: 2020-04-26 19:51
IDE: PyCharm
desc: 
"""
from rpa_openapi.V20200430.Request import Request
from rpa_openapi.V20200430.path import TERMINAL_TASK_PATH


class TerminalTaskRequest(Request):
    """
    根据taskUuid停止任务
    """

    def __init__(self):
        super().__init__(TERMINAL_TASK_PATH)
        self.__task_id = None
        self.method = "POST"

    def __repr__(self) -> str:
        return "<TerminalTaskRequest>: task_id={}".format(self.__task_id)

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
        return d

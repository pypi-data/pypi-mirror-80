# coding=utf-8
# /usr/bin/env/python

"""
Author: AlibabaCloudRPA
Email:
Create time: 2020-05-22 15:07
IDE: PyCharm
desc: 
"""
from rpa_openapi.V20200430.BaseQueryRequest import BaseQueryRequest
from rpa_openapi.V20200430.path import QUERY_TASK_BATCH_BY_TASK_SCHEDULE_ID_PATH


class QueryTaskBatchByTaskScheduleIdRequest(BaseQueryRequest):
    """
    根据taskScheduleId查询任务批次
    """

    def __init__(self):
        super().__init__(QUERY_TASK_BATCH_BY_TASK_SCHEDULE_ID_PATH)
        self.__task_schedule_id = None

    def __repr__(self) -> str:
        return "<QueryTaskBatchByTaskScheduleIdRequest>: task_schedule_id={}, current_page={}, page_size={}".format(
            self.__task_schedule_id, self.current_page, self.page_size)

    @property
    def task_schedule_id(self) -> str:
        return self.__task_schedule_id

    @task_schedule_id.setter
    def task_schedule_id(self, value: str) -> None:
        """
        param: value: taskScheduleId,计划任务唯一标识UUID
        """
        self.__task_schedule_id = value

    @property
    def params(self) -> dict:
        d = {}
        if self.__task_schedule_id:
            d["taskScheduleId"] = self.__task_schedule_id
        if self.current_page:
            d["currentPage"] = str(self.current_page)
        if self.page_size:
            d["pageSize"] = str(self.page_size)
        return d

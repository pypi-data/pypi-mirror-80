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
from rpa_openapi.V20200430.path import QUERY_TASK_SCHEDULES_PATH


class QueryTaskSchedulesRequest(BaseQueryRequest):
    """
    查询计划任务列表
    """

    def __init__(self):
        super().__init__(QUERY_TASK_SCHEDULES_PATH)
        self.task_schedule_name = None
        self.__task_schedule_status = None
        self.__start_time = None
        self.__end_time = None

    def __repr__(self) -> str:
        return "<QueryTaskSchedulesRequest>: task_schedule_name={}".format(
            self.task_schedule_name,
            self.__task_schedule_status,
            self.__start_time,
            self.__end_time,
            self.current_page,
            self.page_size
        )

    @property
    def task_schedule_name(self) -> str:
        return self.task_schedule_name

    @task_schedule_name.setter
    def task_schedule_name(self, value: str) -> None:
        """
        param: value: taskScheduleName: 计划任务名称
        """
        self.task_schedule_name = value

    @property
    def task_schedule_status(self) -> str:
        return self.__task_schedule_status

    @task_schedule_status.setter
    def task_schedule_status(self, value: str) -> None:
        """
        param: value: taskScheduleStatus: 计划任务状态
        """
        self.__task_schedule_status = value

    @property
    def start_time(self) -> str:
        return self.__start_time

    @start_time.setter
    def start_time(self, value: str) -> None:
        """
        param: value: startTime: 计划任务开始时间
        """
        self.__start_time = value

    @property
    def end_time(self) -> str:
        return self.__end_time

    @end_time.setter
    def end_time(self, value: str) -> None:
        """
        param: value: endTime: 计划任务结束时间
        """
        self.__end_time = value

    @property
    def params(self) -> dict:
        d = {}
        if self.task_schedule_name:
            d["taskScheduleName"] = self.task_schedule_name
        if self.__task_schedule_status:
            d["taskScheduleStatus"] = self.__task_schedule_status
        if self.__start_time:
            d["startTime"] = self.__start_time
        if self.__end_time:
            d["endTime"] = self.__end_time
        if self.current_page:
            d["currentPage"] = str(self.current_page)
        if self.page_size:
            d["pageSize"] = str(self.page_size)
        return d

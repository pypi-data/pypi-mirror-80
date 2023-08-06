# coding=utf-8
# /usr/bin/env/ python

"""
Author: AlibabaCloudRPA
Email:
Create time: 2020-04-26 19:49
IDE: PyCharm
desc: 
"""
import json
from json import JSONEncoder
from typing import List
from datetime import date

from rpa_openapi.Enums import SpecifiedValue, ErrorHandling
from rpa_openapi.V20200430.Request import Request
from rpa_openapi.V20200430.path import CREATE_TASK_SCHEDULE_PATH
from rpa_openapi.RPAException import RPAException


class CreateTaskScheduleRequest(Request):
    """
    创建计划任务
    """

    def __init__(self):
        super().__init__(CREATE_TASK_SCHEDULE_PATH)
        self.__app_id = None
        self.__name = None
        self.__client_ids = []
        self.__schedule_type = None
        self.__schedule_config = None
        self.__app_params = None
        self.method = "POST"

    def __repr__(self) -> str:
        return "<CreateTaskScheduleRequest>: " \
               "app_id={}, name={}, client_ids={}, schedule_type={}, schedule_config={}, app_params={}" \
            .format(self.__app_id,
                    self.__name,
                    self.__client_ids,
                    self.__schedule_type,
                    self.__schedule_config,
                    self.__app_params)

    @property
    def app_id(self) -> str:
        return self.__app_id

    @app_id.setter
    def app_id(self, value: str) -> None:
        """
        param: value: appId
        """
        self.__app_id = value

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        """
        param: value: name
        """
        self.__name = value

    @property
    def client_ids(self) -> list:
        return self.__client_ids

    @client_ids.setter
    def client_ids(self, value: list) -> None:
        """
        param: value: robotUuid,机器人UUID
        """
        self.__client_ids = value

    @property
    def schedule_type(self) -> list:
        return self.__schedule_type

    @schedule_type.setter
    def schedule_type(self, value: list) -> None:
        """
        param: value: scheduleType,任务类型
        """
        self.__schedule_type = value

    @property
    def schedule_config(self) -> str:
        return self.__schedule_config

    @schedule_config.setter
    def schedule_config(self, value: dict) -> None:
        """
        param: value: appParams,应用参数
        """
        self.__schedule_config = value

    @property
    def app_params(self) -> str:
        return self.__app_params

    @app_params.setter
    def app_params(self, value: dict) -> None:
        """
        param: value: scheduleConfig,计划任务参数
        """
        self.__app_params = json.dumps(value)

    @property
    def params(self) -> dict:
        d = {}
        if self.__app_id:
            d["appId"] = self.__app_id
        else:
            raise RPAException("appId参数不能为空")
        if self.__name:
            d["name"] = self.__name
        else:
            raise RPAException("name参数不能为空")
        if self.__client_ids:
            d["clientIds"] = ",".join(self.__client_ids)
        else:
            raise RPAException("clientIds参数不能为空")
        if self.__schedule_type:
            d["scheduleType"] = self.__schedule_type.value
        else:
            raise RPAException("scheduleType参数不能为空")
        if self.__schedule_config:
            d["scheduleConfig"] = json.dumps(self.__schedule_config, cls=_JSONEncoder)
        else:
            raise RPAException("scheduleConfig参数不能为空")
        if self.__app_params:
            d["appParams"] = self.__app_params
        return d


class ScheduleConfig:

    def __init__(self, *, year_month_day=None, hour_minute=None, schedule_end_dt=None, specified_value=None,
                 interval_minute=None, interval_hour=None, interval_day=None, weeks=None, month=None,
                 error_handling=None, is_queue_up_type=None, task_number=None, task_priority=None, emails=None,
                 force_radio=True, task_schedule_start_date=None) -> None:
        """
        year_month_day: 指定年月日
        hour_minute: 指定时分
        schedule_end_dt: 强制结束时间；forceRadio为true是，需要有强制结束时间
        specified_value: 间隔值(Enum) ：INTERVAL_MINUTE ,INTERVAL_HOUR ,INTERVAL_DAY
        interval_minute: 间隔分 ，0-59的值
        interval_hour: 间隔时， 0-23的值
        interval_day: 间隔天，0-29的值
        weeks: 1-7的以逗号间隔的字符串组合
        month: 1-31以逗号间隔的字符串组合
        error_handling: 错误处理方式(Enum)：RESUBMIT 重试，TERMINATION 终止；选传
        is_queue_up_type: 是否放入队列；选传
        task_number: 任务数；选传
        task_priority:
        emails: 邮箱参数,多个邮箱时，以逗号间隔
        force_radio: 是否有强制结束时间
        task_schedule_start_date: 计划任务开始时间
        """
        self.__year_month_day = year_month_day
        self.__hour_minute = hour_minute
        self.__schedule_end_dt = schedule_end_dt
        self.__specified_value = specified_value
        self.__interval_minute = interval_minute
        self.__interval_hour = interval_hour
        self.__interval_day = interval_day
        self.__weeks = weeks
        self.__month = month
        self.__error_handling = error_handling
        self.__is_queue_up_type = is_queue_up_type
        self.__task_number = task_number
        self.__task_priority = task_priority
        self.__emails = emails
        self.__force_radio = force_radio
        self.__task_schedule_start_date = task_schedule_start_date

    @property
    def yearMonthDay(self) -> str:
        return self.__year_month_day

    @yearMonthDay.setter
    def yearMonthDay(self, value: str) -> None:
        self.__year_month_day = value

    @property
    def hourMinute(self) -> str:
        return self.__hour_minute

    @hourMinute.setter
    def hourMinute(self, value: str) -> None:
        self.__hour_minute = value

    @property
    def scheduleEndDt(self) -> str:
        return self.__schedule_end_dt

    @scheduleEndDt.setter
    def scheduleEndDt(self, value: str) -> None:
        self.__schedule_end_dt = value

    @property
    def specifiedValue(self) -> SpecifiedValue:
        return self.__specified_value

    @specifiedValue.setter
    def specifiedValue(self, value: SpecifiedValue) -> None:
        self.__specified_value = value

    @property
    def intervalMinute(self) -> int:
        return self.__interval_minute

    @intervalMinute.setter
    def intervalMinute(self, value: int) -> None:
        if value < 0 or value > 59:
            raise ValueError("间隔分的取值范围为：0-59")
        self.__interval_minute = value

    @property
    def intervalHour(self) -> int:
        return self.__interval_hour

    @intervalHour.setter
    def intervalHour(self, value: int) -> None:
        if value < 0 or value > 23:
            raise ValueError("间隔时的取值范围为：0-23")
        self.__interval_hour = value

    @property
    def intervalDay(self) -> int:
        return self.__interval_day

    @intervalDay.setter
    def intervalDay(self, value: int) -> None:
        if value < 0 or value > 29:
            raise ValueError("间隔天的取值范围为：0-29")
        self.__interval_day = value

    @property
    def weeks(self) -> str:
        return self.__weeks

    @weeks.setter
    def weeks(self, value:  List[int]) -> None:
        temp_value = [str(i) for i in value]
        self.__month = ",".join(temp_value)

    @property
    def month(self) -> str:
        return self.__month

    @month.setter
    def month(self, value:  List[int]) -> None:
        temp_value = [str(i) for i in value]
        self.__month = ",".join(temp_value)

    @property
    def errorHandling(self) -> ErrorHandling:
        return self.__error_handling

    @errorHandling.setter
    def errorHandling(self, value: ErrorHandling) -> None:
        self.__error_handling = value

    @property
    def isQueueUpType(self) -> bool:
        return self.__is_queue_up_type

    @isQueueUpType.setter
    def isQueueUpType(self, value: bool) -> None:
        self.__is_queue_up_type = value

    @property
    def taskNumber(self) -> int:
        return self.__task_number

    @taskNumber.setter
    def taskNumber(self, value: int) -> None:
        self.__task_number = value

    @property
    def tasKPriority(self) -> int:
        return self.__task_priority

    @tasKPriority.setter
    def tasKPriority(self, value: int) -> None:
        self.__task_priority = value

    @property
    def emails(self) -> str:
        return self.__emails

    @emails.setter
    def emails(self, value: list) -> None:
        self.__emails = ",".join(value)

    @property
    def forceRadio(self) -> bool:
        return self.__force_radio

    @forceRadio.setter
    def forceRadio(self, value: bool) -> None:
        self.__force_radio = value

    @property
    def taskScheduleStartDate(self) -> str:
        return self.__task_schedule_start_date

    @taskScheduleStartDate.setter
    def taskScheduleStartDate(self, value: str) -> None:
        self.__task_schedule_start_date = value

    def __getitem__(self, item):
        return getattr(self, item)

    def keys(self):
        attrs = ["yearMonthDay", "hourMinute", "scheduleEndDt", "specifiedValue", "intervalMinute", "intervalHour",
                 "intervalDay", "weeks", "month", "errorHandling", "isQueueUpType", "taskNumber", "tasKPriority",
                 "emails", "forceRadio", "taskScheduleStartDate"]
        l = []
        for i in attrs:
            if getattr(self, i) is not None:
                l.append(i)
        return l


class _JSONEncoder(JSONEncoder):

    def default(self, o):
        if hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, SpecifiedValue):
            print(o)
            return o.value


if __name__ == '__main__':
    s = ScheduleConfig()
    # s.yearMonthDay = "2020-04-27"
    # s.hourMinute = "15:18"
    # s.scheduleEndDt = "2020-05-29 18:20:00"
    s.specifiedValue = SpecifiedValue.INTERVAL_MINUTE
    # s.intervalMinute = 1
    # s.intervalHour = 3
    # s.intervalDay = 5
    s.weeks = ["1", "2"]
    s.month = ["1", "2"]
    print(json.dumps(s, cls=_JSONEncoder))

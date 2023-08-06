# coding=utf-8
# /usr/bin/env/ python

"""
Author: AlibabaCloudRPA
Email:
Create time: 2020-04-27 18:15
IDE: PyCharm
desc: 
"""
from enum import Enum, unique


@unique
class Progress(Enum):
    """
    应用申请状态:
    AUDITING: 审批中
    PASS: 通过
    REJECT: 驳回
    """
    AUDITING = "auditing"
    PASS = "pass"
    REJECT = "reject"


@unique
class ClientStatus(Enum):
    """
    客户端认证状态:
    UNAUTHORIZED: 未认证
    AUTHORIZED: 已认证
    REJECTED: 驳回
    """
    UNAUTHORIZED = "unauthorized"
    AUTHORIZED = "authorized"
    REJECTED = "rejected"


@unique
class ClientDispatchMode(Enum):
    """
    客户端是否可调度:
    ATTEND: 可调度
    UNMANNED: 不可调度
    """
    ATTEND = "attend"
    UNMANNED = "unmanned"


@unique
class ConnectStatus(Enum):
    """
    客户端连接状态:
    CONNECTING: 已连接
    UNCONNECT: 断连中
    LOCKED: 等待执行任务
    RUNNING: 执行中
    IDLE: 空闲
    ERROR: 客户端异常
    """
    CONNECTING = "connecting"
    UNCONNECT = "unconnect"
    LOCKED = "locked"
    RUNNING = "running"
    IDLE = "idle"
    ERROR = "error"


@unique
class ClientType(Enum):
    """
    客户端类型:
    STUDIO: studio
    ROBOT: robot
    ROBOT_ATTENDED: robot_attended
    ROBOT_UNATTENDED: robot_unattended
    ROBOT_SERVICE: robot_service
    """
    STUDIO = "studio"
    ROBOT = "robot"
    ROBOT_ATTENDED = "robot_attended"
    ROBOT_UNATTENDED = "robot_unattended"
    ROBOT_SERVICE = "robot_service"


@unique
class DispatchMode(Enum):
    """
    调度模式；
    ATTEND： 不可调度
    UNMANNED： 可调度
    """
    ATTEND = "attend"
    UNMANNED = "unmanned"


@unique
class AppMarketStatus(Enum):
    """
    应用在市场的状态:
    PUBLISH： 已发布
    UNSHELVE： 已下架
    """
    PUBLISH = "publish"
    UNSHELVE = "unshelve"


@unique
class FromType(Enum):
    """
    应用来源：
    PROJECT: 工程文件
    BUY： 购买
    CONSOLE： 控制台
    """
    PROJECT = "project"
    BUY = "buy"
    CONSOLE = "console"


@unique
class SchedulesTaskStatus(Enum):
    """
    任务状态：
    WAIT：未运行
    RUNNING：正在运行
    TERMINATION：手动结束
    COMPLETION：运行结束
    ERROR：异常结束
    NOT_MATCH：未分配
    NOT_READY：未就绪
    """
    WAIT = "wait"
    RUNNING = "running"
    TERMINATION = "termination"
    COMPLETION = "completion"
    ERROR = "error"
    NOT_MATCH = "unmatch"
    NOT_READY = "notready"


@unique
class ScheduleType(Enum):
    """
    计划任务，任务执行类型
    SPECIFIED_TIME：指定时间
    IMMEDIATE：立即执行
    SPECIFIED_INTERVAL_TIME：指定间隔时间
    DAY_INTERVAL：指定间隔天数
    WEEK_INTERVAL：指定每隔周几
    MONTH_INTERVAL：指定每隔几月
    CRON_EXPRESS：直接指定 cron 表达式
    """
    SPECIFIED_TIME = "specified_time"
    IMMEDIATE = "immediate"
    SPECIFIED_INTERVAL_TIME = "specified_interval_time"
    DAY_INTERVAL = "day_interval"
    WEEK_INTERVAL = "week_interval"
    MONTH_INTERVAL = "month_interval"
    CRON_EXPRESS = "cron_express"


@unique
class SpecifiedValue(Enum):
    """
    计划任务间隔类型
    INTERVAL_MINUTE: 间隔类型为分钟
    INTERVAL_HOUR： 间隔类型为小时
    INTERVAL_DAY： 间隔类型为天
    """
    INTERVAL_MINUTE = "intervalMinute"
    INTERVAL_HOUR = "intervalHour"
    INTERVAL_DAY = "intervalDay"


@unique
class ErrorHandling(Enum):
    """
    错误处理方式
    RESUBMIT: 重试
    TERMINATION: 终止
    """
    RESUBMIT = "resubmit"
    TERMINATION = "termination"


@unique
class TaskBatchStatus(Enum):
    """
    任务批次执行状态
    RUNNING: 进行中
    ALL_FINISH: 结束
    """
    RUNNING = "running"
    ALL_FINISH = "all_finish"


@unique
class AppParamType(Enum):
    """
    appParams参数type类型
    TEXT_EDIT: 文本
    COMBOBOX: 下拉框
    CHECKED_COMBOBOX: 已有选中项的下拉框
    OPEN_FILE: 文件
    OPEN_DIR: 目录
    DATE_EDIT: 日期
    COLOR_PICK:  颜色
    PASSWORD_TEXT_EDIT: 密码
    HTML_TEXT_EDIT: html
    MULTI_TEXT_EDIT: 富文本
    """
    TEXT_EDIT = 0
    COMBOBOX = 1
    CHECKED_COMBOBOX = 2
    OPEN_FILE = 3
    OPEN_DIR = 4
    DATE_EDIT = 5
    COLOR_PICK = 6
    PASSWORD_TEXT_EDIT = 7
    HTML_TEXT_EDIT = 8
    MULTI_TEXT_EDIT = 9


if __name__ == '__main__':
    print(Progress.AUDITING.value)
    print(Progress("auditing").value)

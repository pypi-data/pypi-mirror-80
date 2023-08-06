# coding=utf-8
# /usr/bin/env/ python

"""
Author: AlibabaCloudRPA
Email:
Create time: 2020-04-26 10:30
IDE: PyCharm
desc: 
"""

# endpoint
ENDPOINT: str = "http://api-rpa.aliyun.com"

# 查询客户端信息
QUERY_CLIENT_VIEWS_PATH: str = "/rpa/openapi/client/queryClientViews"
# 查询指定客户端对应的任务数
QUERY_TASK_BY_CLIENT_ID_AND_STATUS_PATH: str = "/rpa/openapi/client/queryTaskByClientIdAndStatus"
# 修改客户端状态
UPDATE_CLIENT_STATUS_PATH: str = "/rpa/openapi/client/updateClientStatus"
# 修改客户端是否可调度
UPDATE_CLIENT_DISPATCH_MODE_PATH: str = "/rpa/openapi/client/updateClientDispatchMode"
# 更新客户端信息
UPDATE_CLIENT_INFO_PATH: str = "/rpa/openapi/client/updateClientInfo"
# 断开客户端连接
DISCONNECT_CLIENT_PATH: str = "/rpa/openapi/client/disconnectClient"
# 删除客户端
DELETE_CLIENT_PATH: str = "/rpa/openapi/client/deleteClient"
# 根据客户端唯一标识符查询客户端信息
QUERY_CLIENT_BY_UUID_PATH: str = "/rpa/openapi/client/queryClientByUuid"
# 查询客户端信息
QUERY_CLIENT_VIEW_BY_ID_PATH: str = "/rpa/openapi/client/queryClientViewById"
# 查询用户登录的客户端列表
QUERY_MEMBER_CLIENT_VIEWS_PATH: str = "/rpa/openapi/client/queryMemberClientViews"

# 获取应用列表获取应用列表
QUERY_APPS_PATH: str = "/rpa/openapi/app/queryApps"
# 申请应用
APPLY_APP_PATH: str = "/rpa/openapi/app/applyApp"
# 获取申请列表
QUERY_APPLY_LIST_PATH: str = "/rpa/openapi/app/queryApplyList"
# 查询我的申请列表
QUERY_MY_APP_APPLYS_PATH: str = "/rpa/openapi/app/queryMyAppApplys"
# 查询我的app列表
QUERY_MY_APPS_PATH: str = "/rpa/openapi/app/queryMyApps"
# 通过申请
APPROVE_PATH: str = "/rpa/openapi/app/approve"
# 拒绝申请
REJECT_PATH: str = "/rpa/openapi/app/reject"
# 取消申请
CANCEL_PATH: str = "/rpa/openapi/app/cancel"
# 获取已经申请app
QUERY_APP_APPLY_PATH: str = "/rpa/openapi/app/queryAppApply"

# 创建计划任务
CREATE_TASK_SCHEDULE_PATH: str = "/rpa/openapi/task/createTaskSchedule"
# 运行应用
CREATE_SERVICE_TASK_PATH: str = "/rpa/openapi/task/createServiceTask"
# 查询任务状态
QUERY_TASK_STATUS_PATH: str = "/rpa/openapi/task/queryTaskStatus"
# 查询task结果
QUERY_SERVICE_RESULT_PATH: str = "/rpa/openapi/task/queryServiceResult"
# 根据taskUuid停止任务
TERMINAL_TASK_PATH: str = "/rpa/openapi/task/terminalTask"
# 查询计划任务列表
QUERY_TASK_SCHEDULES_PATH: str = "/rpa/openapi/task/queryTaskSchedules"
# 获取计划任务运行日志
QUERY_TASK_LOGS_PATH: str = "/rpa/openapi/task/queryTaskLogs"
# 根绝客户端唯一标识符获取计划任务
QUERY_TASK_SCHEDULE_BY_CLIENT_ID_PATH: str = "/rpa/openapi/task/queryTaskScheduleByClientId"
# 根绝客户端唯一标识符获取任务
QUERY_TASK_BY_CLIENT_ID_PATH: str = "/rpa/openapi/task/queryTaskByClientId"
# 根据taskScheduleId查询任务批次
QUERY_TASK_BATCH_BY_TASK_SCHEDULE_ID_PATH: str = "/rpa/openapi/task/queryTaskBatchByTaskScheduleId"
# 根据TaskBatchId查询任务
QUERY_TASK_BY_TASK_BATCH_ID_PATH: str = "/rpa/openapi/task/queryTaskByTaskBatchId"

# 文件上传
UPLOAD_FILE_PATH: str = "/rpa/openapi/file/uploadFile"

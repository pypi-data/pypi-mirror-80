# coding=utf-8
# /usr/bin/env/ python

"""
Author: AlibabaCloudRPA
Email:
Create time: 2020-04-28 18:02
IDE: PyCharm
desc: 
"""
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from rpa_openapi.Enums import ClientType, ConnectStatus, ClientStatus, DispatchMode, AppMarketStatus, FromType, \
    Progress, SchedulesTaskStatus, ScheduleType, TaskBatchStatus


class ErrorResponse(BaseModel):
    timestamp: int
    status: str
    error: str
    message: str
    path: str


class Pager(BaseModel):
    currentPage: int
    totalPage: int
    pageSize: int
    total: int
    limit: int
    offset: int


class Response(BaseModel):
    requestId: str
    success: bool
    msg: str
    msgCode: str
    data: List = None
    pager: Optional[Pager] = None


class ClientView(BaseModel):
    uuid: str
    groupId: str
    clientType: ClientType
    name: str
    ip: str
    macAddress: str
    status: ClientStatus
    dispatchMode: DispatchMode
    remark: str = None
    connectTime: int
    disconnectTime: int = None
    userId: str
    userName: str
    appId: str = None
    appName: str = None
    taskId: str = None
    connectStatus: ConnectStatus


class QueryClientViewsResponse(BaseModel):
    requestId: str
    success: bool
    code: int
    msg: str
    msgCode: str
    data: List[ClientView] = None
    pager: Optional[Pager] = None
    instanceId: str = None


class Client(BaseModel):
    uuid: str
    groupId: str
    clientType: ClientType
    name: str
    ip: str
    macAddress: str
    status: ClientStatus
    dispatchMode: DispatchMode


class Task(BaseModel):
    uuid: str
    taskBatchId: str = None
    appId: str
    appName: str
    clientId: str
    status: str
    result: str
    beginTime: str
    endTime: str
    triggerType: str
    taskTrigger: str = None
    client: Client = None


class QueryTaskByClientIdAndStatusResponse(BaseModel):
    requestId: str
    success: bool
    msg: str
    msgCode: str
    data: List[Task] = None
    pager: Optional[Pager] = None


class UpdateClientDispatchModeResponse(BaseModel):
    requestId: str
    success: bool
    msg: str
    msgCode: str
    data: bool = None
    pager: Optional[Pager] = None


UpdateClientInfoResponse = UpdateClientDispatchModeResponse

DisconnectClientResponse = UpdateClientDispatchModeResponse

DeleteClientResponse = UpdateClientDispatchModeResponse


class QueryClientByUuidResponse(BaseModel):
    requestId: str
    success: bool
    msg: str
    msgCode: str
    data: Client = None
    pager: Optional[Pager] = None


class QueryClientViewByIdResponse(QueryClientViewsResponse):
    data: ClientView = None


QueryMemberClientViewsResponse = QueryClientViewsResponse


class App(BaseModel):
    uuid: str
    name: str
    catId: str
    catName: str
    creator: str
    creatorName: str
    creatorNickName: str
    introduction: str
    iconUrl: str
    status: AppMarketStatus
    version: str
    groupId: str
    fromType: FromType


class QueryAPPSResponse(BaseModel):
    """
    获取应用请求响应数据格式
    """
    requestId: str
    success: bool
    msg: str
    msgCode: str
    data: List[App] = None
    pager: Optional[Pager] = None


class ApplyApp(BaseModel):
    uuid: str
    appName: str
    appId: str
    applicant: str
    applyTime: int
    reviewer: str = None
    reviewTime: str = None
    progress: Progress
    memo: str = None


class ApplyAppResponse(BaseModel):
    requestId: str
    success: bool
    msg: str
    msgCode: str
    data: ApplyApp = None
    pager: Optional[Pager] = None


class ApplyList(BaseModel):
    uuid: str
    applicantNickName: str
    applicantName: str
    appName: str
    fromType: FromType
    progress: Progress
    reviewerName: str
    reviewerNickName: str
    reviewTime: int
    applyDate: int
    memo: str


class QueryApplyListResponse(BaseModel):
    requestId: str
    success: bool
    msg: str
    msgCode: str
    data: List[ApplyList] = None
    pager: Optional[Pager] = None


MyAppApplysResponse = QueryApplyListResponse


class MyApp(BaseModel):
    uuid: str
    name: str
    catId: str
    catName: str
    creator: str
    creatorName: str
    creatorNickName: str
    introduction: str
    iconUrl: str = None
    status: AppMarketStatus
    version: str
    groupId: str
    fromType: str


class MyAppsResponse(BaseModel):
    requestId: str
    success: bool
    msg: str
    msgCode: str
    data: List[MyApp] = None
    pager: Optional[Pager] = None


class Approve(BaseModel):
    uuid: str
    # TODO
    # appName not null
    appName: str = None
    appId: str
    applicant: str
    applyTime: int
    reviewer: str = None
    reviewTime: int = None
    progress: Progress
    memo: str = None


class ApproveResponse(BaseModel):
    requestId: str
    success: bool
    msg: str
    msgCode: str
    data: Approve = None
    pager: Optional[Pager] = None


RejectResponse = ApproveResponse

CancelResponse = ApproveResponse

AppApplyResponse = ApproveResponse


class ServiceTask(BaseModel):
    taskId: str
    resultUrl: str


class ServiceTaskResponse(BaseModel):
    """
    服务型任务返回结果
    """
    requestId: str
    success: bool
    msg: str
    msgCode: str
    data: ServiceTask
    pager: Optional[Pager] = None


class TaskStatus(BaseModel):
    status: SchedulesTaskStatus
    statusName: str
    result: str = None


class TaskStatusResponse(BaseModel):
    requestId: str
    success: bool
    msg: str
    msgCode: str
    data: TaskStatus
    pager: Optional[Pager] = None


class ServiceResultResponse(BaseModel):
    requestId: str
    success: bool
    msg: str
    msgCode: str
    data: str = None
    pager: Optional[Pager] = None


TerminalTaskResponse = UpdateClientDispatchModeResponse


class TaskLog(BaseModel):
    taskId: str
    level: str
    content: str
    gmtCreate: str


class TaskLogsResponse(BaseModel):
    requestId: str
    success: bool
    msg: str
    msgCode: str
    data: List[TaskLog] = None
    pager: Optional[Pager] = None


class TaskSchedules(BaseModel):
    uuid: str
    appId: str
    name: str
    groupId: str
    status: SchedulesTaskStatus
    creator: str
    scheduleType: ScheduleType
    scheduleExpress: str = None
    scheduleCron: str = None
    scheduleStartDate: str = None
    scheduleEndDate: str = None
    nextTaskTime: str = None
    clientType: ClientType
    appName: str
    clientCount: int
    creatorName: str
    creatorNickName: str


class TaskSchedulesResponse(BaseModel):
    requestId: str
    success: bool
    msg: str
    msgCode: str
    data: List[TaskSchedules] = None
    pager: Optional[Pager] = None


TaskScheduleByClientIdResponse = TaskSchedulesResponse


class TaskBatch(BaseModel):
    uuid: str
    taskScheduleId: str
    status: TaskBatchStatus
    result: str = None
    beginTime: str
    endTime: str


class QueryTaskBatchByTaskScheduleIdResponse(BaseModel):
    requestId: str
    success: bool
    msg: str
    msgCode: str
    data: List[TaskBatch] = None
    pager: Optional[Pager] = None


class QueryTaskByTaskBatchIdResponse(BaseModel):
    requestId: str
    success: bool
    msg: str
    msgCode: str
    data: List[Task] = None
    pager: Optional[Pager] = None


class AppParam(BaseModel):
    type: int
    name: str
    default: str = None
    value: str = None


if __name__ == '__main__':
    external_data = {"timestamp": 1588127383873,
                     "status": 500,
                     "error": "Internal Server Error",
                     "message": "feign.RetryableException: Read timed out executing GET "
                                "http://127.0.0.1:7002/internal/service/accesskey/queryByKey?key=5147214e66dc1135",
                     "path": "/rpa/openapi/file/uploadFile"}
    error = ErrorResponse(**external_data)
    # print(error)
    # print(error.timestamp)
    # print(datetime.fromtimestamp(error.timestamp / 1000))
    # print(error.status)
    # print(error.error)
    # print(error.message)
    # print(error.path)

    query_client_views_response_data = {
        "requestId": "f163955b-4ce0-474f-ae34-8010a7f303aa",
        "success": True,
        "code": 0,
        "msg": "调用成功",
        "msgCode": "result.success",
        "data": [
            {
                "uuid": "771F76A4DB09F694C3655C64FD8F26E4",
                "groupId": "b8e097d8-605c-47cf-a5a3-db5d13f8b4ca",
                "clientType": "robot",
                "name": "ITDA-D-22633726",
                "ip": "30.11.92.173",
                "macAddress": "A0:63:91:7F:3F:58",
                "status": "unauthorized",
                "dispatchMode": "attend",
                "remark": None,
                "connectTime": 1587722444000,
                "disconnectTime": None,
                "userId": "93bf42a1-6e65-4912-98b2-4d5ec0e6260a",
                "userName": "ss-test",
                "appId": None,
                "appName": None,
                "taskId": None,
                "connectStatus": "unconnect"
            }
        ],
        "pager": {
            "currentPage": 1,
            "totalPage": 8,
            "pageSize": 1,
            "total": 8,
            "limit": 1,
            "offset": 0
        }
    }

    query_client_views_response = QueryClientViewsResponse(**query_client_views_response_data)
    print(query_client_views_response)
    print(query_client_views_response.data[0].uuid)

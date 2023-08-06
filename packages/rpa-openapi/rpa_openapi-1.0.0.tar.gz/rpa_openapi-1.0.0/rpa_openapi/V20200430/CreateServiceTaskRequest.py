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

from rpa_openapi.V20200430.Request import Request
from rpa_openapi.V20200430.path import CREATE_SERVICE_TASK_PATH
from rpa_openapi.RPAException import RPAException


class CreateServiceTaskRequest(Request):
    """
    创建服务型任务
    """

    def __init__(self):
        super().__init__(CREATE_SERVICE_TASK_PATH)
        self.__app_id = None
        self.__app_params = None
        self.__client_id = None
        self.__callback_url = None
        self.method = "POST"

    def __repr__(self) -> str:
        return "<CreateServiceTaskRequest>: app_id={}, app_params={}, client_id={}, callback_url={}".format(self.__app_id, self.__app_params, self.__client_id, self.__callback_url)

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
    def app_params(self) -> str:
        return self.__app_params

    @app_params.setter
    def app_params(self, value: dict) -> None:
        """
        param: value: appParams,应用参数
        """
        self.__app_params = json.dumps(value)

    @property
    def client_id(self) -> str:
        return self.__client_id

    @client_id.setter
    def client_id(self, value: str) -> None:
        """
        param: value: robotUuid,机器人UUID
        """
        self.__client_id = value

    @property
    def callback_url(self) -> str:
        return self.__callback_url

    @callback_url.setter
    def callback_url(self, value: str) -> None:
        """
        param: value: callbackUrl,应用运行结束后请求返回结果的回调地址
        """
        self.__callback_url = value

    @property
    def params(self) -> dict:
        d = {}
        if self.__app_id:
            d["appId"] = self.__app_id
        else:
            raise RPAException("appId参数不能为空")
        if self.__app_params:
            d["appParams"] = self.__app_params
        if self.__client_id:
            d["clientId"] = self.__client_id
        if self.__callback_url:
            d["callbackUrl"] = self.__callback_url
        return d

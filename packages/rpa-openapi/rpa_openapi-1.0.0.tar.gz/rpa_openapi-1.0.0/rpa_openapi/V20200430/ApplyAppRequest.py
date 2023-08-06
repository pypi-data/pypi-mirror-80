# coding=utf-8
# /usr/bin/env/ python

"""
Author: AlibabaCloudRPA
Email:
Create time: 2020-04-26 19:53
IDE: PyCharm
desc: 
"""
from rpa_openapi.V20200430.Request import Request
from rpa_openapi.V20200430.path import APPLY_APP_PATH


class ApplyAppRequest(Request):
    """
    创建服务型任务
    """

    def __init__(self):
        super().__init__(APPLY_APP_PATH)
        self.__app_id = None
        self.method = "POST"

    def __repr__(self) -> str:
        return "<CreateServiceTaskRequest>: app_id={}".format(self.__app_id)

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
    def params(self) -> dict:
        d = {}
        if self.__app_id:
            d["appId"] = self.__app_id
        return d

# coding=utf-8
# /usr/bin/env/ python

"""
Author: AlibabaCloudRPA
Email:
Create time: 2020-04-26 12:01
IDE: PyCharm
desc: 
"""
from rpa_openapi.V20200430.Request import Request
from rpa_openapi.V20200430.path import UPLOAD_FILE_PATH
from rpa_openapi.RPAException import RPAException


class UploadFileRequest(Request):
    """
    文件上传
    """

    def __init__(self):
        super().__init__(UPLOAD_FILE_PATH)
        self.__key = None
        self.__file = None
        self.method = "POST"

    def __repr__(self) -> str:
        return "<UploadFileRequest>: key={}".format(self.__key)

    @property
    def key(self) -> str:
        return self.__key

    @key.setter
    def key(self, value: str) -> None:
        """
        param: value: applyId,申请记录唯一标识符
        """
        self.__key = value

    @property
    def file(self) -> bytes:
        return self.__file

    @file.setter
    def file(self, value: bytes) -> None:
        """
        param: value: applyId,申请记录唯一标识符
        """
        self.__file = value

    @property
    def params(self) -> dict:
        d = {}
        if self.__key:
            d["key"] = self.__key
        if self.__file:
            d["file"] = self.__file
        else:
            raise RPAException("file参数不能为空")
        return d

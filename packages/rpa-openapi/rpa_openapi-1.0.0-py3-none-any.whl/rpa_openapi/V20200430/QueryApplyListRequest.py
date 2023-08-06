# coding=utf-8
# /usr/bin/env/ python

"""
Author: AlibabaCloudRPA
Email:
Create time: 2020-04-26 19:53
IDE: PyCharm
desc: 
"""
from rpa_openapi.V20200430.BaseQueryRequest import BaseQueryRequest
from rpa_openapi.V20200430.path import QUERY_APPLY_LIST_PATH
from rpa_openapi.Enums import Progress


class QueryApplyListRequest(BaseQueryRequest):
    """
    查询申请列表
    """

    def __init__(self):
        super().__init__(QUERY_APPLY_LIST_PATH)
        self._progress = None

    def __repr__(self) -> str:
        return "<QueryApplyListRequest>: progress={}, current_page={}, page_size={}".format(self._progress,
                                                                                            self.current_page,
                                                                                            self.page_size)

    @property
    def progress(self) -> Progress:
        return self._progress

    @progress.setter
    def progress(self, value: Progress) -> None:
        """
        param: value: app名称,非必选参数
        """
        self._progress = value

    @property
    def params(self) -> dict:
        d = {}
        if self._progress:
            d["progress"] = self._progress.value
        if self.current_page:
            d["currentPage"] = str(self.current_page)
        if self.page_size:
            d["pageSize"] = str(self.page_size)
        return d

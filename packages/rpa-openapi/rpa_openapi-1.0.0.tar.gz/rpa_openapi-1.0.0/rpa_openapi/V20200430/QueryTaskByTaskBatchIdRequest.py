from rpa_openapi.V20200430.BaseQueryRequest import BaseQueryRequest
from rpa_openapi.V20200430.path import QUERY_TASK_BY_TASK_BATCH_ID_PATH


class QueryTaskByTaskBatchIdRequest(BaseQueryRequest):
    """
    根据taskBatchId查询任务详情
    """

    def __init__(self):
        super().__init__(QUERY_TASK_BY_TASK_BATCH_ID_PATH)
        self.__task_batch_id = None

    def __repr__(self) -> str:
        return "<QueryTaskByTaskBatchIdRequest>: task_batch_id={}, current_page={}, page_size={}".format(
            self.__task_batch_id, self.current_page, self.page_size)

    @property
    def task_batch_id(self) -> str:
        return self.__task_batch_id

    @task_batch_id.setter
    def task_batch_id(self, value: str) -> None:
        """
        param: value: taskScheduleId,计划任务唯一标识UUID
        """
        self.__task_batch_id = value

    @property
    def params(self) -> dict:
        d = {}
        if self.__task_batch_id:
            d["taskBatchId"] = self.__task_batch_id
        if self.current_page:
            d["currentPage"] = str(self.current_page)
        if self.page_size:
            d["pageSize"] = str(self.page_size)
        return d

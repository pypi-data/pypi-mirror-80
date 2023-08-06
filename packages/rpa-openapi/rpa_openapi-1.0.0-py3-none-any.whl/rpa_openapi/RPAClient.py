# coding=utf-8
# /usr/bin/env/ python

"""
Author: AlibabaCloudRPA
Email:
Create time: 2020-04-26 10:22
IDE: PyCharm
desc: 
"""
import base64
from hashlib import sha1
from urllib import parse

import requests

from rpa_openapi.Utils import Utils
from rpa_openapi.V20200430.Request import Request
from rpa_openapi.V20200430.path import ENDPOINT


class RPAClient:

    def __init__(self, access_key_id: str, access_secret: str, *, signature_method=None, signature_version=None,
                 version=None, data_format=None, endpoint=ENDPOINT):
        """
        param: endpoint: 服务器地址
        """
        self.access_key_id = access_key_id
        self.access_secret = access_secret
        self.signature_method = signature_method if signature_method else "HMAC-SHA1"
        self.signature_version = signature_version if signature_version else "1.0"
        self.signature_nonce = Utils.get_random_string()
        self.timestamp = Utils.get_now_utc_time()
        self.version = version if version else "20200430"
        self.data_format = data_format if data_format else "json"
        self.endpoint = endpoint

    def do_action(self, request: Request):
        params = {"AccessKeyId": self.access_key_id,
                  "Format": self.data_format,
                  "SignatureMethod": self.signature_method,
                  "SignatureNonce": self.signature_nonce,
                  "SignatureVersion": self.signature_version,
                  "Timestamp": self.timestamp,
                  "Version": self.version}
        params.update(request.params)
        request_params = self.build_params(request.method, params)
        url = self.endpoint + request.path
        if request.method.upper() == "GET":
            response = requests.get(url, params=request_params)
        elif request.method.upper() == "POST":
            response = requests.post(url, params=request_params)
        else:
            raise Exception("请求失败")
        return response

    def do_action_with_file(self, request):
        params = {"AccessKeyId": self.access_key_id,
                  "Format": self.data_format,
                  "SignatureMethod": self.signature_method,
                  "SignatureNonce": self.signature_nonce,
                  "SignatureVersion": self.signature_version,
                  "Timestamp": self.timestamp,
                  "Version": self.version}
        if request.params.get("key"):
            params.update({"key": request.params.get("key")})
        files = request.params.get("file")
        request_params = self.build_params(request.method, params)
        url = self.endpoint + request.path
        response = requests.post(url=url, params=request_params, files=files)
        return response

    def build_params(self, method: str, params: dict) -> dict:
        string_to_sign = self.build_string_to_sign(method.upper(), params)
        h = Utils.hash_hmac(self.access_secret + '&', string_to_sign, sha1)
        params["Signature"] = base64.b64encode(h)
        return params

    @staticmethod
    def build_string_to_sign(method: str, params: dict) -> str:
        items = list(params.keys())
        items.sort()
        temp_list = []
        for i in items:
            temp_list.append(parse.quote(i, safe='') + "=" + parse.quote(params[i], safe=''))
        temp_string = "&".join(temp_list)
        return method.upper() + "&%2F&" + parse.quote(temp_string)

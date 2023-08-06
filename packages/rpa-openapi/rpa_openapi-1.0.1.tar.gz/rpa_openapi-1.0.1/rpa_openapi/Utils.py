# coding=utf-8
# /usr/bin/env/ python

"""
Author: AlibabaCloudRPA
Email:
Create time: 2020-04-26 10:23
IDE: PyCharm
desc: 
"""
import datetime
import hmac
import random


class Utils:

    @staticmethod
    def get_now_utc_time() -> str:
        utcnow = datetime.datetime.utcnow()
        # s = utcnow.strftime("%Y-%m-%dT%H:%M:%S") + Utils().format_utcoffset(utcnow.astimezone().utcoffset())
        s = utcnow.strftime("%Y-%m-%dT%H:%M:%SZ")
        return s

    @staticmethod
    def format_utcoffset(off: datetime.timedelta) -> str:
        s = ''
        if off is not None:
            if off.days < 0:
                sign = "-"
                off = -off
            else:
                sign = "+"
            hh, mm = divmod(off, datetime.timedelta(hours=1))
            mm, ss = divmod(mm, datetime.timedelta(minutes=1))
            s += "%s%02d%02d" % (sign, hh, mm)
            if ss or ss.microseconds:
                s += "%02d" % ss.seconds

                if ss.microseconds:
                    s += '.%06d' % ss.microseconds
        return s

    @staticmethod
    def get_random_string() -> str:
        return ''.join(random.sample('abcdefghijklmnopqrstuvwxyz!@#$%^&*()0123456789', 32))

    @staticmethod
    def hash_hmac(ac_key, text, sha1):
        return hmac.new(ac_key.encode("utf-8"), text.encode("utf-8"), sha1).digest()


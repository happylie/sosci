#!/usr/bin/python
# -*- coding: utf-8 -*-
from urllib.parse import urlparse
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError


class UrlPaser:
    def __init__(self):
        self.a = ""

    @staticmethod
    def __url_check(url):
        try:
            with urlopen(url) as response:
                status_code = response.getcode()
                if status_code != 200:
                    return False
            return True
        except HTTPError as err:
            return False
        except URLError as err:
            return False

    def get_parser(self, data):
        """
        Get URL Parser
        :param data: Parse URL
        :return: True/False, host, port
        """
        try:
            obj = urlparse(data)
            scheme = obj.scheme if obj.scheme else 'https'
            hostname = obj.hostname
            if not hostname:
                c_str = '{scheme}://{url}'.format(scheme=scheme, url=data)
                obj = urlparse(c_str)
            host = obj.hostname if obj.hostname else hostname
            port = obj.port if obj.port else 443
            url = '{scheme}://{host}:{port}'.format(scheme=scheme, host=host, port=port)
            if not self.__url_check(url):
                return False, None, None
            return True, host, port
        except Exception as err:
            return False, None, None

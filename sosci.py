#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import json
import socket
import ssl
import sys
from datetime import datetime
from util.url_parser import UrlPaser


class Colors:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


class SSLInfo:
    def __init__(self, host, sport):
        ctx = ssl.create_default_context()
        try:
            with socket.create_connection((host, sport)) as self.sock:
                with ctx.wrap_socket(self.sock, server_hostname=host) as s:
                    self.ret = s.getpeercert()
        except Exception as err:
            sys.exit(0)

    def __del__(self):
        self.sock.close()

    @staticmethod
    def __expire_date(end_date):
        try:
            now_date = datetime.now()
            expire_date = end_date - now_date
            if expire_date.days < -1:
                ret = '-1 Days'
                return ret
            ret = '{expire_in} Days'.format(expire_in=expire_date.days)
        except Exception as err:
            ret = '0 Days'
        return ret

    def __convert_dict2json(self, data):
        dns_list = []
        for i in data['subjectAltName']:
            dns_list.append(i[1])
        subjectaltname_data = {
            "DNS": dns_list
        }
        start_date = datetime.strptime(data['notBefore'], "%b %d %H:%M:%S %Y %Z")
        end_date = datetime.strptime(data['notAfter'], "%b %d %H:%M:%S %Y %Z")
        expire_date = self.__expire_date(end_date)
        ret = {
            "subject": dict(i[0] for i in data['subject']),
            "issuer":  dict(i[0] for i in data['issuer']),
            "notBefore": str(start_date),
            "notAfter": str(end_date),
            "expireDate": expire_date,
            "subjectAltName": subjectaltname_data
        }
        return json.dumps(ret)

    def run(self):
        return self.__convert_dict2json(self.ret)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='sosci.py', description='Search of SSL Certification Information(SoSCI)')
    try:

        parser.add_argument('-u', '--url', dest='url', type=str, help='Check URL(HTTPS URL or Hostname)')
        parser.add_argument('-e', '--expire', dest='exp', action='store_false', help='Certification Expire Date')
        parser.add_argument('-v', '--version', action='version', version='sosci v1.0')
        args = parser.parse_args()
        if not args.url:
            print('Input the URL')
            sys.exit(0)
        up = UrlPaser().get_parser(args.url)
        if not up[0]:
            print('URL is not valid')
            sys.exit(0)
        hostname = up[1]
        port = up[2]
        si = SSLInfo(hostname, port)
        obj = si.run()
        if args.exp:
            print(obj)
        else:
            ret = {
                "expireDate": json.loads(obj)['expireDate']
            }
            print(json.dumps(ret))
        sys.exit(0)
    except Exception as err:
        print("main:: {err}".format(err=err))
        sys.exit(0)


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
            "status": {
                "code": 0,
                "msg": "SSL Certification Information"
            },
            "result": {
                "subject": dict(i[0] for i in data['subject']),
                "issuer": dict(i[0] for i in data['issuer']),
                "notBefore": str(start_date),
                "notAfter": str(end_date),
                "expireDate": expire_date,
                "subjectAltName": subjectaltname_data
            }
        }
        return json.dumps(ret, indent=4, sort_keys=True)

    def run(self):
        return self.__convert_dict2json(self.ret)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='sosci.py', description='Search of SSL Certification Information(SoSCI)',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    if len(sys.argv) == 1:
        ret = {
            "status": {
                "code": 1,
                "msg": "Input the URL"
            },
            "result": {}
        }
        print(json.dumps(ret, indent=4, sort_keys=True))
        sys.exit(0)
    parser.add_argument('url', type=str, help='Check URL(HTTPS URL or Hostname)')
    parser.add_argument('-e', '--expire', action='store_true', dest='exp', help='Certification Expire Date')
    parser.add_argument('-v', '--version', action='version', version='sosci v1.1')
    try:
        args = parser.parse_args()
        up = UrlPaser().get_parser(args.url)
        if not up[0]:
            ret = {
                "status": {
                    "code": 1,
                    "msg": "URL is not valid"
                },
                "result": {}
            }
            print(json.dumps(ret, indent=4, sort_keys=True))
            sys.exit(0)
        si = SSLInfo(up[1], up[2])
        obj = si.run()
        if args.exp:
            ret = {
                "status": {
                    "code": 0,
                    "msg": "SSL Expire Date"
                },
                "result": {
                    "expireDate": json.loads(obj)['result']['expireDate']
                }
            }
            print(json.dumps(ret, indent=4, sort_keys=True))
        else:
            print(obj)
        sys.exit(0)
    except Exception as err:
        print(err)
        ret = {
            "status": {
                "code": 1,
                "msg": "ArgumentParser Error"
            },
            "result": {}
        }
        print(json.dumps(ret, indent=4, sort_keys=True))
        sys.exit(0)


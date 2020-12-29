# coding:utf-8

from payload.tomcat_put import tomcat_put_rwf_scan
from payload.tomcat_auth_brute import tomcat_auth
from core.common import *
import sys

version = "v1.4"
author = "jijue"

_py_version = int(sys.version.split()[0][0])

if _py_version >= 3:
    logging_message("critical","python版本大于3，自动退出")
    print "不支持python3，换成python2.7试试"
    sys.exit(0)

logging_message("info","Google_Hacker_Est 启动")
vuln_scan(semi_automatic(),tomcat_auth)

logging_message("info","扫描结束")
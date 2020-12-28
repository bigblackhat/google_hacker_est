# coding:utf-8

from payload.tomcat_put import tomcat_put_rwf_scan
from core.common import *


version = "v1.4"
author = "jijue"

logging_message("info","Google_Hacker_Est 启动")
vuln_scan(semi_automatic(),tomcat_put_rwf_scan)

logging_message("info","扫描结束")
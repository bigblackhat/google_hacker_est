# coding:utf-8

import requests
from tqdm import tqdm

from google_core import semi_automatic

from payload.thinkphp_5_0_23 import scan


_safe_list = []
_unsafe_list = []
vuln_list = []
unvuln_list = []

"""
TODO 
最大重连次数  
timeout设置  

进度条显示

scan模块 url解析

windows 版本 dir dns记录
"""
url_list = semi_automatic()
# url_list = ["http://www.loveblq.top/"]

def life_scan(url_list=url_list):
    """
    url存活检测  
    url_list:url列表  
    无返回，直接将存活和无响应的url写入_safe_list和_unsafe_list
    """
    print "开始进行存活检测"
    for i in tqdm(url_list):
        try:
            res = requests.get(url=i,timeout=30)
            if res.status_code == 200:
                _safe_list.append(i)
                # print "%s |!_!| %s" % (res.status_code,i)
            else:
                _unsafe_list.append(i)
        except (requests.exceptions.ConnectionError,requests.exceptions.ReadTimeout) as e:
            # print "连不上 %s" % (i)
            _un_reach = i +" |!_!| " + str(e)
            _unsafe_list.append(_un_reach)
            continue
    print "%d条存活，%d条无响应或不可达\n" % (len(_safe_list),len(_unsafe_list))

# print len(_safe_list)
# print len(_unsafe_list)
# _safe_list.append("http://127.0.0.1:8080/")

def vul_scan(_safe_list=_safe_list):
    """
    存活url，调用漏洞检测模块扫描  
    _safe_list:存活url列表  
    无返回，直接将有漏洞和没有漏洞的url分别写入vuln_list和unvuln_list
    """
    print "开始进行漏洞检测"
    for i in tqdm(_safe_list):
        vuln = scan(i)
        if vuln == True:
            vuln_list.append(i)
        elif vuln == False:
            unvuln_list.append(i)
        elif "|!_!|" in vuln :
            _unsafe_list.append(i)
    print "漏洞检测完毕\n%d条存在漏洞，%d条不存在漏洞\n" % (len(vuln_list),len(unvuln_list))

def output(vuln_list=vuln_list,unvuln_list=unvuln_list,_unsafe_list=_unsafe_list):
    _d = "#"*20
    with open("_init/vuln.txt","w") as f:
        f.write(_d + "  vulnerability " + _d + "\n\n")
        for i in vuln_list:
            f.write(i + "\n\n")

        f.write("\n\n\n" + _d + "  un_vuln  " + _d + "\n\n")
        for i in unvuln_list:
            f.write(i + "\n\n")

        f.write("\n\n\n" + _d + "  un_reach  " + _d + "\n\n")
        for i in _unsafe_list:
            f.write(i + "\n\n")

def main():
    life_scan()
    vul_scan()
    output()

if __name__ == "__main__":
    main()
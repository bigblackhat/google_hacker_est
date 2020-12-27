# coding:utf-8
import requests
# import socks
from bs4 import BeautifulSoup
import random
import time
import json
import re

"""
[对于 Python 抓取 Google 搜索结果的一些了解](https://juejin.cn/post/6844903750939705357)
"""

# robots = ["About this page"]

# sleep_time = random.randint(45,70)

# query = "intitle:\"index of\"+\"backup files\"".replace(" ","+")



# def gen_user_agent():
#     with open("data/user_agents.txt","r") as f:
#         ua_file = f.readlines()
#         ua_list = [i.strip() for i in ua_file]
#     # user_list = user_agent_list.strip().splitlines()
#     # user_list = [i.strip() for i in user_list]
#     return random.choice(ua_list)

# def gen_domain():
#     with open("data/all_domain.txt","r") as f:
#         domain_file = f.readlines()
#         domain_list = [i.strip() for i in domain_file]
#     return random.choice(domain_list)
# dork = "intitle:'Welcome to JBoss AS"

# def google_search_core(dork,page=0):
#     domain = gen_domain()
#     url = "http://" + domain + "/search?hl=en&q={}&start={}&btnG=Search&gbv=1".format(dork,page)
#     url.replace(" ","")
#     headers = {'user-agent': gen_user_agent(),"Connection":"close"}
#     try:
#         response = requests.get(url, proxies={
#             'http': 'socks5://127.0.0.1:1086',
#             'https': 'socks5://127.0.0.1:1086'
#         },headers=headers)
#         # print response.status_code
#     except Exception as e:
#         print e 
#         exit(0)

#     if response.status_code == 200:

#         print response.status_code

#         if robots[0] in response.text :
#             print "响应 {}".format(response.status_code)
#             print "请求域名为 %s" % (domain)
#             print "遭遇robots 检查，sleep %d秒" % (sleep_time)
#             time.sleep(sleep_time)
#             print "休眠结束，可继续进行测试"

#         with open("_init/_init.html","w") as f:
#             f.write(response.text.encode("utf-8"))

#         with open("_init/_init.html","r") as f:
#             print google_response_parse(f.read())

#         print "请求成功，休眠%d秒" % (sleep_time)
#         time.sleep(sleep_time)            
#         print "休眠结束,可继续进行测试"

#     elif response.status_code == 429 and robots[0] in response.text:
#         print "响应 {}".format(response.status_code)
#         print "请求域名为 %s" % (domain)
#         print "遭遇robots 检查，sleep %d秒" % (sleep_time)
#         time.sleep(sleep_time)
#         print "休眠结束，可继续进行测试"

#     else:
        
#         print response.status_code
#         print response.text
#         exit("未知HTTP错误")


def google_response_parse(html_source):

    html = BeautifulSoup(html_source,"html.parser")

    result_list = list()
    for i in html.find_all(rel="noopener"):
        if "cached" in str(i).lower():
            continue
        url = i["href"]
        title = str(i.span)

        line = "{} |!_!| {}".format(title,url)
        result_list.append(line)

    return result_list

def remove_span(str_title):
    if "<span>" in str_title:
        str_title = str_title.replace("<span>","")

    if "</span" in str_title:
        str_title = str_title.replace("</span>","")
    return str_title



def semi_automatic():
    with open("_init/_init.html","r") as f:
            file_content = f.read()
            result = google_response_parse(file_content)
    with open("_init/result.txt","w") as f:
        for i in result:
            if "webcache.googleusercontent" in i:
                continue
            if "translate.google" in i :
                continue
            i = remove_span(i)
            f.write(i+"\n")
    with open("_init/result.txt","r") as f:
        lists = f.readlines()

        target_list = []
        for i in lists:
            i = i.split("|!_!|")[1].strip()
            target_list.append(i)
        # print len(target_list)
        return target_list

if __name__ == "__main__":
    print semi_automatic()
    

    # google_search_core(dork)

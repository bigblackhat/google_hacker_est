# coding:utf-8
import requests
import socks
from bs4 import BeautifulSoup
import random
import time
import json
import re

"""
[对于 Python 抓取 Google 搜索结果的一些了解](https://juejin.cn/post/6844903750939705357)
"""

robots = ["About this page"]

sleep_time = random.randint(45,70)

query = "intitle:\"index of\"+\"backup files\"".replace(" ","+")



def gen_user_agent():
    with open("data/user_agents.txt","r") as f:
        ua_file = f.readlines()
        ua_list = [i.strip() for i in ua_file]
    # user_list = user_agent_list.strip().splitlines()
    # user_list = [i.strip() for i in user_list]
    return random.choice(ua_list)

def gen_domain():
    with open("data/all_domain.txt","r") as f:
        domain_file = f.readlines()
        domain_list = [i.strip() for i in domain_file]
    return random.choice(domain_list)
dork = "intitle:'Welcome to JBoss AS"

def google_search_core(dork):
    url = "http://" + gen_domain() + "/search?q={}".format(dork)
    url.replace(" ","")
    headers = {'user-agent': gen_user_agent(),"Connection":"close"}
    try:
        response = requests.get(url, proxies={
            'http': 'socks5://127.0.0.1:1086',
            'https': 'socks5://127.0.0.1:1086'
        },headers=headers)
        # print response.status_code
    except Exception as e:
        print e 
        exit(0)

    if response.status_code == 200:

        print response.status_code

        if robots[0] in response.text :
            print "遭遇robots 检查，sleep %d秒" % (sleep_time)
            time.sleep(sleep_time)
            print "休眠结束，可继续进行测试"

        with open("_init/_init.html","w") as f:
            f.write(response.text.encode("utf-8"))

        with open("_init/_init.html","r") as f:
            print google_response_parse(f.read())

        print "请求成功，休眠%d秒" % (sleep_time)
        time.sleep(sleep_time)            
        print "休眠结束,可继续进行测试"

    elif response.status_code == 429 and robots[0] in response.text:

        print "遭遇robots 检查，sleep %d秒" % (sleep_time)
        time.sleep(sleep_time)
        print "休眠结束，可继续进行测试"

    else:

        print response.status_code
        print response.text
        exit("未知HTTP错误")


def google_response_parse(html_source):

    html = BeautifulSoup(html_source,"html.parser")

    result_list = list()
    for i in html.find_all(rel="noopener"):
        # print i
        # url = str(i["href"].split("&sa")[0].replace("/url?q=",""))
        # print url
        # try:
        #     title = str(i.span).encode("utf-8").split(">")[1].split("</")[0]
        #     print title    +"\n"
        # except:
        #     print i.span
        # print str(l for l in i["href"].split("&") if "url" in l)
        if i["href"] and i.span:
            for l in i["href"].split("?")[1].split("&"):
                if "url" in l :
                    url = l.split("=")[1]
                    continue
                # print url
            title = str(i.span).split(">")[1].split("</")[0]
            line = "{} | {}".format(title,url)
            result_list.append(line)
        else:
            pass
        

    return result_list


if __name__ == "__main__":
    # with open("_init/_init.html","r") as f:
    #     fc = f.read()
    #     print google_response_parse(fc)

    google_search_core(dork)

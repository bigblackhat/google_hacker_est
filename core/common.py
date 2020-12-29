# coding:utf-8
import requests
from time import sleep
from bs4 import BeautifulSoup
import random
import time
from urlparse import urlparse
from tqdm import tqdm
from requests.exceptions import *
import logging
import os

dork = "intitle:'Welcome to JBoss AS"

robots = ["About this page"]

sleep_time = random.randint(45,70)

query = "intitle:\"index of\"+\"backup files\"".replace(" ","+")

root_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__))+os.path.sep+"..")

# 日志配置信息
# 我设成了level为INFO了，DEBUG实在是太啰嗦了
logging.basicConfig(filename=root_path + '/_init/run.log',
                    format='[%(asctime)s-%(levelname)s:%(message)s]', 
                    level = logging.INFO,
                    filemode='w',
                    datefmt='%Y-%m-%d  %I:%M:%S %p')

def logging_message(level,message):
    """
    level :: log级别
    message :: log内容
    """
    if level.lower() == "debug":
        logging.debug("  {}".format(message))
    elif level.lower() == "info":
        logging.info("  {}".format(message))
    elif level.lower() == "warning":
        logging.warning("  {}".format(message))
    elif level.lower() == "error":
        logging.error("  {}".format(message))
    elif level.lower() == "critical":
        logging.critical("  {}".format(message))

def return_line(vuln,info):
    ret_lin = {"info":info,
                "vuln":vuln}
    return ret_lin

def gen_user_agent():
    """
    返回一个随机的user_agent
    """
    with open("data/user_agents.txt","r") as f:
        ua_file = f.readlines()
        ua_list = [i.strip() for i in ua_file]
    return random.choice(ua_list)

def gen_domain():
    """
    返回一个随机的域名，用来躲避谷歌对ip的追踪
    """
    with open("data/all_domain.txt","r") as f:
        domain_file = f.readlines()
        domain_list = [i.strip() for i in domain_file]
    return random.choice(domain_list)


def google_search_core(dork,page=0):
    """
    google search 的核心功能函数  
    问题挺多的，暂时先不用这个功能函数
    """
    domain = gen_domain()
    url = "http://" + domain + "/search?hl=en&q={}&start={}&btnG=Search&gbv=1".format(dork,page)
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
            print "响应 {}".format(response.status_code)
            print "请求域名为 %s" % (domain)
            print "遭遇robots 检查，sleep %d秒" % (sleep_time)
            time.sleep(sleep_time)
            print "休眠结束，可继续进行测试"

        with open("_init/_init.html","w") as f:
            f.write(response.text.encode("utf-8"))

        with open("_init/_init.html","r") as f:
            print google_html_parse(f.read())

        print "请求成功，休眠%d秒" % (sleep_time)
        time.sleep(sleep_time)            
        print "休眠结束,可继续进行测试"

    elif response.status_code == 429 and robots[0] in response.text:
        print "响应 {}".format(response.status_code)
        print "请求域名为 %s" % (domain)
        print "遭遇robots 检查，sleep %d秒" % (sleep_time)
        time.sleep(sleep_time)
        print "休眠结束，可继续进行测试"

    else:
        
        print response.status_code
        print response.text
        exit("未知HTTP错误")



def remove_span(str_title):
    """
    将目标title中的<span>和</span>标签剔除  

    str_title : 要剔除span标签的title

    return  剔除标签以后的str_title
    """
    if "<span>" in str_title:
        str_title = str_title.replace("<span>","")

    if "</span" in str_title:
        str_title = str_title.replace("</span>","")
    return str_title


def google_html_parse(html_source):
    """
    google 搜索返回页面的解析函数，提取出目标的title和url   

    html_source : google 搜索返回页面的html源码  

    返回一个列表  
    """
    html = BeautifulSoup(html_source,"html.parser")
    logging_message("info","开始解析html代码")

    result_list = list()
    for i in html.find_all(rel="noopener"):
        if "cached" in str(i).lower():
            continue
        url = i["href"]
        if "webcache.googleusercontent" in str(url) :
            continue
        elif "translate.google" in str(url):
            continue
        title = remove_span(str(i.span))

        line = "{} |!_!| {}".format(title,url)
        result_list.append(line)

    return result_list


def semi_automatic():
    """
    谷歌翻译，半自动  
    因为google_html_parse函数返回的结果包含了title和url，所以这个函数的主要工作内容就是将url提取出来  
    之所以这么设计是防止google_html_parse函数有缺陷以及scan功能不完善，方便手动调试   
    直接返回url列表
    """

    # 存放google search html源码的文件路径
    with open("_init/_init.html","r") as f:
            file_content = f.read()
            result = google_html_parse(file_content)
    
    # 存放title和url的文件
    with open("_init/target.list","w") as f:
        for i in result:
            f.write(i+"\n")

    with open("_init/target.list","r") as f:
        lists = f.readlines()

        target_list = []
        for i in lists:
            i = i.split("|!_!|")[1].strip()
            target_list.append(i)
        # print len(target_list)
        return target_list


def url_life(url):
    """
    url存活验证函数，逻辑是成功返回True，三次失败就返回False  
    
    只接受url参数  

    return True/False
    """
    for i in range(3):
        e = 0
        try:
            req = requests.get(url)
        except (SSLError,ConnectionError):
            e = 1
        if e == 1:
            continue
        elif req.status_code >= 400 :
            continue
        else :
            logging_message("info","url - {} 存活，开始对该条url进行漏洞检测".format(url))
            return True
        sleep(3)
    logging_message("info","url - {} 未响应或出现错误，跳过该url".format(url))
    return False

def gen_domain_url(url):
    """
    生成任意url的根目录url，用于验证url存活，结尾不带/  
    例 http://domain.com/sd.php?cd=1 => http://domain.com
    """
    url_parse = urlparse(url)
    url = url_parse.scheme + "://" + url_parse.netloc
    return url 


vuln_list = list()
unvuln_list = list()
unreach_list = list()


def vuln_scan(url_list,scan_module):
    """
    调用payload中的模块进行漏洞扫描  
    url_list : 待扫描的url列表  
    scan_module :: 用于扫描的函数   
    直接操作，无
    """
    for i in tqdm(url_list):
        vuln = scan_module(i)
    
        if vuln["vuln"] == "True":
            vuln_list.append(i)
        elif vuln["vuln"] == "False":
            unvuln_list.append(i)
        elif vuln["vuln"] == "unreach":
            unreach_list.append(i)
        output()



def output(vuln_list=vuln_list,unvuln_list=unvuln_list,_unreach_list=unreach_list):
    """
    报告输出模块，接受三个参数，基本不必用户提供  
    直接操作文件，无返回
    """
    _d = "#"*20
    with open("_init/scan_report.txt","w") as f:
        f.write(_d + "  vulnerability " + _d + "\n\n")
        for i in vuln_list:
            f.write(i + "\n\n")

        f.write("\n\n\n" + _d + "  un_vuln  " + _d + "\n\n")
        for i in unvuln_list:
            f.write(i + "\n\n")

        f.write("\n\n\n" + _d + "  un_reach  " + _d + "\n\n")
        for i in unreach_list:
            f.write(i + "\n\n")

if __name__ == "__main__":
    # print url_life("https://www.medpatent.cn/")
    
    # with open("./_init/_init.html","r") as f:
    #     content = f.read()      
    # print google_html_parse(content)  
    # print semi_automatic()

    # print gen_user_agent(),gen_domain()
    # print gen_domain_url("http://www.cvetb.saude.sp.gov.br/mmmm.aspx?cdc=dcd")
    # vuln_scan(semi_automatic(),"tomcat_put_rwf_scan")
    pass
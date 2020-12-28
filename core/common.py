# coding:utf-8
import requests
from time import sleep

def url_life(url):
    """
    url存活验证函数，逻辑是成功返回True，三次失败就返回False  
    只接受url参数  
    """
    for i in range(3):
        e = 0
        try:
            req = requests.get(url)
        except requests.exceptions.SSLError:
            e = 1
        if e == 1:
            continue
        elif req.status_code >= 400 :
            continue
        else :
            return True
        sleep(3)
    return False


if __name__ == "__main__":
    print url_life("https://www.medpatent.cn/")
        
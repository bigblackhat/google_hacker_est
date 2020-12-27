# google-hacker-est

根据google hack语法，获取大量目标，然后逐个验证漏洞存在与否，用于批量拿站

目前正在紧锣密鼓的开发当中，逐步实现以下模块


[-] google 搜索模块

[-] html解析 + 结果输出模块


简单说下思路，要想避开google对爬虫的检查，只能慢，否则就是429警告！

我曾经在5秒内连续请求了两次，就被封了一下午

通过ua和domain随机的方式，可以一定程度上改善这种境况

但仍建议不论请求是否成功，每次都要sleep 50秒以上

第二页的参数是start=10，第三页的参数是start=20，以此类推
https://www.google.com.hk/search?q=python&start=10

num参数是返回数量，默认为10，设为100时将会返回100条数据，很nice
num=100

hl参数是home language，母语，用en就行了，即英语
hl=en

google dork 内容，除了A-Za-z0-9以外，都进行url编码

# 检测流程

>html页面解析，提取出有效的url

html页面解析完毕，有效url为xx条，sleep 3秒，

开始进行存活检测

>对所有有效的url进行存活检测

存活检测完毕，xx条存活，xx条无法访问

开始进行漏洞检测

>对存活url进行漏洞检测

漏洞检测完毕，xx条存在漏洞，xx条没有漏洞

>将检测结果写入vuln文件

检测结果保存为vuln文件
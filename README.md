# google-hacker-est

``个人兴趣项目，VScode下调试使用，非开箱即用``

根据google hack语法，获取大量目标，然后逐个验证漏洞存在与否，用于批量~~拿站~~安全测试

就目前来说，这并不是一款开箱即用的工具，我也是处于自己的需要才开发的，目前才刚刚起步，因此，如果感兴趣不妨先star一个

哦对了，说一句，这个工具仅用于安全研究，任何人或组织使用这个本项目提供的工具及功能造成的任何后果作者本人不予承担。

简单说下思路，要想避开google对爬虫的检查，只能慢，否则就是429警告！

我曾经在5秒内连续请求了两次，就被封了一下午

通过ua和domain随机的方式，可以一定程度上改善这种境况

但仍建议不论请求是否成功，每次都要sleep 50秒以上(这个速度是最保险的，也可以根据实际情况适当降低sleep)

第二页的参数是start=10，第三页的参数是start=20，以此类推
https://www.google.com.hk/search?q=python&start=10

num参数是返回数量，默认为10，设为100时将会返回100条数据，很nice
num=100

hl参数是home language，母语，用en就行了，即英语
hl=en

google dork 内容，除了A-Za-z0-9以外，都进行url编码

# 目录结构

/_init ------ 临时文件及扫描结果report文件存放处  
/core ------- 核心功能   
/payload ---- 各种漏洞验证及利用插件脚本   
/data ------- 一些必要的数据  
/doc -------- 实验用的无用数据  
/readme.md -- 本文  
/main.py ---- 入口文件  


# 开发心路

【 WARNING 】因为我用的是买的vpn，应该有不同的人在用同一个IP作为出口，所以即使我已经很慢了，也做好了一些随机操作，通过google search时也是很玄学的，百分之七十的概率会遭遇到429，非常搞心态，所以暂时调整策略，利用返回数量可定义，手动在浏览器上获取两百条返回结果，然后将html源码交给google_core模块解析并返回url，然后用payload模块去批量验证

暂时并不打算处理vpn这个问题(因为如果要自己搭建vpn的话就要搞信用卡、VISA、然后VPS一通倒腾调配，可能两天时间就没了，反正我现在是没这个心气儿了，换作以前可能会折腾一下，而且以前用同事自己搭的VPN说实话很不稳定，再观望吧，能用就行不是么，人生苦短)，因为google search的功能其实我已经写好了，而且也实验多次证明功能可用，有兴趣的可以看一下然后稍微调整一下即可(可能也不用调整)，就几个核心函数，被我注释掉了而已

接下来可能就是扩充一些payload脚本吧，多支持一些，批量拿站还是蛮爽的，我主要会做一些RCE漏洞的利用脚本，利用起来简单直接


【 INFO 】昨天简单写了个tomcat 的put任意文件上传，在今天下午测试完以后，意外的意识到之前先批量存活检测再漏洞检测的路子其实有点蠢，因为这意味着我要等很久才能得到漏洞信息，不妨稍微改动一下，在将页面存活的动作放到漏洞验证模块里面去，如果存活，就进一步scan，如果无响应，直接pass，这样的好处就是我能实时看到那些漏洞有漏洞或没漏洞

【 INFO 】2020.12.18 昨晚把log和之前说的单条存活+漏洞验证的模式都实现了，并且测试完毕，之前目录结构也比较混乱，包括模块的路径等等，现在其实也不行，因为像request/log这些最好是能定制一下，单独做成一个模块，统一配置，要不然每写一个payload都要单独配置，例如timeout、user-agent这些（这还不是最糟糕的，最糟的是有的想起来写，有的没想起来），每次都要写一遍给我累完了，之前就看jexboss、xsstrike他们都是这么搞得

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


# 参考

[对于 Python 抓取 Google 搜索结果的一些了解](https://juejin.cn/post/6844903750939705357)

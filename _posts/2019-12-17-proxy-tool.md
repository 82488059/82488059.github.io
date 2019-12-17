---
layout: post
title:  "python写的爬取与测试代理IP工具"
categories: shell
tags: proxy python tool
author: flame
description: python写的爬取与测试代理IP工具
---


[p1]:/assets/images/post/2019-12-17-proxy-tool/1.png

![p1][p1]

Multirun是多线程相关代码。

Task是任务封装。

MultiTaskRun.py是线程启动与任务封装。

主要业务相关代码在Proxy中。
conf.py是数据库配置。
db_public.py是数据查询与写入的代码。
Pool是池子，主要用于减少数据库连接与断开的次数。
Http.py简易的封装了http请求，使用起来方便一些。
Proxy.py主要是各个代理网站的爬取方式。

proxy2.sql是数据库结构。

项目从RunProxy.py启动
```py
if __name__ == "__main__":
    # 对已有的IP进行测试
    q = db_public.get_proxy2_ip_queue()
    MultiTaskRun.multi_thread_run_base_task(q, test_proxy, 4 * cpu_count())

    # 找新的IP并入库
    q = queue.Queue()
    tn = 6  # type
    for x in range(0, tn):
        q.put(x)
    MultiTaskRun.multi_thread_run_base_task(q, find_new_proxy, tn)
```

git 地址：[https://github.com/82488059/Proxy](https://github.com/82488059/Proxy)

git 地址：[git@gitee.com:user.zt/Proxy.git](git@gitee.com:user.zt/Proxy.git)



`注意conf.py并没有上传到git，下面是conf.py的代码。conf.py位于Proxy文件夹下。`
conf.py
```py
#!/usr/bin/python3
# -*- coding: utf-8 -*-
db_charset = 'utf8'
db_public = 'dbname'
db_public_host = '127.0.0.1'
db_public_user_name = 'root'
db_public_user_pwd = 'pwd'
db_port = 3306
```




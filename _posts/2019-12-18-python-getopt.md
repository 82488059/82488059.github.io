---
layout: post
title:  "python中使用getopt分析命令行参数"
categories: shell
tags: getopt python
author: flame
description: python中使用getopt分析命令行参数的用法
---

### 1、命令行参数获取方法使用sys.argv
test.py
```py
#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys

if __name__ == "__main__":
    for i in range(len(sys.argv)):
        print(sys.argv[i])
```
执行
```
python t1.py 1 2
```
输出：
```
test.py
1
2
```
sys.argv第一个是脚本路径，剩下的是命令行参数。

### 2、getopt用法 

```py
#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import getopt


if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hi:p:t:v", ["help", "ip=", "port=", "version"])
    except getopt.GetoptError:
        # 解析出错的时候走这里
        print('test.py -h to help')
        exit(1)

    # print(args)
    if not opts:
        # 没有解析到参数时走这里
        print('test.py -h to help')
        exit(1)
    # 打印解析到的内容
    print(opts)
    ip = None
    port = None
    types = None
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('test.py -i <ip> -p <port> -t <m1|m2>')
            sys.exit(0)
        if opt in ("-i"):
            ip = arg
        if opt in ("-p", "--ip"):
            port = arg
        if opt in ("-t"):
            types = arg
        if opt in ("-v"):
            print("version 0.0.0.0")
            exit(1)

    print("master ip {}, port {}, type {}.".format(ip, port, types))
```



在`"hi:p:t:v"`中字母后面没有:的表示没有值。例如`i:`表示i后面有值`v`表示v后面没有值。




---
layout: post
title:  "python中使用getopt分析命令行参数"
categories: shell
tags: python
author: flame
description: python中使用getopt分析命令行参数的用法
---

### 说明：
getopt.getopt(args,shortopts,longopts = [])

`args`是要解析的参数列表(不包括程序启动路径)，通常是sys.argv[1:]。  
`shortopts`是脚本要识别的选项字母字符串，其中的选项需要一个参数，后接一个冒号。   
`longopts`(如果已指定)必须是包含应支持的long选项名称的字符串列表。`'--'`选项名称中不应包含前导字符。需要参数的长选项应后跟等号(`'='`)。不支持可选参数。要仅接受长选项，shortopts应该为空字符串。


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
python test.py 1 2
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
        opts, args = getopt.getopt(sys.argv[1:],"-h-i:-p:-t:-v", ["help", "ip=", "port=", "types=", "version"])
    except getopt.GetoptError:
        print('test.py -h to help')
        exit(1)

    print(opts)
    # print(args)
    if not opts:
        print('test.py -h to help')
        exit(1)

    ip = None
    port = None
    types = None
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('test.py -i <ip> -p <port> -t <m1|m2>')
            sys.exit(0)
        if opt in ("-i", "--ip"):
            ip = arg
        if opt in ("-p", "--port"):
            port = arg
        if opt in ("-t", "--types"):
            types = arg
        if opt in ("-v"):
            print("version 0.0.0.0")
            exit(1)

    print("master ip {}, port {}, type {}.".format(ip, port, types))
```

在`"hi:p:t:v"`中字母后面没有:的表示没有值。例如`i:`表示i后面有值，`v`表示v后面没有值。  
`"hi:p:t:v"`也可以写成`"-h-i:-p:-t:-v"`的形式。

输入：
```py
python test.py --ip=111 -p a
```

输出：
```py
[('--ip', '111'), ('-p', 'a')]
master ip 111, port a, type None.
```

参考：  
[https://docs.python.org/3/library/getopt.html](https://docs.python.org/3/library/getopt.html)
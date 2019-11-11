---
layout: post
title:  "centOS7.3忘记密码CentOS7.3重置修改root密码centos7破解密码"
categories: tool
tags: linux 
author: other
description: centOS7.3忘记密码CentOS7.3重置修改root密码centos7破解密码
---

1、机进入启动界面，开机进入启动界面后，要按照屏幕的下方的操作提示迅速按下e键，进入编辑页面。动作要快点,否则5秒就会开始自动进入启动页面了。

[1]:/assets/images/post/2019-11-11-Centos7-forgot-posswork/1.jpg "启动界面"

![1][1]


2、然后，在这个页面，找到linux16这一行，将之前的ro，改为rw init=sysroot/bin/sh，然后按ctrl+x，进入单用户模式.由于是单用户,就不需要密码进入了：

[2.1]:/assets/images/post/2019-11-11-Centos7-forgot-posswork/2.1.png "单用户模式"

![2.1][2.1]


[2.2]:/assets/images/post/2019-11-11-Centos7-forgot-posswork/2.2.png "单用户模式"

![2.2][2.2]


3、输入命令chroot /sysroot，也就是改变程序执行时所参考的根目录位置,根目录改为/sysroot。然后输入命令passwd root


[3]:/assets/images/post/2019-11-11-Centos7-forgot-posswork/3.png "3"

![3][3]



4、输入命令touch /.autorelabel ,在/目录下创建一个.autorelabel文件，而有这个文件存在，系统在重启时就会对整个文件系统进行relabeling。然后命令exit退出，再命令reboot重启：

[4]:/assets/images/post/2019-11-11-Centos7-forgot-posswork/4.png "4"

![4][4]


reboot重启后自动修改密码，修改成功后系统会再次重启，就可以输入root和新密码，重新登录了。

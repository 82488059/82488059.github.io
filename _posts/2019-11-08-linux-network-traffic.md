---
layout: post
title:  "Linux服务器上监控网络带宽的18个常用命令和linux带宽流量监控查看工具"
categories: tool
tags: linux network
author: flame
description: 记录一下Linux服务器上监控网络带宽的18个常用命令和linux带宽流量监控查看工具。
---
[nload]:/assets/images/post/2019-11-08-linux-network-traffic/nload.jpg "nload"

 这些工具使用不同的机制来制作流量报告。nload等一些工具可以读取"proc/net/dev"文件，以获得流量统计信息；而一些工具使用pcap库来捕获所有数据包，然后计算总数据量，从而估计流量负载。

下面是按功能划分的命令名称。

监控总体带宽使用――nload、bmon、slurm、bwm-ng、cbm、speedometer和netload
监控总体带宽使用（批量式输出）――vnstat、ifstat、dstat和collectl
每个套接字连接的带宽使用――iftop、iptraf、tcptrack、pktstat、netwatch和trafshow
每个进程的带宽使用――nethogs

1. nload
</br>
![nload][nload]


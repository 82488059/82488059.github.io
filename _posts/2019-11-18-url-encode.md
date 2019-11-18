---
layout: post
title:  "服务端文件路径拼接url地址时一定要注意encode"
categories: programming
tags: 吐槽 
author: flame
description: 服务端读取文件路径并拼成URL路径的时候一定要注意对路径URLENCODE
---


搭建的http文件服务器。http地址由服务端拼接，然而web开发竟然忘记了encode，导致上线后某些文件不能预览（手动滑稽）。

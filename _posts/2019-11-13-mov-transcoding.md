---
layout: post
title:  "mov转码使用"
categories: programming
tags: av 
author: flame
description: mov转码中遇到的问题
---

使用vlc不能播放mac生成的mov格式视频。

使用VLC转码生成的视频只有1秒。转码不成功。
使用ffmpeg转码
1、视频编码格式h264音频复制。转码的视频QuickTimePlayer不能播放。
2、视频使用mpeg4音频复制。转码的视频QuickTimePlayer能正常播放。

参考：
1、[FFmpeg](http://ffmpeg.org/ffmpeg.html)

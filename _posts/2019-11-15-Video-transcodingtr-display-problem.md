---
layout: post
title:  "Display resolution is different from video resolution"
categories: programming
tags: ffmpeg av  
author: flame
description: 视频转码后播放分辨率与转码分辨率不同
---
问是这样的，有一批竖版(408\*720)视频全部转码为横版(720\*480)视频,播放的时候一部分横版显示，一部分是竖版显示。

使用VLC查看分辨率都是720*480。

使用ffprobe查看原视频信息

[charts]:/assets/images/post/2019-11-15-Video-transcodingtr-display-problem/1.jpg "charts" 
![charts][charts]

发现有[SAR[^脚注1] 1:1 DAR[^脚注2] 17:30]

播放器会根据DAR来显示视频，在没有DAR参数时会根据视频分辨率来显示视频，所以视频转为横版的时候需要删除DAR信息或者修改DAR信息，才能使播放时为横版。



[^脚注1]: SAR - storage aspect ratio就是对图像采集时，横向采集与纵向采集构成的点阵，横向点数与纵向点数的比值。比如VGA图像640/480 = 4:3，D-1 PAL图像720/576 = 5:4

[^脚注2]: DAR - display aspect ratio就是视频播放时，我们看到的图像宽高的比例，缩放视频也要按这个比例来，否则会使图像看起来被压扁或者拉长了似的。


PAR - pixel aspect ratio（可以理解为单个像素的宽高比）大多数情况为1:1,就是一个正方形像素，否则为长方形像素。常用的PAR比率(1:1，10:11, 40:33, 16:11, 12:11 ).

SAR - storage aspect ratio就是对图像采集时，横向采集与纵向采集构成的点阵，横向点数与纵向点数的比值。比如VGA图像640/480 = 4:3，D-1 PAL图像720/576 = 5:4

DAR - display aspect ratio就是视频播放时，我们看到的图像宽高的比例，缩放视频也要按这个比例来，否则会使图像看起来被压扁或者拉长了似的。

这三者的关系PAR x SAR = DAR或者PAR = DAR/SAR.







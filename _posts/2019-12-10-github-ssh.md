---
layout: post
title:  "TortriseGit使用key连接github"
categories: c++
tags: c++ 
author: flame
description: TortriseGit使用key连接github
---

### 1、使用PuTTYgen生成key

[PuTTYgen]:/assets/images/post/2019-12-10-github-ssh/1.png "PuTTYgen" 

![PuTTYgen][PuTTYgen]

点击Generate生成key(需要等一会，时间和机器配置成反比。)

[p2]:/assets/images/post/2019-12-10-github-ssh/2.png "PuTTYgen" 

![p2][p2]

生成后的效果

[p3]:/assets/images/post/2019-12-10-github-ssh/3.png "PuTTYgen" 

![p3][p3]

点击`Save public Key`保存公钥，点击`Save Private key`保存私钥。
可以在`Key passphrase`后面输入密码,在`confirm passphrase`后面确认密码，对私钥进行加密。

### 2、Github增加ssh key
点击右上角人物头像，选择Setting。

[Setting]:/assets/images/post/2019-12-10-github-ssh/4.png "Setting"  

![Setting][Setting]


进入设置页面后左侧选择SSH and GPG keys，进入配置界面。点击`New SSH key`。

[newssh]:/assets/images/post/2019-12-10-github-ssh/5.png "newssh"  

![newssh][newssh]

以文本方式打开私钥文件，复制私钥,只复制私钥内容，不复制头和

[key]:/assets/images/post/2019-12-10-github-ssh/6.png "key"  

![key][key]

在Github配置页面Title输入名字，Key先输入ssh-rsa 再粘贴key(因为GitHub不认识PuTTYgen生成的私钥格式所以修改为Github可以认识的格式)。
`注意 ssh-rsa 和key中间有一个空格`

[s7]:/assets/images/post/2019-12-10-github-ssh/7.png "s7"  

![s7][s7]

然后点击Add SSH key保存配置。之后输入github密码完成github配置。

完成后可以看到配置好的key。

[s8]:/assets/images/post/2019-12-10-github-ssh/8.png "s8"  

![s8][s8]



### 3、使用TortoiseGit克隆仓库

克隆Github上的代码，注意勾选加载Putty密钥。
URL是自己的代码库。
Putty密钥就是之前生成的私钥文件。
如果私钥加了密码开始克隆的时候会让输入私钥密码。


[s10]:/assets/images/post/2019-12-10-github-ssh/10.png "s10"  

![s10][s10]

克隆完成后配置TortoiseGit，配置好后就可以提交代码。

[s9]:/assets/images/post/2019-12-10-github-ssh/9.png "s9"  

![s9][s9]

### `注意: 远端的选项只有在受git版本控制的地方才有这个选项。`


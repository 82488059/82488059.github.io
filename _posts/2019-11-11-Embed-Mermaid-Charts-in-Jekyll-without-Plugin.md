---
layout: post
title:  "Embed Mermaid Charts in Jekyll without Plugin"
categories: tool
tags: Jekyll 
author: Kai Zhang
description: Embed Mermaid Charts in Jekyll without Plugin
---
转载自：
http://kkpattern.github.io/2015/05/15/Embed-Chart-in-Jekyll.html


# Embed Mermaid Charts in Jekyll without Plugin

##### May 15, 2015

Jekyll is a blog system with which you can use markdown to write your post. It’s a great tool for programers to write blogs, especially with [github](https://help.github.com/en/github/working-with-github-pages/setting-up-a-github-pages-site-with-jekyll). However markdown lacks of supportment for charts, which could be helpful for elaborating some concepts. Luckily there are some tools to make up this.

[Mermaid](http://knsv.github.io/mermaid/index.html) is a tool for users to create diagrams and flowcharts from text similiar to markdown. For example, the following text:

```
graph TD;
    A-->B;
    A-->C;
    B-->D;
    C-->D;
```
will be automatically transformed by mermaid into the following flowchart:

[charts]:/assets/images/post/2019-11-11-Embed-Mermaid-Charts-in-Jekyll-without-Plugin/charts.jpg "charts"

![charts][charts]


To do this, you only need to include mermaid on your web page:
```html
<script src="mermaid.full.min.js"></script>
```
Then define your chart like this:

```html
<div class="mermaid">
graph TD;
    A-->B;
    A-->C;
    B-->D;
    C-->D;
</div>
```
That’s all. And jekyll has a [plugin](https://github.com/jasonbellamy/jekyll-mermaid) to to simplify the creation of mermaid diagrams and flowcharts in your posts and pages. However, for safety reasons, if you want github automatically transform your post into web pages, you can’t use a plugin. So here I’ll show you how to make mermaid work in jekyll without plugin.

First, we need to [download](https://github.com/knsv/mermaid) the javascript code of mermaid. You can download the stable version by choosing the versioned branch in mermaid’s github page and download the mermaid.full.min.js file under the dist directory.

Then put the downloaded file in a directory named js in your jekyll project so the web page rendered by jekll can include this js file. Well other directories like css will also work, choose your favourite one.

Next, we will change the jekyll template to include the mermaid code. In the _includes directory there is a file named “head.html”. Content in this file will be include in the head section of every page rendered by jekyll. It’s a perfect place for us to include mermaid code. Add the following content in this file:


```html 
<script src="/js/mermaid.full.min.js"></script>
```

After this, we can create diagrams and flowcharts with mermaid in jekyll. However, even though mermaid’s syntax is similar to markdown, it’s not. And the chart definition need to be in a div whose class is “mermaid”. Luckily, for those html elements that markdown doesn’t support, you can just write them directly in the markdown file. So now you can easily create charts in your jekyll blog and maintain them in git and even diff the charts. Have a nice day!
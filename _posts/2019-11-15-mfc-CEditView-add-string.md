---
layout: post
title:  "MFC CEditView 末尾增加文本"
categories: programming
tags: mfc windows  
author: flame
description: 记录一下如何在MFC CEditView末尾增加文本
---

## CEditView中使用CEdit作为编辑控件，所以可以通过CEdit的方法来改变CEditView中的文字。

## 取得CEdit的方法：

[bmp1]:/assets/images/post/2019-11-15-mfc-CEditView-add-string/1.jpg "bmp1" 
![bmp1][bmp1]

## GetEditCtrl的说明：

### CEditView:: GetEditCtrl
调用`GetEditCtrl`以获取对 "编辑" 视图使用的编辑控件的引用。
```
CEdit& GetEditCtrl() const;
```
#### 返回值

对`CEdit`对象的引用。

#### 备注

此控件的类型为[CEdit](https://docs.microsoft.com/zh-cn/cpp/mfc/reference/cedit-class?view=vs-2019), 因此可以使用`CEdit`成员函数直接操作 Windows 编辑控件。

实现代码如下： 

```c++
//  class CXXXView : public CEditView
int CXXXView::AddString(const CString & string)
{
    // CEditView::GetEditCtrl 提供对CEdit CEditView对象 (Windows 编辑控件) 的部分的访问。
    CEdit& thisEdit = GetEditCtrl();
    int nLength = thisEdit.GetWindowTextLength();
    // 选定当前文本的末端
    thisEdit.SetSel(nLength, nLength);
    // 追加文本
    thisEdit.ReplaceSel(string);
    return 0;
}
```

参考：

[Microsoft CEditView类说明文档](https://docs.microsoft.com/zh-cn/cpp/mfc/reference/ceditview-class?view=vs-2019)

[Microsoft CEdit类说明文档](https://docs.microsoft.com/zh-cn/cpp/mfc/reference/cedit-class?view=vs-2019)





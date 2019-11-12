---
layout: post
title:  "在多文档界面中创建文档并修改标题名"
categories: programming
tags: mfc c++ 
author: flame
description: 在app的OnFileNew中创建Doc并修改标题
---

创建文档模板代码。

```c++
    // create doc template
	CMultiDocTemplate* pDocTemplate;
	pDocTemplate = new CMultiDocTemplate(IDR_TYPE,
		RUNTIME_CLASS(CXXDoc),
		RUNTIME_CLASS(CChildFrame), // 自定义 MDI 子框架
		RUNTIME_CLASS(CXXView));
	if (!pDocTemplate)
		return FALSE;
    // add doc template
	AddDocTemplate(pDocTemplate);
```

创建Doc并加入DocManager

```c++
void CXXApp::OnFileNew()
{
    if (NULL == m_pDocManager)
        return;
    // first template position 
    POSITION posTemplate =  m_pDocManager->GetFirstDocTemplatePosition();
    // if NULL no template
    if (NULL == posTemplate)
    {
        return;
    }
    // first template 
    CDocTemplate* pTemplate = m_pDocManager->GetNextDocTemplate(posTemplate);
    if (!pTemplate)
        return;
    // create new doc and add to manager
    CDocument* pDoc = pTemplate->OpenDocumentFile(NULL);
    if (!pDoc)
    {
        return;
    }
    // set doc title 
    pDoc->SetTitle(_T("127.0.0.1"));

    // unnecessary
    // Test is not the first document
    POSITION posDoc =  pTemplate->GetFirstDocPosition();
    if (posDoc)
    {
        auto p = pTemplate->GetNextDoc(posDoc);
        if (p == pDoc)
        {
            TRACE(_T("new doc title is %s\n"), p->GetTitle());
        }
        else
        {
            TRACE(_T("first doc title is %s\n"), p->GetTitle());
            TRACE(_T("new doc title is %s\n"), pDoc->GetTitle());
        }
    }
    // unnecessary
}
````



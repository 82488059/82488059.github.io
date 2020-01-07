---
layout: post
title:  "MFC对话框程序中创建托盘图标"
categories: MFC
tags: MFC 
author: flame
description: 记录MFC对话框程序中创建托盘图标的方法
---


### 1.在对话框类头文件中声名变量和函数。
```c++
class CXXDlg{
    // 原类中的代码...
private:
    // 托盘图标用到的变量
    NOTIFYICONDATA m_notifyIconData{ 0 };
public:
    // 初始化m_notifyIconData
    BOOL InitNotifyIcon();
    // 控制显示/隐藏托盘图标
    BOOL ShowNotifyIcon(BOOL bShow);
    // 托盘图标回调函数
    afx_msg LRESULT NotifyIconCallBack(WPARAM wParam, LPARAM lParam);
};
```
### 2.在cpp文件中定义函数
```c++
BOOL CXXDlg::InitNotifyIcon()
{
    // Add a Shell_NotifyIcon notificaion
    m_notifyIconData.cbSize = sizeof(m_notifyIconData);
    // 图标ID
    m_notifyIconData.uID = IDR_MAINFRAME;
    m_notifyIconData.uFlags = NIF_ICON | NIF_MESSAGE | NIF_TIP;
    m_notifyIconData.hIcon = LoadIcon(AfxGetInstanceHandle(), MAKEINTRESOURCE(IDR_MAINFRAME));
    // 这里是定义的消息ID
    m_notifyIconData.uCallbackMessage = WM_NOTIFY_MESSAGE;
    lstrcpy(m_notifyIconData.szTip, _T("XX"));
    m_notifyIconData.hWnd = m_hWnd;
    // 增加图标到托盘
    // Shell_NotifyIcon(NIM_ADD, &m_notifyIconData);
    // 更新图标的代码
    // m_notifyIconData.uFlags = NIF_ICON;
    // m_notifyIconData.hIcon = LoadIcon(g_hInstance, MAKEINTRESOURCE(IDR_MAINFRAME));
    return 0;
}

BOOL CXXDlg::ShowNotifyIcon(BOOL bShow)
{
    BOOL bResult = FALSE;
    if (bShow)
    {
        bResult = Shell_NotifyIcon(NIM_ADD, &m_notifyIconData);
    }
    else
    {
        bResult = Shell_NotifyIcon(NIM_DELETE, &m_notifyIconData);
    }
    return bResult;
}

LRESULT CXXDlg::NotifyIconCallBack(WPARAM wParam, LPARAM lParam)
{
    UINT uID{ wParam };
    UINT uMouseMsg{ (UINT)lParam };

    switch (uMouseMsg)
    {
    // 在托盘图标上抬起右键
    case WM_RBUTTONUP:
    {
        NotifyIconMesgRestore(0, 0);
    }
    break;
    // 在托盘图标上抬起左键
    case WM_LBUTTONUP:
    {
        NotifyIconMesgRestore(0, 0);
    }
    break;
    default:
    {
    }
    break;
    }
    return LRESULT();
}
// 还原窗口
LRESULT CXXDlg::NotifyIconMesgRestore(WPARAM wParam, LPARAM lParam)
{
    // 还原到其原始大小并显示窗口
    ShowWindow(SW_SHOWNORMAL);
    // 置顶窗口
    ::SetWindowPos(m_hWnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOSIZE | SWP_NOMOVE);
    // 删除托盘图标
    ShowNotifyIcon(FALSE);
    return LRESULT();
}
```
### 3.定义WM_NOTIFY_MESSAGE并在消息映射表中增加映射
```c++
// 定义一个在项目中独一无二的宏。消息ID
#define WM_NOTIFY_MESSAGE WM_USER + 101

BEGIN_MESSAGE_MAP(CXXDlg, CDialogEx)
	ON_WM_SYSCOMMAND()
	ON_WM_PAINT()
	ON_WM_QUERYDRAGICON()
    ON_WM_SIZE()
    ON_WM_DESTROY()
    // 增加的映射 
    ON_MESSAGE(WM_NOTIFY_MESSAGE, NotifyIconCallBack)
END_MESSAGE_MAP()
```

### 4.增加Onsize并在OnSize中增加最小化时创建托盘图标和隐藏窗口的代码。
```c++
void CXXDlg::OnSize(UINT nType, int cx, int cy)
{
    CDialogEx::OnSize(nType, cx, cy);

    // TODO: 在此处添加消息处理程序代码

    if (SIZE_MINIMIZED == nType)
    {
        // 最小化时创建托盘图标
        ShowNotifyIcon(TRUE);
        // 隐藏窗口
        ShowWindow(SW_HIDE);
    }
}
```
### 5.参考
Shell_NotifyIcon [https://docs.microsoft.com/en-us/previous-versions/aa922175(v=msdn.10)](https://docs.microsoft.com/en-us/previous-versions/aa922175(v=msdn.10))




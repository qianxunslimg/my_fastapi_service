---
date: '2021-12-02T19:36:20+08:00'
---

首先 pro：

```c++
LIBS +=User32.LIB


main.cpp：
#include "hooktest.h"
#include "ui_hooktest.h"
#include <QDebug>

LRESULT CALLBACK keyProc(int nCode, WPARAM wParam, LPARAM lParam);

HHOOK keyHook=NULL;
WPARAM lastkey=0;
QString lastStr;

int starthook();
HookTest::HookTest(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::HookTest)
{
    ui->setupUi(this);
        keyHook = SetWindowsHookEx(WH_KEYBOARD_LL, keyProc, GetModuleHandle(NULL), 0);

        MSG msg = { 0 };
        while (GetMessage(&msg, NULL, 0, 0)) {  //WM_QUIT消息 退出
        //将虚拟键消息转换为字符消息,虚拟键值                `
        //VK_UP,VK_DOWN
        TranslateMessage(&msg);
        //将消息分发给窗口处理函数
        DispatchMessage(&msg);
        }
}

HookTest::~HookTest()
{
    delete ui;
}

LRESULT CALLBACK keyProc(int nCode, WPARAM wParam, LPARAM lParam){
    PKBDLLHOOKSTRUCT key = (PKBDLLHOOKSTRUCT)lParam;
    qDebug()<<key->vkCode<<endl;
    return CallNextHookEx(keyHook, nCode, wParam, lParam);
}
```

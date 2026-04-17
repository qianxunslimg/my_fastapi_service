---
date: '2021-12-02T19:34:56+08:00'
tags:
- 开发随笔
---

# [windows API关闭exe](https://www.cnblogs.com/qianxunslimg/p/14351941.html)

可以直接使用的函数 做个备份 只需要输入要关闭的文件名就好了

```c++
#include <Windows.h>
#include <Tlhelp32.h>
#include <stdio.h>
#include <winnt.h>
 
void terminateSuwellReader(const char* str)
{
    HANDLE hSnapShot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS,0);
 
    //现在我们获得了所有进程的信息。
    //将从hSnapShot中抽取数据到一个PROCESSENTRY32结构中
    //这个结构代表了一个进程，是ToolHelp32 API的一部分。
    //抽取数据靠Process32First()和Process32Next()这两个函数。
    //这里我们仅用Process32Next()，他的原形是：
    //BOOL WINAPI Process32Next(HANDLE hSnapshot,LPPROCESSENTRY32 lppe);
    //我们程序的代码中加入：
    PROCESSENTRY32* processInfo=new PROCESSENTRY32;
    // 必须设置PROCESSENTRY32的dwSize成员的值 ;
    processInfo->dwSize=sizeof(PROCESSENTRY32);
    int index=0;
    //这里我们将快照句柄和PROCESSENTRY32结构传给Process32Next()。
    //执行之后，PROCESSENTRY32 结构将获得进程的信息。我们循环遍历，直到函数返回FALSE。
    int ID = 0;
    while(Process32Next(hSnapShot,processInfo)!=FALSE)
    {
        index++;
        int size=WideCharToMultiByte(CP_ACP,0,processInfo->szExeFile,-1,NULL,0,NULL,NULL);
        char *ch=new char[size+1];
        if(WideCharToMultiByte(CP_ACP,0,processInfo->szExeFile,-1,ch,size,NULL,NULL))
        {
            //使用这段代码的时候只需要改变"cmd.exe".将其改成你要结束的进程名就可以了。
            if(strstr(ch,str))
            {
                ID = processInfo->th32ProcessID;
                HANDLE hProcess;
                // 现在我们用函数 TerminateProcess()终止进程，这里我们用PROCESS_ALL_ACCESS
                hProcess=OpenProcess(PROCESS_ALL_ACCESS,TRUE,ID);
                TerminateProcess(hProcess,0);
                CloseHandle(hProcess);
            }
        }
    }
    CloseHandle(hSnapShot);
    delete processInfo;
}
 
int main(){
    terminateSuwellReader("SuwellReader.exe");
    return 0;
}
```

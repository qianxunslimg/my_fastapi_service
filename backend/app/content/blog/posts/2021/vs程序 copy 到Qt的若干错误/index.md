---
date: '2021-10-02T19:37:11+08:00'
tags:
- 开发随笔
---

# [vs程序 copy 到Qt的若干错误](https://www.cnblogs.com/qianxunslimg/p/14347565.html)

打杂人的苦恼：

- 发票太多ofd的 sunny只要pdf的 ofd只能用某个国产软件打开
- 某国产软件过于拉跨，无法直接转为pdf 只能认为截图 word 另存为...
- ofd的编码格式搞清楚有点费劲 但是想到了一个笨方法
  1. 调用某软件打开ofd文档
  2. 整体截图 使用opencv提取roi为发票区域
  3. 基于QT强大的模块化能力 直接存储为pdf



唉 在vs下学习了一些基础的操作 打算到qt下编写（当时还没有用qtvstools），不熟悉qtCreator 出现了一些问题

#### 菜归菜，还是学到一些东西

1. 首先是windows.h在qt下的使用  LIBS +=User32.LIB

2. 离谱的 dependent error .h does not exist  

   看网上说的是.pro文件存在缓存？解决方案：瞎jb乱摁

   通过以下步骤乱搞：

   ​	   （1）ctrl A ctrlX .pro文件，编译，ctrl v编译

   ​		（2）删除相关头文件及代码的使用，重新添加并编译（傻逼操作）

3. 无法解析的外部符号 __imp_DeleteObject 等等， 解决方法

　　#pragma comment(lib, "Gdi32.lib")

4. Cmd命令无法进行直接调用  system("start C:\\Users\\00\\Desktop\\发票\\1.24-\\思巴克72.ofd");

   解决方法：使用QProcess运行cmd命令  https://blog.csdn.net/vample/article/details/78872587

啊呸，直接打开文件搞什么逼逼赖赖

```c++
QString fileName = "C:\\Users\\00\\Desktop\\发票\\1.24-\\思巴克72.ofd";
QFile file(fileName);
if(file.exists()){
    QDesktopServices::openUrl(QUrl::fromLocalFile(fileName));
}
```

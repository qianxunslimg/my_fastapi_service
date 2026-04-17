---
date: '2021-12-02T19:17:36+08:00'
---

## 1.发布release版本的QT程序

　　在build release文件夹内找到exe文件，将其单独放在一个自建的空文件夹内

![](./assets/2092994-20200927165117303-604984762-2.png)

![](./assets/2092994-20200927165455009-910788885-2.png)

&nbsp;

&nbsp;

&nbsp;

## &nbsp;2.cd到含exe的空文件夹

　　在QT命令行cd到含exe的空文件夹，cd /d E:\QDIR

![](./assets/2092994-20200927165604874-1233279110-2.png)![](./assets/2092994-20200927165951305-446477392-2.png)

## 3.使用windeployqt.exe进行打包

首先找到windeployqt.exe的路径&nbsp;

&nbsp;![](./assets/2092994-20200927170127591-1210427907-2.png)

&nbsp;

&nbsp;

输入命令D:\QT\5.14.2\msvc2017_64\bin\windeployqt&nbsp;QDIR.exe即完成了打包

![](./assets/2092994-20200927170421891-1644738339-2.png)![](./assets/2092994-20200927170550570-2063963822-2.png)

&nbsp;

## &nbsp;附：打包前修改exe图标

## 改变exe的图标

1、下载一个.ico格式的图标（如：bucket and shovel.ico），将bucket and shovel.ico复制到工程目录下。

![](./assets/2092994-20200927172502714-1388114573-2.png)

&nbsp;

&nbsp;

2、工程目录下新建一个空白txt文档，文档内添加如下内容
`IDI_ICON1 ICON DISCARDABLE "bucket and shovel.ico"`
3、将文档后缀修改为.rc（如：bucke.rc, !!注意!!rc文件名不要含空格）&nbsp;
4、在工程的pro文件添加如下内容
`RC_FILE = bucket.rc`
5、重新编译程序，即可发现生成的程序图标变成了bucket.ico

![](./assets/2092994-20200927172701527-227417489-2.png)

&nbsp;

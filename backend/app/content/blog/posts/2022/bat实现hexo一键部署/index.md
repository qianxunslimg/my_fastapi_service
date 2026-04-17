---
date: '2022-04-19T15:41:00+08:00'
tags:
- 开发随笔
---

#### 起因

个人有每天凌晨更新所有博客的习惯，流程繁琐如下

1. 从多个文件夹中拷贝所有markdown到指定的文件夹
2. 该目录下运行cmd
3. 执行hexo g生成html 然后漫长的等待 执行完成后 hexo d部署到远端 然后又是漫长的等待

不堪折磨，粗略学了下脚本语言，简单实现了博客一键更新部署的功能

#### 实现

```bash
@echo off
%color 4A%
echo 自动远端部署开始。。。
%注意有中文路径 则必须使用ANSI编码 && 表示前面执行成功 后面再执行%
copy C:\Users\qianxunslimg\Desktop\myMD\算法\*.md D:\MyBlog\source\_posts
copy C:\Users\qianxunslimg\Desktop\myMD\面试\*.md D:\MyBlog\source\_posts
copy C:\Users\qianxunslimg\Desktop\myMD\开发随笔\*.md D:\MyBlog\source\_posts
echo 拷贝工作完成。。。"
cd d: 
cd D:\MyBlog
hexo g && hexo d && echo 自动部署完成。。。 && color 20 && pause > nul
```

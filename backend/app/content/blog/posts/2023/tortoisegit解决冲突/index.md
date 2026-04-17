---
date: '2023-04-12T23:43:00+08:00'
tags:
- 开发随笔
---

之前开发虽然使用了git但只是当作备份 和版本管理，很少进行多人多线开发，偶尔设计也只是手动进行合并，解决冲突，参考[git 使用 tortoisegit 解冲突 - J.晒太阳的猫 - 博客园 (cnblogs.com)](https://www.cnblogs.com/jasongrass/p/11199039.html)学习一下tortoisegit快速解决冲突和分支合并。

## `冲突示例1` 多人单分支提交

- 仓库初始状态

![image-20230412213907952](./assets/image-20230412213907952-2.png)

- 此时开发者1和开发者2在此基础上 对分支进行修改：

- 开发者1修改 并提交->push到远端

<img src="./assets/image-20230412214217616-2.png" alt="image-20230412214217616" style="zoom:50%;" />

![image-20230412214854059](./assets/image-20230412214854059-2.png)

- 开发者2修改 并提交

<img src="./assets/image-20230412220053802-2.png" alt="image-20230412220053802" style="zoom: 50%;" />

- push到远端时，会报错，

<img src="./assets/image-20230412214453352-2.png" alt="image-20230412214453352" style="zoom: 50%;" />

- 此时需要pull远端版本 并解决冲突。

<img src="./assets/image-20230412215022516-2.png" alt="image-20230412215022516" style="zoom: 50%;" />

- 双击冲突文件(注意，不是点确定)

<img src="./assets/image-20230412220635264-2.png" alt="image-20230412220635264" style="zoom:50%;" />

- 不知道为啥初始化的第一行 剪掉了 直接修改已合并的版本

<img src="./assets/image-20230412220726958-2.png" alt="image-20230412220726958" style="zoom:50%;" />

- 重新进行提交和push  合并成功

![image-20230412220954242](./assets/image-20230412220954242-2.png)

## `冲突示例2` 多人多分支合并

- 在gitee上新建仓库，从master分支拷贝一个分支，dev2 和 dev3分别对两个分支进行修改

![image-20230412221709891](./assets/image-20230412221709891-2.png)

- dev2对master的修改

<img src="./assets/image-20230412221630666-2.png" alt="image-20230412221630666" style="zoom:50%;" />



- dev3对feature_dev3的修改

<img src="./assets/image-20230412221753183-2.png" alt="image-20230412221753183" style="zoom:50%;" />

- dev2提交并push到master 代表其他开发人员的进度更新

<img src="./assets/image-20230412221857979-2.png" alt="image-20230412221857979" style="zoom:50%;" />

- dev3提交并push到feature_dev3 代表当前开发者的进度完成

<img src="./assets/image-20230412222047860-2.png" alt="image-20230412222047860" style="zoom:50%;" />

- 将dev3开发的功能合并到master分支

- 直接切换到目标分支master，同步进行pull，右键选择合并

<img src="./assets/image-20230412223353585-2.png" alt="image-20230412223353585" style="zoom:50%;" />

- 解决冲突

<img src="./assets/image-20230412223440687-2.png" alt="image-20230412223440687" style="zoom:50%;" />

- 修改冲突文件

<img src="./assets/image-20230412223531914-2.png" alt="image-20230412223531914" style="zoom:50%;" />

- 提交并push到远端

![image-20230412223737578](./assets/image-20230412223737578-2.png)

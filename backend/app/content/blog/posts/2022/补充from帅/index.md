---
date: '2022-03-16T09:46:00+08:00'
categories:
- 基础知识
tags:
- 面试
password: '87654123'
---

## Linux内核

主要由5部分组成：

<img src="./assets/image-20220726211056086-2.png" alt="image-20220726211056086" style="zoom:50%;" />

- 进程调度（SCHED）

  > 进程调度负责控制系统中的多个进程对 CPU 的访问，实现多进程并发（分时复用）地执行
  >
  > - 进程的描述
  >
  >   - 在Linux内核中，使用进程描述符task_struct来描述进程，该结构体描述的主要包括：
  >
  >     - 任务ID
  >
  >       <img src="./assets/d6c34678-25a7-42f9-9f0c-1793cfd036c5-17149424-2.jpg" alt="img" style="zoom:50%;" />
  >
  >     - 任务状态
  >
  >       其中状态state通过设置比特位的方式来赋值，具体值在include/linux/sched.h中定义
  >
  >       <img src="./assets/24953412-52a9-4bdf-af8b-71140777bebf-17149424-2.jpg" alt="img" style="zoom: 50%;" />
  >
  >     - 内存资源
  >
  >       <img src="./assets/8d887ca7-40fe-447a-b4c5-4eaec99de4d3-17149424-2.jpg" alt="img" style="zoom:50%;" />
  >
  >     - 文件与文件系统资源
  >
  >       <img src="./assets/1b551a4c-3988-4218-87ce-35fdbcfe77e9-17149424-2.jpg" alt="img" style="zoom:50%;" />
  >
  >     - tty资源
  >
  >     - 信号处理相关的数据结构
  >
  >       <img src="./assets/d8b4a8d3-5e61-4cf5-99eb-c3d190ca7787-17149424-2.jpg" alt="img" style="zoom:50%;" />

- 内存管理（MM）

  > - 虚拟内存与页表（内存分页）
  >
  >   <img src="./assets/c3c81bc5-8a5b-4ed8-bdc1-ec139e4d92cb-17149424-2.jpg" alt="img" style="zoom:50%;" />

- 虚拟文件系统（VFS）

  > <img src="./assets/image-20220726211603205-2.png" alt="image-20220726211603205" style="zoom:50%;" />

- 网络接口（NET）

  > <img src="./assets/image-20220726211615168-2.png" alt="image-20220726211615168" style="zoom:50%;" />
  >
  > 网络接口提供了对各种网络标准的存取和各种网络硬件的支持。如上所示，在Linux中网络接口可分为网络协议和网络驱动程序，网络协议部分负责实现每一种可能的网络传输协议，网络设备驱动程序负责与硬件设备通信，每一种可能的硬件设备都有相应的设备驱动程序。

- 进程间通信（IPC）

## 常用的寄存器

<img src="./assets/image-20220726212511499-2.png" alt="image-20220726212511499" style="zoom:150%;" />

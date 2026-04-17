---
date: '2023-04-23T23:43:00+08:00'
tags:
- 自驾相关
---

按照大佬的教程配置

> 1. [配置CLion用于STM32开发【优雅の嵌入式开发】 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/145801160)
> 2. [Docs (feishu.cn)](https://uk0mjrsnkf.feishu.cn/docx/doxcnUbs3RJby8CxKHYOh3nSi3f)

但是有几个注意问题记录一下

1. STM32CubeMX版本不能过高，不然不支持sw4stm32
2. OpenOCD的解压存放路径不能有空格，不然无法编译
3. STM32CubeMX配置芯片时需要ctrl+s保存，不然生成代码之后还是无法更新，仍是之前的默认芯片
4. Toolchains中有两种可选配置：
   1. C和C++编译器选择arm-none-eabi的, 调试器选择捆绑gdb(bundled gdb)
   2. C和C++编译器默认(cmake决定)，调试器选择arm-none-eabi的，但是注意此时run的OCD配置中也要选择arm-none-eabi的gdb
5. debug调试默认编译器优化选项为-Og -g，将`add_compile_options(-Og -g)`修改为`add_compile_options(-O0 -g)`，关闭优化
6. 一个比较坑的问题，clion的中文插件经常导致OCD崩溃，禁用

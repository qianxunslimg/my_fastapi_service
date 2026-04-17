---
date: '2023-04-18T00:24:00+08:00'
tags:
- 自驾相关
---

对看了下大佬的博客：[C++11（及现代C++风格）和快速迭代式开发 – 刘未鹏 | Mind Hacks](http://mindhacks.cn/2012/08/27/modern-cpp-practices/)中 提到了ScopeGuard的使用

### ScopeGuard

ScopeGuard，作用是在C++中实现资源管理。其实现基于RAII（Resource Acquisition Is Initialization）技术，即在对象的构造函数中获取资源，在对象的析构函数中释放资源。这种技术可以确保资源在任何情况下都会被正确地释放，即使在发生异常时也是如此。

使用这个ScopeGuard的好处是可以确保资源在任何情况下都会被正确地释放，即使在发生异常时也是如此。应用场景包括但不限于：

- 文件操作：打开文件后需要关闭文件。
- 内存分配：分配内存后需要释放内存。
- 线程同步：获取锁后需要释放锁。

### 源码及使用

ScopeGuard.h

```c++
#pragma once
#include <functional>
#include <iostream>

class ScopeGuard {
public:
  explicit ScopeGuard(std::function<void()> onExitScope)
      : onExitScope_(onExitScope), dismissed_(false) {}

  ~ScopeGuard() {  //析构函数中释放
    if (!dismissed_) {
      onExitScope_();
    }
  }

  void Dismiss() { dismissed_ = true; }

private:
  std::function<void()> onExitScope_;
  bool dismissed_;  //是否取消释放

private: // noncopyable
  ScopeGuard(ScopeGuard const &);
  ScopeGuard &operator=(ScopeGuard const &);
};

```

ScopeGuard_test.cpp

```c++
#include "ScopeGuard.h"
#include <fstream>
#include <iostream>

void foo() {
  // 打开一个文件
  std::ofstream file("test.txt");
  if (!file.is_open()) {
    std::cerr << "Failed to open file\n";
    return;
  }
  // 创建一个ScopeGuard对象，传入一个关闭文件的操作
  ScopeGuard guard([&file] { file.close(); });

  // 在文件中写入一些内容
  file << "Hello world\n";

  // 可能发生异常的代码
  // throw std::runtime_error("Something bad happened");

  // 退出函数时，无论是否发生异常，都会自动执行关闭文件的操作
}

int main() {
  try {
    foo();
  } catch (const std::exception &e) {
    std::cerr << e.what() << '\n';
  }
  return 0;
}

```

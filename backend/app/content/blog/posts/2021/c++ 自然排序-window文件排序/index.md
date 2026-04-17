---
date: '2021-12-02T19:29:51+08:00'
tags:
- 开发随笔
---

### 起因 

mfc的fileDialog读取批量文件 读取出来的文件名是按照字典序排序的

例如文件（举例子 忽略后缀）：1 2 3 4 5 6 7 8 9 10 11 12

字典序：1 10 11 12 2 3 4 5 6 7 8 9 

而很多时候需要按照`windows自然排序`，也就是例子本身 也就是windows按名称排序的顺序

调整好了一个用的`自然排序`比较函数 如下

#### 代码

```c++
//自然排序
bool compareNat(const std::string &a, const std::string &b) {
  if (a.empty())
    return true;
  if (b.empty())
    return false;
  if (std::isdigit(a[0]) && !std::isdigit(b[0]))
    return true;
  if (!std::isdigit(a[0]) && std::isdigit(b[0]))
    return false;
  if (!std::isdigit(a[0]) && !std::isdigit(b[0])) {
    if (std::toupper(a[0]) == std::toupper(b[0]))
      return compareNat(a.substr(1), b.substr(1));
    return (std::toupper(a[0]) < std::toupper(b[0]));
  }

  // Both strings begin with digit --> parse both numbers
  std::istringstream issa(a);
  std::istringstream issb(b);
  int ia, ib;
  issa >> ia;
  issb >> ib;
  if (ia != ib)
    return ia < ib;

  // Numbers are the same --> remove numbers and recurse
  std::string anew, bnew;
  std::getline(issa, anew);
  std::getline(issb, bnew);
  return (compareNat(anew, bnew));
}
bool judge(const pair<string, string> a, const pair<string, string> b) {
  return compareNat(a.first, b.first);
}
```

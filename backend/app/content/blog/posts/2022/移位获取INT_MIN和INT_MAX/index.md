---
date: '2022-05-09T19:28:00+08:00'
tags:
- 开发随笔
---

```c++
int main() {
  
  int minn = 1 << 31;           // INT_MIN 0x80000000
  int maxx = long(1 << 31) - 1; // INT_MAX 0x7fffffff
  int a = INT_MAX;
  int b = INT_MIN;

  return 0;
}
```

![image-20220509110112005](./assets/image-20220509110112005-2.png)

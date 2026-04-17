---
date: '2022-06-22T19:28:00+08:00'
tags:
- 开发随笔
---

# 哈希 自定义key

1. 自定义==等于判断函数==

   1. 结构体中重载==
   2. 仿函数 struct内重载()

2. 自定义==哈希函数==

   根据向量的每一个维度的不同，通过一定的计算，得到一个值，注意类型要用`size_t`来返回

```c++
struct Point {
  int x;
  int y;
  Point() : x(0), y(0){};
  Point(int _x, int _y) : x(_x), y(_y){};
  //1. 重载==
  bool operator==(const Point &other) const {
    return this->x == other.x && this->y == other.y;
  }
};

//2. 仿函数重载()
struct MyEqualFunc {
  bool operator()(const Point &v1, const Point &v2) const {
    return (v1.x == v2.x && v1.y == v2.y);
  }
};

struct MyHashFunc {
  size_t operator()(const Point &p) const { return hash<int>()(p.x & p.y); }
};


int main() {
  //1.
  unordered_set<Point, MyHashFunc, MyEqualFunc> set1;
  //2. 
  unordered_set<Point, MyHashFunc> set2;
  
  set1.insert(Point(0, 1));
  set1.insert(Point(0, 1));
  set1.insert(Point(0, 1));
  set1.insert(Point(2, 1));
  set1.insert(Point(0, 1));
  set1.insert(Point(1, 1));
  set1.insert(Point(1, 2));

  return 0;
```

# [红黑树自定义key](https://blog.csdn.net/y109y/article/details/82901710)

map是STL里的一个模板类，用来存放<key, value>键值对的数据结构，它的定义如下。

```c
template < class Key,                          				 //map::key_tpe
           class T,                                     //map::mapped_type
           class Compare = less<Key>,                   //map::key_compare
           class Alloc = allocator<pair<const Key, T>>  //map::allocator_type
           > class map;
```

- 第1个参数存储了key。

- 第2个参数存储了mapped value。

- 第3个参数是比较函数的[函数对象](https://blog.csdn.net/y109y/article/details/82898345)。map用它来判断两个key的大小，并返回bool类型的结果。利用这个函数，map可以确定元素在容器中遵循的顺序以及两个元素键是否相等（！comp（a，b）&&！comp（b，a）），确保map中没有两个元素可以具有等效键。这里，它的默认值是==less< Key >==，定义如下。

  ```c
  template <class T> 
  struct less {
    bool operator() (const T& x, const T& y) const {return x < y;}
    typedef T first_argument_type;
    typedef T second_argument_type;
    typedef bool result_type;
  };
  ```

- 第4个参数是用来定义存储分配模型的。

### 自定义key的方法主要是重载比较函数

1. 重载自定义的结构体的< 注意重载函数的两个const
2. lamda表达式 定义小于号的比较规则
3. 结构体仿函数重载()   map<Person, int, MyCompare> group;
4. 利用std::function调用普通函数
5. less函数的模板定制 略

```c++
struct Nodee {
  int a;
  Nodee(int val) { a = val; }
  // 2. 直接重载<
  bool operator<(const Nodee &other) const { return this->a < other.a; }
};

bool MyFunCompare(const Nodee &p1, const Nodee &p2) { //普通的函数
  return (p1.a < p2.a);
}

struct MyStructCompare { // Function Object
  bool operator()(const Nodee &p1, const Nodee &p2) const {
    return (p1.a < p2.a);
  }
};

int main() {
  Nodee a(5);
  Nodee b(1);
  Nodee c(100);
  // 1. lamda
  auto cmp = [](Nodee a, Nodee b) { return a.a < b.a; };
  map<Nodee, int, decltype(cmp)> map1(cmp);
  // 3. 结构体仿函数
  map<Nodee, int, MyStructCompare> map2;
  // 4. 利用std::function调用普通函数
  map<Nodee, int, function<bool(const Nodee &, const Nodee &)>> map3(
      MyFunCompare); //需要在构造函数中指明
  // 5. less函数的模板定制 略
  return 0;
}
```

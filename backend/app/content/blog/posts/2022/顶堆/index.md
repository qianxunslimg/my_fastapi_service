---
date: '2022-04-20T10:42:00+08:00'
categories:
- 算法整理
tags:
- 算法总结
---

## 顶堆基础知识

### 1. 底层原理

### 2. 应用

c++中的顶堆是 priority_queue，应用中有以下几个注意的点

1. 默认是大顶堆

   ```c++
   priority_queue<int> que;
   que.push(1);
   que.push(3);
   que.push(2);  // top : 3 2 1
   ```

2. 可以使用stl提供的 greater< T > 实现小顶堆

   `priority_queue<int, vector<int>, greater<int>> que;`

   对上面的参数做几个说明：

   1. 第一个int 是顶堆中的数据类型
   2. vector是顶堆使用的容器
   3. greater< T >标配是指定的

3. 自定义数据类型 和 比较规则 例如存储pair 按 和 从小到大排序

   ```c++
   auto cmp = [](const pair<int, int> a, const pair<int, int> b)->bool{
     return a.first + a.second > b.first + b.second;
   };
   priority_queue<pair<int, int>, vector<pair<int, int>>, decltype(cmp)> que(cmp);
   ```

   注意：

   1. 比较规则上，顶堆是和vector（或者其他？）完全相反的 `> 表示小顶堆`    `< 表示大顶堆`

   2. 不使用lamda的话 需要加取址运算符 `&`

      ```c++
      static bool cmp(const pair<int, int> a, const pair<int, int> b){
        return a.first + a.second > b.first + b.second;
      };
      priority_queue<pair<int, int>, vector<pair<int, int>>, decltype(&cmp)> que(cmp);
      ```

   3. 结构体内部重载 < 注意函数后的const该加加

      > 重载小于号猜测 顶堆默认调的是 less  如果重载大于号 则需要明确greater

      结构体重载（） 仿函数
      
      lamda decltype 注意 用到decltype 后面顶堆名就也要加（cmp函数名）

## 题目



### [剑指 Offer II 059. 数据流的第 K 大数值](https://leetcode-cn.com/problems/jBjn9C/)

难度简单23收藏分享切换为英文接收动态反馈英文版讨论区

设计一个找到数据流中第 `k` 大元素的类（class）。注意是排序后的第 `k` 大元素，不是第 `k` 个不同的元素。

请实现 `KthLargest` 类：

- `KthLargest(int k, int[] nums)` 使用整数 `k` 和整数流 `nums` 初始化对象。
- `int add(int val)` 将 `val` 插入数据流 `nums` 后，返回当前数据流中第 `k` 大的元素。

 

**示例：**

```
输入：
["KthLargest", "add", "add", "add", "add", "add"]
[[3, [4, 5, 8, 2]], [3], [5], [10], [9], [4]]
输出：
[null, 4, 5, 5, 8, 8]

解释：
KthLargest kthLargest = new KthLargest(3, [4, 5, 8, 2]);
kthLargest.add(3);   // return 4
kthLargest.add(5);   // return 5
kthLargest.add(10);  // return 5
kthLargest.add(9);   // return 8
kthLargest.add(4);   // return 8
```

#### 顶堆

维护一个大小为k的小顶堆，每次直接压入，超过k就pop 这样top()永远是第k大的

##### 直接使用优先级队列

```c++
class KthLargest {
    priority_queue<int, vector<int>, greater<int>> que;
    int k;
public:
    KthLargest(int k, vector<int>& nums) {
      this->k = k;
      for(int i = 0; i<nums.size(); i++){
        if(que.size() >= k){
          //其实可以压入前判断一下 减少压入
          que.push(nums[i]);
          que.pop();
        }else{
          que.push(nums[i]);
        }
      }
    }
    
    int add(int val) {
      if(que.size() == k){
        que.push(val);
        que.pop();
      }else{
        que.push(val);
      }
      return que.size() >= k?que.top():0;
    }
};
```

##### 听说字节不让直接用优先级队列

下滤并不如直接用优先级队列 猜测可能是insert部分的时间复杂度为Ok^2^*logk, 而使用上滤操作的话 可以使这里的局部复杂度为Oklogk

> 如果是堆排序 直接给定了n个数的数组, 那么使用下滤建堆 这样的时间复杂度是On?
>
> ```c++
> //小根堆
> void heap_build(vector<int> &nums, int rootPos, int lastPos) {
>   int leftPos = rootPos * 2 + 1;
>   if (leftPos < lastPos) {
>     int rightPos = leftPos + 1;
>     int maxPos = leftPos;
>     if (rightPos < lastPos) {
>       maxPos = nums[leftPos] < nums[rightPos] ? leftPos : rightPos;
>     }
>     if (nums[maxPos] < nums[rootPos]) {
>       swap(nums[maxPos], nums[rootPos]);
>       heap_build(nums, maxPos, lastPos);
>     }
>   }
> }
> 
> void heap_sort(vector<int> &nums) {
>   int n = nums.size();
>   for (int i = n / 2; i >= 0; i--) {
>     heap_build(nums, i, n);
>   }
>   for (int i = n - 1; i >= 0; i--) {
>     swap(nums[0], nums[i]);
>     heap_build(nums, 0, i);
>   }
> }
> 
> ```
>
> 而如果是像topk这种, 是慢慢插入的, 使用上滤插入建堆更好

```c++
//小根堆
void heap_build(vector<int> &nums, int rootPos, int lastPos) {
  int leftPos = rootPos * 2 + 1;
  if (leftPos < lastPos) {
    int rightPos = leftPos + 1;
    int maxPos = leftPos;
    if (rightPos < lastPos) {
      maxPos = nums[leftPos] < nums[rightPos] ? leftPos : rightPos;
    }
    if (nums[maxPos] < nums[rootPos]) {
      swap(nums[maxPos], nums[rootPos]);
      heap_build(nums, maxPos, lastPos);
    }
  }
}

void heap_sort(vector<int> &nums) {
  int n = nums.size();
  for (int i = n / 2; i >= 0; i--) {
    heap_build(nums, i, n);
  }
  for (int i = n - 1; i >= 0; i--) {
    swap(nums[0], nums[i]);
    heap_build(nums, 0, i);
  }
}

//上滤
void shift_up(vector<int> &nums) {
  int curr = nums.size() - 1;
  int val = nums.back();
  while (curr > 0 && val < nums[curr / 2]) {
    nums[curr] = nums[curr / 2];
    curr /= 2;
  }
  nums[curr] = val;
}

int findKthLargest(vector<int> &nums, int k) {
  int n = nums.size();
  vector<int> small_heap;
  for (int i = 0; i < n; i++) {
    if (small_heap.size() < k) {
      // small_heap.insert(small_heap.begin(), nums[i]);
      // heap_build(small_heap, 0, small_heap.size());
      small_heap.push_back(nums[i]);
      shift_up(small_heap);
    } else if (nums[i] > small_heap.front()) {
      small_heap[0] = nums[i];
      heap_build(small_heap, 0, small_heap.size());
    }
  }
  return small_heap[0];
}
```



### [373. 查找和最小的 K 对数字](https://leetcode-cn.com/problems/find-k-pairs-with-smallest-sums/)

难度中等390

给定两个以 **升序排列** 的整数数组 `nums1` 和 `nums2` , 以及一个整数 `k` 。

定义一对值 `(u,v)`，其中第一个元素来自 `nums1`，第二个元素来自 `nums2` 。

请找到和最小的 `k` 个数对 `(u1,v1)`, ` (u2,v2)` ...  `(uk,vk)` 。

 

**示例 1:**

```
输入: nums1 = [1,7,11], nums2 = [2,4,6], k = 3
输出: [1,2],[1,4],[1,6]
解释: 返回序列中的前 3 对数：
     [1,2],[1,4],[1,6],[7,2],[7,4],[11,2],[7,6],[11,4],[11,6]
```

**示例 2:**

```
输入: nums1 = [1,1,2], nums2 = [1,2,3], k = 2
输出: [1,1],[1,1]
解释: 返回序列中的前 2 对数：
     [1,1],[1,1],[1,2],[2,1],[1,2],[2,2],[1,3],[1,3],[2,3]
```

**示例 3:**

```
输入: nums1 = [1,2], nums2 = [3], k = 3 
输出: [1,3],[2,3]
解释: 也可能序列中所有的数对都被返回:[1,3],[2,3]
```

#### 解法1

1. 将所有组合 都压入顶堆 取前k个
2. 组合最后每个k个 小优化到 时间复杂度 k^2logk；

```c++
class Solution {
public:
    vector<vector<int>> kSmallestPairs(vector<int>& nums1, vector<int>& nums2, int k) {
      vector<vector<int>> ans;
      auto cmp = [](const pair<int,int>& a, const pair<int,int>& b)->bool{
        return a.first + a.second < b.first + b.second;
      };
      priority_queue<pair<int, int>,vector<pair<int,int>>, decltype(cmp)> que(cmp);
      auto sumPair = [](const pair<int, int> &a)->int{
        return a.first + a.second;
      };
      //注意这里可以小优化一下 k个数 则单个不可能超过k
      for(int i = 0; i<nums1.size() && i<k; i++) {
        int num1 = nums1[i];
        for(int j = 0; j<nums2.size() && j<k; j++){
          int num2 = nums2[j];
          if(que.size() >= k){
            if(sumPair(que.top()) > (num1 + num2)){
              que.pop();
              que.push(pair<int, int>(num1, num2));
            }
          }else que.push(pair<int, int>(num1, num2));
        }
      }
      int i = que.size() - 1;
      ans.resize(que.size());
      while(!que.empty()){
        ans[i--] = vector<int>{que.top().first, que.top().second};
        que.pop();
      }
      return ans;
    }
};
```

#### 解法2 正解

多路归并

同样是用顶堆 但是先压入较少的一组， 然后循环压入第二个数组 每次将堆顶压入ans 然后pop

注意一下lamda捕获的妙用，`只需要传入index 然后按照nums内的关系排序` 

时间复杂度 klogk 空间复杂度 k

```c++
class Solution {
public:
    bool swaped;
    vector<vector<int>> kSmallestPairs(vector<int>& nums1, vector<int>& nums2, int k) {
      vector<vector<int>> ans;
      swaped = 0;
      int n = nums1.size(), m = nums2.size();
      if(n > m){ //保证nums1 较少 n
        swap(nums1, nums2);
        swap(m, n);
        swaped = 1;
      }
      //定义比较规则  lamda捕获 用的太妙了
      auto cmp = [&](const auto& a, const auto& b)->bool{
        return nums1[a.first] + nums2[a.second] > nums1[b.first] + nums2[b.second];
      };
      priority_queue<pair<int, int>, vector<pair<int, int>>, decltype(cmp)> que(cmp);
      for(int i = 0; i<min(n, k); i++)
        que.push(pair<int, int>(i, 0));
      while(ans.size() < k && !que.empty()){
        pair<int, int> temp = que.top();
        que.pop();
        //注意 反转的换 需要在ans 反转回来
        swaped ? ans.push_back({nums2[temp.second], nums1[temp.first]}) : ans.push_back({nums1[temp.first], nums2[temp.second]});
        if(temp.second + 1 < m)
          que.push(pair<int, int>(temp.first, temp.second + 1));
      }
      return ans;
    }
};
```

### [剑指 Offer 41. 数据流中的中位数](https://leetcode-cn.com/problems/shu-ju-liu-zhong-de-zhong-wei-shu-lcof/)

难度困难309

如何得到一个数据流中的中位数？如果从数据流中读出奇数个数值，那么中位数就是所有数值排序之后位于中间的数值。如果从数据流中读出偶数个数值，那么中位数就是所有数值排序之后中间两个数的平均值。

例如，

[2,3,4] 的中位数是 3

[2,3] 的中位数是 (2 + 3) / 2 = 2.5

设计一个支持以下两种操作的数据结构：

- void addNum(int num) - 从数据流中添加一个整数到数据结构中。
- double findMedian() - 返回目前所有元素的中位数。

**示例 1：**

```
输入：
["MedianFinder","addNum","addNum","findMedian","addNum","findMedian"]
[[],[1],[2],[],[3],[]]
输出：[null,null,null,1.50000,null,2.00000]
```

#### 方法

使用两个顶堆 对半分的维护整个数组

例如：1 2 3 4 5

假设维护大顶堆个数多1

小： . 		2		3 		 3 4 		4 5

大： 1		1		2 1		2 1		3 2 1

```c++
class MedianFinder {
public:
    /** initialize your data structure here. */
    priority_queue<int> bigQue;
    priority_queue<int, vector<int>, greater<int>> smallQue;
    MedianFinder() {
    }
    
    //两个顶堆哪个个数多都没关系 只需要保证size差最大为1
    void addNum(int num) {
      if(smallQue.size() == bigQue.size()){
        smallQue.push(num);
        int tmp = smallQue.top();
        smallQue.pop();
        bigQue.push(tmp); 
      }else{
        bigQue.push(num);
        int tmp = bigQue.top();
        bigQue.pop();
        smallQue.push(tmp);     
      }
    }
    
    double findMedian() {
      if(smallQue.size() == bigQue.size())
        return (1.0 * (smallQue.top() + bigQue.top())/2);
      else return smallQue.top();
    }
};
```

### [378. 有序矩阵中第 K 小的元素](https://leetcode.cn/problems/kth-smallest-element-in-a-sorted-matrix/)

难度中等802

给你一个 `n x n` 矩阵 `matrix` ，其中每行和每列元素均按升序排序，找到矩阵中第 `k` 小的元素。
请注意，它是 **排序后** 的第 `k` 小元素，而不是第 `k` 个 **不同** 的元素。

你必须找到一个内存复杂度优于 `O(n2)` 的解决方案。

 

**示例 1：**

```
输入：matrix = [[1,5,9],[10,11,13],[12,13,15]], k = 8
输出：13
解释：矩阵中的元素为 [1,5,9,10,11,12,13,13,15]，第 8 小元素是 13
```

#### 解法1 归并

```c++
class Solution {
public:
    int kthSmallest(vector<vector<int>>& matrix, int k) {
        int n = matrix.size();

        // // 定义pq方法一：用自定义的比较
        // auto comp = [](Element e1, Element e2) { return e1.val > e2.val; };
        // priority_queue<Element, vector<Element>, decltype(comp)> pq (comp);    // 用优先队列表示最小堆

        // 定义pq方法二：在 Element 中重载 operator>，然后用内置的std::greater
        priority_queue<Element, vector<Element>> pq;

        // 初始化：将 matrix 的第一列加入 pq 作为初始的「最小人候选值」列表
        for (int r = 0; r < n; r++) {
            Element e (matrix[r][0], r, 0);
            pq.push(e);
        }

        // 弹出前 k-1 小的值
        for (int i = 0; i < k-1; i++) {
            Element top = pq.top();
            pq.pop();
            if (top.y != n - 1) {   // 当前 (top.x, top.y) 的右边还有数字，将它右边的数 push 到优先队列中
                Element e (matrix[top.x][top.y + 1], top.x, top.y + 1);
                pq.push(e);
            }
        }

        return pq.top().val;
    }

private:
    struct Element {
        int val;
        int x;
        int y;

        Element(int val, int x, int y) : val(val), x(x), y(y) {}

        // 方法二定义pq 需要重载 operator>
        bool operator< (const Element &other) const {
            return this->val > other.val;
        }
    };
};
```

##### 利用lamda捕获的简单归并写法

```c++
class Solution {
public:
    int kthSmallest(vector<vector<int>>& matrix, int k) {
      int n = matrix.size();
      auto cmp = [&](pair<int, int>& a, pair<int, int>& b){
        return matrix[a.first][a.second] > matrix[b.first][b.second];
      };
      priority_queue<pair<int, int>, vector<pair<int, int>>, decltype(cmp)> que(cmp);
      for(int i = 0; i < n; i++){
        que.push(pair<int, int>(i, 0));
      }
      // 弹出前 k-1 小的值
      for(int i = 0; i<k-1; i++){
        pair<int, int> top = que.top();
        que.pop(); //每次把最小的拿出来
        int x = top.first, y = top.second;
        if(y != n-1){
          que.push(pair<int, int>(x, y+1));
        }
      }
      return matrix[que.top().first][que.top().second];
    }
};
```

#### 解法2 二分 最优

时间复杂度：O(nlog(r−l))，二分查找进行次数为O(log(r−l))，每次操作时间复杂度为 O(n)。

空间复杂度：O(1)。

```c++
  bool check(vector<vector<int>> &matrix, int mid, int k, int n) {
    int i = n - 1;
    int j = 0;
    int num = 0;
    //每次对于「猜测」的答案 mid，计算矩阵中有多少数不大于 mid
    //如果数量不少于 k，那么说明最终答案 x 不大于 mid；
    //如果数量少于 k，那么说明最终答案 x 大于 mid。
    while (i >= 0 && j < n) {
      if (matrix[i][j] <= mid) {
        num += i + 1;
        j++;
      } else {
        i--;
      }
    }
    return num >= k;
  }

  int kthSmallest2(vector<vector<int>> &matrix, int k) {
    int n = matrix.size();
    int left = matrix[0][0];
    int right = matrix[n - 1][n - 1];
    while (left < right) {
      int mid = left + ((right - left) >> 1);
      if (check(matrix, mid, k, n)) { //<=mid的个数>=k 找左边界
        right = mid;                  //向左上角收缩
      } else {
        left = mid + 1; //向右下角扩大
      }
    }
    return left;
  }
```

### [347. 前 K 个高频元素](https://leetcode.cn/problems/top-k-frequent-elements/)

难度中等1197

给你一个整数数组 `nums` 和一个整数 `k` ，请你返回其中出现频率前 `k` 高的元素。你可以按 **任意顺序** 返回答案。

 

**示例 1:**

```
输入: nums = [1,1,1,2,2,3], k = 2
输出: [1,2]
```

**示例 2:**

```
输入: nums = [1], k = 1
输出: [1]
```

 

**提示：**

- `1 <= nums.length <= 105`
- `k` 的取值范围是 `[1, 数组中不相同的元素的个数]`
- 题目数据保证答案唯一，换句话说，数组中前 `k` 个高频元素的集合是唯一的

<u>**进阶：**你所设计算法的时间复杂度 **必须** 优于 `O(n log n)` ，其中 `n` 是数组大小。</u>

#### 思路

作为面试题的话 大顶堆的写法很好想到的 但是时间复杂度是onlogn，不满足后面的进阶要求，如下

- topk （前k大）用小根堆，维护堆大小不超过 k 即可。每次压入堆前和堆顶元素比较，如果比堆顶元素还小，直接扔掉，否则压入堆。检查堆大小是否超过 k，如果超过，弹出堆顶。复杂度是 `nlogk`
- 避免使用大根堆，因为你得把所有元素压入堆，复杂度是 nlogn，而且还浪费内存。如果是海量元素，那就挂了。

#### 代码

> 使用lamda对map进行捕获，顶堆只存int就可以

```c++
class Solution {
public:
    vector<int> topKFrequent(vector<int>& nums, int k) {
      unordered_map<int, int> mapp;
      for(int num : nums)
        mapp[num]++;
      auto cmp = [&](int a, int b){
        return mapp[a] > mapp[b];
      };
      priority_queue<int, vector<int>, decltype(cmp)> que(cmp);
      for(auto it = mapp.begin(); it!= mapp.end(); it++){
        if(que.size() < k)
          que.push(it->first);
        else{
          int nowMin = mapp[que.top()];
          if(it->second > nowMin){
            que.pop();
            que.push(it->first);
          }
        }
      }
      vector<int> ans;
      while(!que.empty()){
        ans.push_back(que.top());
        que.pop();
      }
      return ans;
    }
};
```

### [239. 滑动窗口最大值](https://leetcode.cn/problems/sliding-window-maximum/)

[labuladong 题解](https://labuladong.github.io/article/?qno=239)[思路](https://leetcode.cn/problems/sliding-window-maximum/#)

难度困难1685

给你一个整数数组 `nums`，有一个大小为 `k` 的滑动窗口从数组的最左侧移动到数组的最右侧。你只可以看到在滑动窗口内的 `k` 个数字。滑动窗口每次只向右移动一位。

返回 *滑动窗口中的最大值* 。

**示例 1：**

```
输入：nums = [1,3,-1,-3,5,3,6,7], k = 3
输出：[3,3,5,5,6,7]
解释：
滑动窗口的位置                最大值
---------------               -----
[1  3  -1] -3  5  3  6  7       3
 1 [3  -1  -3] 5  3  6  7       3
 1  3 [-1  -3  5] 3  6  7       5
 1  3  -1 [-3  5  3] 6  7       5
 1  3  -1  -3 [5  3  6] 7       6
 1  3  -1  -3  5 [3  6  7]      7
```

#### 解答

1. 优先队列 Onlogn
```c++
class Solution {
public:
    vector<int> maxSlidingWindow(vector<int>& nums, int k) {
        int n = nums.size();
        priority_queue<pair<int, int>> q;
        for (int i = 0; i < k; ++i) {
            q.emplace(nums[i], i);
        }
        vector<int> ans = {q.top().first};
        for (int i = k; i < n; ++i) {
            q.emplace(nums[i], i);
            while (q.top().second <= i - k) {
                q.pop();
            }
            ans.push_back(q.top().first);
        }
        return ans;
    }
};
```
2. 单调双端队列
```c++
class Solution {
public:
    vector<int> maxSlidingWindow(vector<int>& nums, int k) {
        int n = nums.size();
        deque<int> q;
        for (int i = 0; i < k; ++i) {
            while (!q.empty() && nums[i] >= nums[q.back()]) {
                q.pop_back();
            }
            q.push_back(i);
        }

        vector<int> ans = {nums[q.front()]};
        for (int i = k; i < n; ++i) {
            while (!q.empty() && nums[i] >= nums[q.back()]) {
                q.pop_back();
            }
            q.push_back(i);
            while (q.front() <= i - k) {
                q.pop_front();
            }
            ans.push_back(nums[q.front()]);
        }
        return ans;
    }
};
```

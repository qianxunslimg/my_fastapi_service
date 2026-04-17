---
date: '2022-04-20T01:52:49+08:00'
categories:
- 算法整理
tags:
- 算法总结
---

## 多路归并

- [264. 丑数 II](https://leetcode-cn.com/problems/ugly-number-ii/)
- [313. 超级丑数](https://leetcode-cn.com/problems/super-ugly-number/)
- [373. 查找和最小的K对数字](https://leetcode-cn.com/problems/find-k-pairs-with-smallest-sums/comments/)
- [632. 最小区间](https://leetcode-cn.com/problems/smallest-range-covering-elements-from-k-lists/)
- [719. 找出第 k 小的距离对](https://leetcode-cn.com/problems/find-k-th-smallest-pair-distance/)
- [786. 第 K 个最小的素数分数](https://leetcode-cn.com/problems/k-th-smallest-prime-fraction/)
- [1439. 有序矩阵中的第 k 个最小数组和](https://leetcode-cn.com/problems/find-the-kth-smallest-sum-of-a-matrix-with-sorted-rows/)
- [1508. 子数组和排序后的区间和](https://leetcode-cn.com/problems/range-sum-of-sorted-subarray-sums/)
- [1675. 数组的最小偏移量](https://leetcode-cn.com/problems/minimize-deviation-in-array/)



### [264. 丑数 II](https://leetcode-cn.com/problems/ugly-number-ii/)

难度中等890收藏分享切换为英文接收动态反馈

给你一个整数 `n` ，请你找出并返回第 `n` 个 **丑数** 。

**丑数** 就是只包含质因数 `2`、`3` 和/或 `5` 的正整数。

 

**示例 1：**

```
输入：n = 10
输出：12
解释：[1, 2, 3, 4, 5, 6, 8, 9, 10, 12] 是由前 10 个丑数组成的序列。
```

**示例 2：**

```
输入：n = 1
输出：1
解释：1 通常被视为丑数。
```

#### 解法1

使用小顶堆记录每个丑数 使用set进行去重

去重的原因 1 2 3 4 5    2 * 5    5 * 2  不去重的话  会记录两遍

```c++
class Solution {
public:
    int nthUglyNumber(int n) {
        vector<int> factors = {2, 3, 5};
        unordered_set<long> sett;
        priority_queue<long, vector<long>, greater<long>> que;
        sett.insert(1L);
        que.push(1L);
        int ans = 0;
        for (int i = 0; i < n; i++) {
            long curr = que.top();
            que.pop();
            ans = (int)curr;
            for (int factor : factors) {
                long next = curr * factor;
                if (!sett.count(next)) {
                    sett.insert(next);
                    que.push(next);
                }
            }
        }
        return ans;
    }
};
```

相同的思路 可以直接用set

```c++
class Solution {
public:
	int nthUglyNumber(int n) {
        set<long> sett;  // set 是有序的，且不重复
        long ans = 1;
        for (int i = 1; i < n; i++) {
            sett.insert(ans * 2);
            sett.insert(ans * 3);
            sett.insert(ans * 5);
            ans = *sett.begin();
            sett.erase(ans);
        }
        return (int)ans;
    }	
};
```

#### 解答2

多路归并

「往后产生的丑数」都是基于「已有丑数」而来（使用「已有丑数」乘上「质因数」2、3、5）。

```c++
class Solution {
public:
    int nthUglyNumber(int n) {
      vector<int> dp(n+1);
      dp[1] = 1;
      //三个数记录*2 *3 *5 在dp内的下标
      int p2 = 1, p3 = 1, p5 = 1;
      for(int i = 2; i<=n; i++){
        dp[i] = min(min(dp[p2]*2, dp[p3]*3), dp[p5]*5);
        if(dp[i] == dp[p2]*2)
          p2++;
        if(dp[i] == dp[p3]*3)
          p3++;
        if(dp[i] == dp[p5]*5)
          p5++;
      }
      return dp[n];
  }
};
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

#### 解法1

1. 将所有组合 都压入顶堆 取前k个
2. 组合最后每个k个 小优化到 时间复杂度 `k^2logk`；

```C++
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

### [786. 第 K 个最小的素数分数](https://leetcode-cn.com/problems/k-th-smallest-prime-fraction/)

难度困难213英文版讨论区

给你一个按递增顺序排序的数组 `arr` 和一个整数 `k` 。数组 `arr` 由 `1` 和若干 **素数** 组成，且其中所有整数互不相同。

对于每对满足 `0 <= i < j < arr.length` 的 `i` 和 `j` ，可以得到分数 `arr[i] / arr[j]` 。

那么第 `k` 个最小的分数是多少呢? 以长度为 `2` 的整数数组返回你的答案, 这里 `answer[0] == arr[i]` 且 `answer[1] == arr[j]` 。

**示例 1：**

```
输入：arr = [1,2,3,5], k = 3
输出：[2,5]
解释：已构造好的分数,排序后如下所示: 
1/5, 1/3, 2/5, 1/2, 3/5, 2/3
很明显第三个最小的分数是 2/5
```

**示例 2：**

```
输入：arr = [1,7], k = 1
输出：[1,7]
```

#### 解法

1. 什么pair On^2 加sort的垃圾解法就不说了，On^2^logn

2. 用归并，类似上一题

   1 2 3 4 5 

   1 2 3 4 5

   压入 1/2 1/3 1/4 1/5 然后 1/5出  2/5入 然后 1/4出 2/4入....

```c++
class Solution {
public:
    vector<int> kthSmallestPrimeFraction(vector<int>& nums, int k) {
      vector<int> ans;
      auto cmp = [&](const pair<int, int> a, const pair<int ,int> b){
        return (double)nums[a.first] / nums[a.second] >  (double)nums[b.first] / nums[b.second];
      };
      priority_queue<pair<int, int> ,vector<pair<int, int>>, decltype(cmp)> que(cmp);
      for(int i = 1; i<nums.size(); i++){
        que.push(pair<int, int>(0, i));
      }
      // 为社么是 k-1 因为pop调k-1g个最下 就是第k个最小了
      // 相同的怎么办 1怎么办  
      // 1太大 不可能到1 看题目
      for (int i = 0; i < k - 1; i++) {
          auto p = que.top();
          que.pop();
          que.push(pair<int, int>(p.first + 1, p.second));
      }

      ans.push_back(nums[que.top().first]);
      ans.push_back(nums[que.top().second]);

      return ans;
    }
};
```

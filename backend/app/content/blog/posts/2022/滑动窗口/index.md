---
date: '2022-03-15T19:49:49+08:00'
categories:
- 算法整理
tags:
- 算法总结
---

## 滑动窗口模板

框架

```c++
/* 滑动窗口算法框架 */
void slidingWindow(string s, string t) {
    unordered_map<char, int> need, window;
    for (char c : t) need[c]++;
    
    int left = 0, right = 0;
    int valid = 0; 
    while (right < s.size()) {
        // c 是将移入窗口的字符
        char c = s[right];
        // 右移窗口
        right++;
        // 进行窗口内数据的一系列更新
        ...

        /*** debug 输出的位置 ***/
        printf("window: [%d, %d)\n", left, right);
        /********************/
        
        // 判断左侧窗口是否要收缩
        while (window needs shrink) {
            // d 是将移出窗口的字符
            char d = s[left];
            // 左移窗口
            left++;
            // 进行窗口内数据的一系列更新
            ...
        }
    }
}
```

## 相关题目

### [76. 最小覆盖子串](https://leetcode-cn.com/problems/minimum-window-substring/) 困难

[labuladong 题解](https://labuladong.github.io/article/?qno=76)[思路](https://leetcode.cn/problems/minimum-window-substring/#)

难度困难1896

给你一个字符串 `s` 、一个字符串 `t` 。返回 `s` 中涵盖 `t` 所有字符的最小子串。如果 `s` 中不存在涵盖 `t` 所有字符的子串，则返回空字符串 `""` 。

 

**注意：**

- 对于 `t` 中重复字符，我们寻找的子字符串中该字符数量必须不少于 `t` 中该字符数量。
- 如果 `s` 中存在这样的子串，我们保证它是唯一的答案。

 

**示例 1：**

```
输入：s = "ADOBECODEBANC", t = "ABC"
输出："BANC"
```

````c++
class Solution {
public:
  string minWindow(string s, string t) {
    unordered_map<char, int> need, window;
    for (char c : t)
      need[c]++;
    int left = 0, right = 0;
    int valid = 0;
    //记录最小覆盖字串的其实索引和长度
    int start = 0, len = INT_MAX;
    while (right < s.size()) {
      // c是移入窗口的字符
      char c = s[right];
      right++;
      // 进行窗口内数据的一系列更新
      if (need.count(c)) {
        window[c]++;
        if (window[c] == need[c])
          valid++;
      }
      //判断左窗口是否需要收缩
      while (valid == need.size()) { //窗口满足条件
                                     // 在这里更新最小覆盖子串
        if (right - left < len) {
          start = left;
          len = right - left;
        }
        // d 是将移出窗口的字符
        char d = s[left];
        // 左移窗口
        left++;
        // 进行窗口内数据的一系列更新
        if (need.count(d)) {
          if (window[d] == need[d]) {
            valid--;
          }
          window[d]--;
        }
      }
    }
    return len == INT_MAX ? "" : s.substr(start, len);
  }
};
````

### [567. 字符串的排列](https://leetcode-cn.com/problems/permutation-in-string/) 中等

难度中等685

给你两个字符串 `s1` 和 `s2` ，写一个函数来判断 `s2` 是否包含 `s1` 的排列。如果是，返回 `true` ；否则，返回 `false` 。

换句话说，`s1` 的排列之一是 `s2` 的 **子串** 。

 

**示例 1：**

```
输入：s1 = "ab" s2 = "eidbaooo"
输出：true
解释：s2 包含 s1 的排列之一 ("ba").
```

**示例 2：**

```
输入：s1= "ab" s2 = "eidboaoo"
输出：false
```

```c++
class Solution {
public:
    bool checkInclusion(string t, string s) {
      unordered_map<char,int> window, need;
      for(char c : t) need[c]++;
      int left = 0, right = 0;
      int valid = 0;
      while(right < s.size()){
        //扩大 知道满足 window = need
        char c = s[right];
        right++;
        if(need.count(c)){
          window[c]++;
          if(window[c] == need[c])
            valid++;
        }
        //个数满足
        while(right-left>=t.size()){  //缩减窗口到t的长度
          if(valid == need.size())
            return true;
          char d = s[left];
          left++;
          if(need.count(d)){
            if(window[d] == need[d])
              valid--;
            window[d]--;
          }
        }
      }
      return false;
    }
};

```

### [438. 找到字符串中所有字母异位词](https://leetcode-cn.com/problems/find-all-anagrams-in-a-string/) 

难度中等898收藏分享切换为英文接收动态反馈

给定两个字符串 `s` 和 `p`，找到 `s` 中所有 `p` 的 **异位词** 的子串，返回这些子串的起始索引。不考虑答案输出的顺序。

**异位词** 指由相同字母重排列形成的字符串（包括相同的字符串）。

```c++

// class Solution {
// public:
//     map<char, int> checkAna;
//     map<char, int> checkAnb;
//     vector<int> findAnagrams(string s, string p) {
//         vector<int> res;
//         int n = s.size(); 
//         int nn = p.size();
//         if(isAnagrams("abc", "bca")){
//             cout<<"check"<<endl;
//         }
//         for(int i = 0; i<n-nn+1; i++){
//             cout<<s.substr(i, nn) <<endl;
//             if(isAnagrams(s.substr(i, nn), p))
//                 res.push_back(i);
//         }
//         return res;
//     }
//     bool isAnagrams(string a, string b){
//         checkAna.clear();
//         checkAnb.clear();
//         for(int i = 0; i<a.size(); i++){
//             checkAna[a[i]]++;
//             checkAnb[b[i]]++;
//         }
//         for(auto it = checkAna.begin(); it !=checkAna.end(); it++){
//             if(it->second != checkAnb[it->first])
//                 return 0;
//         }
//         return 1;
//     }
// };

// class Solution {
// public:
//     vector<int> findAnagrams(string s, string p) {
//         vector<int> res;
//         int n = s.size(); 
//         int nn = p.size();
//         if(n<nn) return vector<int>();
//         vector<int> ss(26);
//         vector<int> pp(26);
//         //初始化保证窗口初始移动
//         for(int i = 0; i<nn; i++){
//             ss[s[i]-'a']++;
//             pp[p[i]-'a']++;
//         }
//         if(ss == pp) res.push_back(0);
//         for(int i = 0; i<n-nn; i++){
//             ss[s[i]-'a']--;
//             ss[s[i+nn]-'a']++;
//             if(ss == pp) res.push_back(i+1);
//         }
//         return res;
//     }
// };

class Solution {
public:
    vector<int> findAnagrams(string s, string p) {
      vector<int> ans;
      unordered_map<char, int> need, window;
      for(char c : p) need[c]++;
      int left = 0, right = 0, valid = 0;
      while(right<s.size()){
        char c = s[right];
        right++;
        if(need.count(c)){
          window[c]++;
          if(window[c] == need[c])
            valid++;
        }
        while(right-left >= p.size()){
          if(valid == need.size()) ans.push_back(left);
          char d = s[left];
          left++;
          if(need.count(d)){
            if(need[d] == window[d])
              valid--;
            window[d]--;
          }
        }
      }
      return ans;
    }
};

```

### [3. 无重复字符的最长子串](https://leetcode-cn.com/problems/longest-substring-without-repeating-characters/) 

难度中等7633

给定一个字符串 `s` ，请你找出其中不含有重复字符的 **最长子串** 的长度。

 

**示例 1:**

```
输入: s = "abcabcbb"
输出: 3 
解释: 因为无重复字符的最长子串是 "abc"，所以其长度为 3。
```

**示例 2:**

```
输入: s = "bbbbb"
输出: 1
解释: 因为无重复字符的最长子串是 "b"，所以其长度为 1。
```

````c++

class Solution {
public:
  int lengthOfLongestSubstring(string s) {
    int ans = 0;
    int left = 0, right = 0;
    unordered_map<char, int> window;
    while (right < s.size()) {
      char c = s[right];
      right++;
      window[c]++;
      while (window[c] > 1) { //有重复就要从left++ 直到消除当前重复
        char d = s[left];
        left++;
        window[d]--;
      }
      ans = max(ans, right - left);
    }
    return ans;
  }
};
// class Solution {
// public:
//   int lengthOfLongestSubstring(string s) {
//     if (s.size() == 0)
//       return 0;
//     unordered_set<char> lookup;
//     int maxStr = 0;
//     int left = 0;
//     for (int i = 0; i < s.size(); i++) {
//       while (lookup.find(s[i]) != lookup.end()) {
//         lookup.erase(s[left]);
//         left++;
//       }
//       maxStr = max(maxStr, i - left + 1);
//       lookup.insert(s[i]);
//     }
//     return maxStr;
//   }
// };
  //int lengthOfLongestSubstring(string s) {
  //  if (s.size() == 0) {
  //    return 0;
  //  }
  //  vector<string> ss;
  //  for (int i = 0; i < s.size(); i++) {
  //    unordered_map<char, int> temp_map;
  //    for (int j = i; j < s.size(); j++) {
  //      ++temp_map[s[j]];
  //      if (temp_map[s[j]] > 1) {
  //        string sss = s.substr(i, j - i);
  //        ss.push_back(sss);
  //        break;
  //      }
  //      if (j == s.size() - 1) {
  //        string sss = s.substr(i, s.size() - i);
  //        ss.push_back(sss);
  //      }
  //    }
  //  }
  //  if (ss.size() == 0) {
  //    return s.size();
  //  }
  //  sort(ss.begin(), ss.end(),
  //       [](string &a, string &b) { return a.size() > b.size(); });
  //  return ss[0].size();
  //}

````

### [2024. 考试的最大困扰度](https://leetcode-cn.com/problems/maximize-the-confusion-of-an-exam/)

一位老师正在出一场由 `n` 道判断题构成的考试，每道题的答案为 true （用 `'T'` 表示）或者 false （用 `'F'` 表示）。老师想增加学生对自己做出答案的不确定性，方法是 **最大化** 有 **连续相同** 结果的题数。（也就是连续出现 true 或者连续出现 false）。

给你一个字符串 `answerKey` ，其中 `answerKey[i]` 是第 `i` 个问题的正确结果。除此以外，还给你一个整数 `k` ，表示你能进行以下操作的最多次数：

- 每次操作中，将问题的正确答案改为 `'T'` 或者 `'F'` （也就是将 `answerKey[i]` 改为 `'T'` 或者 `'F'` ）。

请你返回在不超过 `k` 次操作的情况下，**最大** 连续 `'T'` 或者 `'F'` 的数目。

 

**示例 1：**

```
输入：answerKey = "TTFF", k = 2
输出：4
解释：我们可以将两个 'F' 都变为 'T' ，得到 answerKey = "TTTT" 。
总共有四个连续的 'T' 。
```

**示例 2：**

```
输入：answerKey = "TFFT", k = 1
输出：3
解释：我们可以将最前面的 'T' 换成 'F' ，得到 answerKey = "FFFT" 。
或者，我们可以将第二个 'T' 换成 'F' ，得到 answerKey = "TFFF" 。
两种情况下，都有三个连续的 'F' 。
```

#### 思路

1. 用框架 但需要使用额外的 On   90ms 10mb
2. 官方题解 有点类似分治的思想 以T和F都当作最大值基准算一遍 取结果最大值  30ms 10mb

#### 代码

框架  90ms 10mb

```c++
//滑动窗口 框架
class Solution {
public:
    int maxConsecutiveAnswers(string answerKey, int k) {
        int n = answerKey.size();
        unordered_map<int, int> window;
        int left = 0, right = 0;
        int ans = 0;
        while(right<n){
            char c = answerKey[right];
            right++;
            window[c]++;
            //窗口缩小
            while(window['F']> k && window['T']>k){
                char d = answerKey[left];
                left++;
                window[d]--;
            }
            ans = max(window['F']+window['T'], ans);
        }
        return ans;
    }
};
```

官方 30ms 10mb

```c++
class Solution {
public:
    //ch 假设的最大值字母
    int maxConsecutiveChar(string& answerKey, int k, char ch) {
        int n = answerKey.length();
        int ans = 0;
        //sum 为另一种 杂质字母的数量
        for (int left = 0, right = 0, sum = 0; right < n; right++) {
            sum += answerKey[right] != ch;
            while (sum > k) {
                //不断left++ 减小另一个字母数量
                sum -= answerKey[left++] != ch;
            }
            ans = max(ans, right - left + 1);
        }
        return ans;
    }

    int maxConsecutiveAnswers(string answerKey, int k) {
        return max(maxConsecutiveChar(answerKey, k, 'T'),
                   maxConsecutiveChar(answerKey, k, 'F'));
    }
};
```

### [1004. 最大连续1的个数 III](https://leetcode-cn.com/problems/max-consecutive-ones-iii/)

难度中等393

给定一个二进制数组 `nums` 和一个整数 `k`，如果可以翻转最多 `k` 个 `0` ，则返回 *数组中连续 `1` 的最大个数* 。

 

**示例 1：**

```
输入：nums = [1,1,1,0,0,0,1,1,1,1,0], K = 2
输出：6
解释：[1,1,1,0,0,1,1,1,1,1,1]
粗体数字从 0 翻转到 1，最长的子数组长度为 6。
```

**示例 2：**

```
输入：nums = [0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1], K = 3
输出：10
解释：[0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1]
粗体数字从 0 翻转到 1，最长的子数组长度为 10。
```

思路

滑动窗口是一个思想 重点在于窗口指针的移动 

所以 哈希只是通用性比较强 在有的情况下是可以替换乃至省去的

代码

模板

```c++
class Solution {
public:
    int longestOnes(vector<int>& nums, int k) {
        int n = nums.size();
        unordered_map<int,int> window;
        int left = 0, right = 0;
        int ans = 0;
        while(right<n){
            int c = nums[right];
            window[c]++;
            right++;
            while(window[0]>k){
                int d = nums[left];
                left++;
                window[d]--;
            }
            ans = max(ans, window[1] + window[0]);
        }
        return ans;
    }
};
```

空间优化版本：只需要维护0的个数就可以了

```c++
class Solution {
public:
    int longestOnes(vector<int>& A, int K) {
        int res = 0, zeros = 0, left = 0;
        for (int right = 0; right < A.size(); ++right) {
            if (A[right] == 0) ++zeros;
            while (zeros > K) {
                if (A[left++] == 0) --zeros;
            }
            res = max(res, right - left + 1);
        }
        return res;
    }
};
```

### [424. 替换后的最长重复字符 字节2020原题](https://leetcode-cn.com/problems/longest-repeating-character-replacement/)

难度中等576

给你一个字符串 `s` 和一个整数 `k` 。你可以选择字符串中的任一字符，并将其更改为任何其他大写英文字符。该操作最多可执行 `k` 次。

在执行上述操作后，返回包含相同字母的最长子字符串的长度。

 

**示例 1：**

```
输入：s = "ABAB", k = 2
输出：4
解释：用两个'A'替换为两个'B',反之亦然。
```

**示例 2：**

```
输入：s = "AABABBA", k = 1
输出：4
解释：
将中间的一个'A'替换为'B',字符串变为 "AABBBBA"。
子串 "BBBB" 有最长重复字母, 答案为 4。
```

#### 思路

滑动窗口融会贯通，比如这个题 就没想到怎么用map滑

> 这里有个优化，`不需要每次都去重新更新max_count`。比如说"`AAABCDEEEE`" k=2，这个case，一开始A出现3次,max_count=3，但是当指针移到D时发现不行了，要移动left指针了。此时count['A']-=1，但是不需要把max_count更新为2。为什么呢？ 因为根据我们的算法，当max_count和k一定时，区间最大长度也就定了。当我们找到一个max_count之后，我们就能说我们找到了一个长度为d=max_count+k的合法区间，所以最终答案一定不小于d。所以，当发现继续向右扩展right不合法的时候，我们不需要不断地右移left，只需要保持区间长度为d向右滑动即可。如果有某个合法区间大于d，一定在某个时刻存在count[t]+1>max_count，这时再去更新max_count即可。

#### 代码

```c++
class Solution {
public:
    int characterReplacement(string s, int k) {
        vector<int> num(26);
        int n = s.length();
        int maxn = 0;
        int left = 0, right = 0;
        while (right < n) {
            num[s[right] - 'A']++;
            //maxn维护窗口最多元素的个数 以进行非最多元素个数的统计判断
            maxn = max(maxn, num[s[right] - 'A']);
            if (right - left + 1 - maxn > k) {
                num[s[left] - 'A']--;
                left++;
            }
            right++;
        }
        return right - left;
    }
};

//更换为 map计数
class Solution {
public:
    int characterReplacement(string s, int k) {
        unordered_map<char, int> window;
        int n = s.length();
        int maxn = 0;
        int left = 0, right = 0;
        while (right < n) {
            window[s[right]]++;
            maxn = max(maxn, window[s[right]]);
            while(right - left + 1 - maxn > k) {
                window[s[left]]--;;
                left++;
            }
            right++;
        }
        return right - left;
    }
};
```

### [剑指 Offer II 008. 和大于等于 target 的最短子数组](https://leetcode-cn.com/problems/2VG8Kg/)

难度中等53

给定一个含有 `n` 个正整数的数组和一个正整数 `target` **。**

找出该数组中满足其和 `≥ target` 的长度最小的 **连续子数组** `[numsl, numsl+1, ..., numsr-1, numsr]` ，并返回其长度**。**如果不存在符合条件的子数组，返回 `0` 。

 

**示例 1：**

```
输入：target = 7, nums = [2,3,1,2,4,3]
输出：2
解释：子数组 [4,3] 是该条件下的长度最小的子数组。
```

**示例 2：**

```
输入：target = 4, nums = [1,4,4]
输出：1
```

**示例 3：**

```
输入：target = 11, nums = [1,1,1,1,1,1,1,1]
输出：0
```

#### 思路

滑动窗口 模板大概还是那个模板 两个while比较好理解

#### 代码

```c++
class Solution {
public:
    int minSubArrayLen(int target, vector<int>& nums) {
        int left = 0; 
        int right = 0;
        int n = nums.size();
        int sum = 0; 
        int ans = INT_MAX;
        while(right<n){
            sum += nums[right];
            right++;
            while(sum>=target) {
                ans = min(ans, right - left);
                sum -= nums[left];
                left++;
            }
        }
        return ans == INT_MAX ? 0 : ans;
    }
};
```

### [剑指 Offer II 009. 乘积小于 K 的子数组](https://leetcode-cn.com/problems/ZVAVXX/)

难度中等63

给定一个正整数数组 `nums`和整数 `k` ，请找出该数组内乘积小于 `k` 的连续的子数组的个数。

 

**示例 1:**

```
输入: nums = [10,5,2,6], k = 100
输出: 8
解释: 8 个乘积小于 100 的子数组分别为: [10], [5], [2], [6], [10,5], [5,2], [2,6], [5,2,6]。
需要注意的是 [10,5,2] 并不是乘积小于100的子数组。
```

**示例 2:**

```
输入: nums = [1,2,3], k = 0
输出: 0
```

#### 思路

1. 这道题 正确解法 应该是滑动窗口

   > `重点 right - left + 1`
   >
   > 比如某次遍历符合题意的子数组为 ABCX，那么在该条件下符合条件的有X，CX，BCX，ABCX共四个（可以进行多个例子，发现个数符合right-left+1）

2. 但是 做这道题的过程中 感觉这个 不跳步的回溯 挺有意思 外层循环backtrack 

   其实 好像相当于两层for循环了 卧槽 我真是垃圾
   
   <u>`其实 也好像有点类似n叉树 有向图的遍历吧？`</u>[图论 | qianxunslimgのblog](https://qianxunslimg.github.io/2022/03/15/tu-lun/)

#### 代码

正确的滑动窗口解法

```c++
class Solution {
public:
    int numSubarrayProductLessThanK(vector<int>& nums, int k) {
        int multi = 1;
        int n = nums.size();
        if(k <= 1) return 0;
        int left = 0, right = 0;
        int ans = 0;
        while(right < n){
            multi*=nums[right];
            while(multi>=k){
                multi/=nums[left];
                left++;
            }
            ans += (right - left + 1); //注意 每次+的是窗口的长度
            right++;  //这个写在前面也是可以的 只是right - left 不加1
        }
        return ans;
    }
};
```

回溯（假）

```c++
class Solution {
public:
    int ans;
    //vector<vector<int>> all;
    //vector<int> path;
    int numSubarrayProductLessThanK(vector<int>& nums, int k) {
        ans = 0;
        for(int i = 0; i<nums.size(); i++){
            backtrack(nums, i, 1, k);
        }
        // cout<<all.size()<<endl;
        // for(int i = 0; i<all.size(); i++){
        //     for(int j = 0; j<all[i].size(); j++){
        //         cout<<all[i][j]<<" ";
        //     }
        //     cout<<endl;
        // }
        return ans;
    }

    void backtrack(vector<int>& nums, int startIndex, int preK, int k){
        if(startIndex>=nums.size() || preK>=k) return;
        preK*=nums[startIndex];
        //path.push_back(nums[startIndex]);
        if(preK<k){
          ans++;  
          //all.push_back(path);
        }
        backtrack(nums, startIndex+1, preK, k);
        preK /= nums[startIndex];
        //path.pop_back();
    }
};
```

### [剑指 Offer II 057. 值和下标之差都在给定的范围内](https://leetcode-cn.com/problems/7WqeDu/)

难度中等35

给你一个整数数组 `nums` 和两个整数 `k` 和 `t` 。请你判断是否存在 **两个不同下标** `i` 和 `j`，使得 `abs(nums[i] - nums[j]) <= t` ，同时又满足 `abs(i - j) <= k` 。

如果存在则返回 `true`，不存在返回 `false`。

 

**示例 1：**

```
输入：nums = [1,2,3,1], k = 3, t = 0
输出：true
```

**示例 2：**

```
输入：nums = [1,0,1,1], k = 1, t = 2
输出：true
```

**示例 3：**

```
输入：nums = [1,5,9,1,5,9], k = 2, t = 3
输出：false
```

#### 方法1

滑动窗口 用set进行排序 查找满足条件的最小元素

```c++
class Solution {
public:
    bool containsNearbyAlmostDuplicate(vector<int>& nums, int k, int t) {
      set<int> window;
      int left = 0, right = 0;
      while(right < nums.size()){
        int num = nums[right];
        right++;
        
        //查找set内落在 [num -t, num + t]的元素 也就是>=num-t的第一个元素
        auto iter = window.lower_bound(max(num, INT_MIN + t) - t);
        if (iter != window.end() && *iter <= min(num, INT_MAX - t) + t) 
            return true;

        window.insert(num);
        if(window.size() > k){
          window.erase(nums[left]);
          left++;
        }
      }
      return 0;
    }
};
```

#### 方法2

`桶排序`我们可以把输入的元素按桶的个数，假设位t的间隔进行划分。
划分成：
第一个桶，存放[0...t]的数,
第二个桶，存放[t+1...2t],
...,
最后一个桶[(n-1)t...nt]。

举个例子:
若输入t = 3,nums = [1,5,9,1,5,8]，我们按照上面的思路，进行划分，因为0 < nums[0] = 1 < t，于是我们放入第一个桶，t + 1 = 4 < nums[1] = 5 < 2t = 6，于是放入第二个桶，其它同理，最后我们得到分布了数据的三个桶

[0...3]:1,1
[4...6]:5,5
[7...9]:9,8
因为我们是按大小为t来划分每一个桶的，所以如果两个数据落在了一个桶，我们就能够断言其绝对值之差是在t以内。

有一个问题，如果元素分布在两个桶中，那么它们的绝对值之差一定大于t吗？
显然，不是的。

若其中一个为上边界，另一个为下边界。如|7 - 6| = 1 <t∣7−6∣=1<t，可见分布在相邻桶的元素也可能会存在绝对值之差小于t的情况。

因此，综合上面的解释我们可以确定两种情况下：

任意两个元素落在了一个桶
分布在相邻桶的元素绝对值之差有可能小于t
于是乎(借助官方题解的代码)


```c++
// 第一种情况，分布在同一个桶
if (mp.count(id)) {
    return true;
}
// 第二种情况
// 判断相邻桶是否已经有元素
// 若有则判断是否绝对值之差在t内
if (mp.count(id - 1) && abs(x - mp[id - 1]) <= t) {
    return true;
}
if (mp.count(id + 1) && abs(x - mp[id + 1]) <= t) {
    return true;
}
```

### [1838. 最高频元素的频数](https://leetcode.cn/problems/frequency-of-the-most-frequent-element/)

难度中等222

元素的 **频数** 是该元素在一个数组中出现的次数。

给你一个整数数组 `nums` 和一个整数 `k` 。在一步操作中，你可以选择 `nums` 的一个下标，并将该下标对应元素的值增加 `1` 。

执行最多 `k` 次操作后，返回数组中最高频元素的 **最大可能频数** *。*

 

**示例 1：**

```
输入：nums = [1,2,4], k = 5
输出：3
解释：对第一个元素执行 3 次递增操作，对第二个元素执 2 次递增操作，此时 nums = [4,4,4] 。
4 是数组中最高频元素，频数是 3 。
```

**示例 2：**

```
输入：nums = [1,4,8,13], k = 5
输出：2
解释：存在多种最优解决方案：
- 对第一个元素执行 3 次递增操作，此时 nums = [4,4,8,13] 。4 是数组中最高频元素，频数是 2 。
- 对第二个元素执行 4 次递增操作，此时 nums = [1,8,8,13] 。8 是数组中最高频元素，频数是 2 。
- 对第三个元素执行 5 次递增操作，此时 nums = [1,4,13,13] 。13 是数组中最高频元素，频数是 2 。
```

#### 解法 不动脑子的滑动窗口

使用一个滑窗，看窗口内的k够不够用把所有元素变成同一个值，这个值肯定是窗口中元素的最大值 所以先对nums进行排序，每次变成最右侧的值就可以了

首先是我的蠢比解法，每次去检验k够不够用，对窗口进行遍历 

超时！

```c++
class Solution {
public:
    int maxFrequency(vector<int>& nums, int k) {
      //先排序， 这样每次窗口最右就是要变成的数
      sort(nums.begin(), nums.end());
      int n = nums.size();
      int left = 0, right = 0, ans = 0;
      while(right < n){
        int numR = nums[right];
        while(lastK(nums, left, right, k) < 0){
          left++;
        }
        ans = max(ans, right - left + 1);
        right++;
      }
      return ans;
    }
    //表示填充全部窗口元素到相同值 k剩余多少
    int lastK(vector<int>& nums, int left, int right, int k){
      int dst = nums[right];
      int res = 0;
      for(int i = left; i<right; i++){
        res += (dst - nums[i]);
      }
      return k - res;
    }
};
```

#### 解法 滑窗 直接统计差值

```c++
class Solution {
public:
    int maxFrequency(vector<int>& nums, int k) {
      //先排序， 这样每次窗口最右就是要变成的数
      sort(nums.begin(), nums.end());
      int n = nums.size();
      int left = 0, right = 1, ans = 1;
      long sum = 0;
      while(right < n){
        //窗口右移，元素变大后所有元素与最大值 新增的差值
        sum += (long)(nums[right] - nums[right-1])*(right - left);
        while(sum > k){
          sum -= nums[right] - nums[left];
          left++;
        }
        ans = max(ans, right - left + 1);
        right++;
      }
      return ans;
    }
};
```

---
date: '2022-05-25T10:42:00+08:00'
categories:
- 算法整理
tags:
- 算法总结
---

### [696. 计数二进制子串](https://leetcode.cn/problems/count-binary-substrings/)

难度简单455

给定一个字符串 `s`，统计并返回具有相同数量 `0` 和 `1` 的非空（连续）子字符串的数量，并且这些子字符串中的所有 `0` 和所有 `1` 都是成组连续的。

重复出现（不同位置）的子串也要统计它们出现的次数。

**示例 1：**

```
输入：s = "00110011"
输出：6
解释：6 个子串满足具有相同数量的连续 1 和 0 ："0011"、"01"、"1100"、"10"、"0011" 和 "01" 。
注意，一些重复出现的子串（不同位置）要统计它们出现的次数。
另外，"00110011" 不是有效的子串，因为所有的 0（还有 1 ）没有组合在一起。
```

**示例 2：**

```
输入：s = "10101"
输出：4
解释：有 4 个子串："10"、"01"、"10"、"01" ，具有相同数量的连续 1 和 0 。
```

#### 解法

脑筋急转弯 存储连续 0  1 的个数，两两取最小即可

```c++
class Solution {
public:
    int countBinarySubstrings(string s) {
      vector<int> all;
      char pre = s[0];
      int cnt = 1;
      for(int i = 1; i<s.size(); i++){
        if(s[i] == pre){
          cnt++;
        }else{
          all.push_back(cnt);
          cnt = 1;
          pre = s[i];
        }
      }
      all.push_back(cnt);
      // for(int nun : all)
      //   cout<<nun <<" ";
      int ans = 0;
      for(int i = 1; i<all.size(); i++){
        ans += min(all[i-1], all[i]);
      }
      return ans;
    }
};
```

### [5. 最长回文子串](https://leetcode.cn/problems/longest-palindromic-substring/)

[labuladong 题解](https://labuladong.github.io/article/?qno=5)[思路](https://leetcode.cn/problems/longest-palindromic-substring/#)

难度中等5256收藏分享切换为英文接收动态反馈

给你一个字符串 `s`，找到 `s` 中最长的回文子串。

 

**示例 1：**

```
输入：s = "babad"
输出："bab"
解释："aba" 同样是符合题意的答案。
```

**示例 2：**

```
输入：s = "cbbd"
输出："bb"
```

#### 解法 中心扩展

```c++
class Solution {
public:
    string expandCenter(string& s, int left, int right){
      while(left>= 0 && right<s.size() && s[left] == s[right]){
        left--;
        right++;
      }
      return s.substr(left + 1, right - 1 - left); 
    }
    string longestPalindrome(string s) {
      string ans;
      for(int i = 0; i<s.size(); i++){
        string p1 = expandCenter(s, i, i);
        string p2 = expandCenter(s, i, i+1);
        ans = ans.size()<p1.size()?p1:ans;
        ans = ans.size()<p2.size()?p2:ans;
      }
      return ans;
    }
};
```

### [647. 回文子串](https://leetcode.cn/problems/palindromic-substrings/)

难度中等880

给你一个字符串 `s` ，请你统计并返回这个字符串中 **回文子串** 的数目。

**回文字符串** 是正着读和倒过来读一样的字符串。

**子字符串** 是字符串中的由连续字符组成的一个序列。

具有不同开始位置或结束位置的子串，即使是由相同的字符组成，也会被视作不同的子串。

 

**示例 1：**

```
输入：s = "abc"
输出：3
解释：三个回文子串: "a", "b", "c"
```

**示例 2：**

```
输入：s = "aaa"
输出：6
解释：6个回文子串: "a", "a", "a", "aa", "aa", "aaa"
```

#### 中心扩展

```c++
class Solution {
public:
    // 中心扩展, 分别以一个字符为中心、两个字符为中心。 共2n-1种可能
    int countSubstrings(string s) {
      int n = s.size(), ans = 0;  // 默认一个字符的均为回文串
      for (int i = 0; i < n; i++) {   // 以一个字符为中心
        int left = i, right = i;
        while (left >= 0 && right < n) {
            if (s[left--] == s[right++]) 
              ans++;
            else break;
        }
      }
      for (int i = 0; i < n - 1; i++) {   // 以两个字符为中心
        int left = i, right = i+1;
        while(left>=0 && right<n){
          if(s[left--] == s[right++])
            ans++;
          else break;
        }
      }
      return ans;
    }
};
```

#### 精简

```c++
class Solution {
public:
    int countSubstrings(string s) {
        int n = s.size(), ans = 0;
        for (int i = 0; i < 2 * n - 1; ++i) {
            int l = i / 2, r = i / 2 + i % 2;
            while (l >= 0 && r < n && s[l] == s[r]) {
                --l;
                ++r;
                ++ans;
            }
        }
        return ans;
    }
};
```

### [1297. 子串的最大出现次数](https://leetcode.cn/problems/maximum-number-of-occurrences-of-a-substring/)

难度中等65收藏分享切换为英文接收动态反馈

给你一个字符串 `s` ，请你返回满足以下条件且出现次数最大的 **任意** 子串的出现次数：

- 子串中不同字母的数目必须小于等于 `maxLetters` 。
- 子串的长度必须大于等于 `minSize` 且小于等于 `maxSize` 。

 

**示例 1：**

```
输入：s = "aababcaab", maxLetters = 2, minSize = 3, maxSize = 4
输出：2
解释：子串 "aab" 在原字符串中出现了 2 次。
它满足所有的要求：2 个不同的字母，长度为 3 （在 minSize 和 maxSize 范围内）。
```

**示例 2：**

```
输入：s = "aaaa", maxLetters = 1, minSize = 3, maxSize = 3
输出：2
解释：子串 "aaa" 在原字符串中出现了 2 次，且它们有重叠部分。
```

#### 解法

因为比最小长度大的字串肯定包含最小长度字串，所以只需要遍历最小长度满足条件的字串即可

##### 长臭代码

```c++
class Solution {
public:
    //maxsize长度的字符串肯定包含minsize的字符串 
    //所以只需要统计最小长度的额字符串就可以
    int maxFreq(string s, int maxLetters, int minSize, int maxSize) {
      int n = s.size();
      //暴力得到所有满足条件的字串
      vector<string> all;
      for(int i = 0; i<n; i++){
        //for(int j = minSize; j<=maxSize; j++){
          if(i+minSize>n) continue;
          string temp = s.substr(i, minSize);
          //cout<<temp<<" ";
          all.push_back(temp);
        //}
        //cout<<endl;
      }
      unordered_map<string, int> mapp;
      int ans = 0;
      for(int i = 0; i<all.size(); i++){
        unordered_set<int> sett;
        for(auto ch : all[i]){
          sett.insert(ch);
        }
        if(sett.size() > maxLetters)
          continue;
        else mapp[all[i]]++;
        ans = max(ans, mapp[all[i]]);
      }
      return ans;
    }
};
```

##### 官方

```c++
class Solution {
public:
    int maxFreq(string s, int maxLetters, int minSize, int maxSize) {
        int n = s.size();
        unordered_map<string, int> occ;
        int ans = 0;
        for (int i = 0; i < n - minSize + 1; ++i) {
            string cur = s.substr(i, minSize);
            unordered_set<char> exist(cur.begin(), cur.end());
            if (exist.size() <= maxLetters) {
                string cur = s.substr(i, minSize);
                ++occ[cur];
                ans = max(ans, occ[cur]);
            }
        }
        return ans;
    }
};
```

### [467. 环绕字符串中唯一的子字符串](https://leetcode.cn/problems/unique-substrings-in-wraparound-string/)

难度中等317

把字符串 `s` 看作是 `“abcdefghijklmnopqrstuvwxyz”` 的无限环绕字符串，所以 `s` 看起来是这样的：

- `"...zabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcd...."` . 

现在给定另一个字符串 `p` 。返回 *`s` 中 **唯一** 的 `p` 的 **非空子串** 的数量* 。 

 

**示例 1:**

```
输入: p = "a"
输出: 1
解释: 字符串 s 中只有一个"a"子字符。
```

**示例 2:**

```
输入: p = "cac"
输出: 2
解释: 字符串 s 中的字符串“cac”只有两个子串“a”、“c”。.
```

**示例 3:**

```
输入: p = "zab"
输出: 6
解释: 在字符串 s 中有六个子串“z”、“a”、“b”、“za”、“ab”、“zab”。
```

```c++
class Solution {
public:
    int findSubstringInWraproundString(string p) {
        vector<int> dp(26);
        int k = 0;
        for (int i = 0; i < p.length(); ++i) {
            if (i && (p[i] - p[i - 1] + 26) % 26 == 1) { // 字符之差为 1 或 -25
                ++k;
            } else {
                k = 1;
            }
            dp[p[i] - 'a'] = max(dp[p[i] - 'a'], k);
        }
        return accumulate(dp.begin(), dp.end(), 0);
    }
};
```

---
date: '2021-12-02T19:23:40+08:00'
tags:
- leetcode
---

原地修改

class Solution {
public:
    vector&lt;int&gt; buildArray(vector&lt;int&gt;&amp; nums) {
        int n = nums.size();
        // 第一次遍历编码最终值
        for (int i = 0; i &lt; n; ++i){
            nums[i] += 1000 * (nums[nums[i]] % 1000);
        }
        // 第二次遍历修改为最终值
        for (int i = 0; i &lt; n; ++i){
            nums[i] /= 1000;
        }
        return nums;
    }
};

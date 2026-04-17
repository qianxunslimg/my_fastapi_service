---
date: '2022-04-13T10:42:00+08:00'
categories:
- 算法整理
tags:
- 算法总结
---

暂时懒得整理了 指个路

# [代码随想录 (programmercarl.com)](https://programmercarl.com/贪心算法理论基础.html#什么是贪心)

# 其他的贪心题

### [630. 课程表 III](https://leetcode-cn.com/problems/course-schedule-iii/)

难度困难326

这里有 `n` 门不同的在线课程，按从 `1` 到 `n` 编号。给你一个数组 `courses` ，其中 `courses[i] = [durationi, lastDayi]` 表示第 `i` 门课将会 **持续** 上 `durationi` 天课，并且必须在不晚于 `lastDayi` 的时候完成。

你的学期从第 `1` 天开始。且不能同时修读两门及两门以上的课程。

返回你最多可以修读的课程数目。

 

**示例 1：**

```
输入：courses = [[100, 200], [200, 1300], [1000, 1250], [2000, 3200]]
输出：3
解释：
这里一共有 4 门课程，但是你最多可以修 3 门：
首先，修第 1 门课，耗费 100 天，在第 100 天完成，在第 101 天开始下门课。
第二，修第 3 门课，耗费 1000 天，在第 1100 天完成，在第 1101 天开始下门课程。
第三，修第 2 门课，耗时 200 天，在第 1300 天完成。
第 4 门课现在不能修，因为将会在第 3300 天完成它，这已经超出了关闭日期。
```

#### 思路

什么是最优的？每个先排序 都想一遍， 看能不能实现最优

1. 持续时间越短，截止时间越晚的课程 越好  其中最最重要的截止时间
2. 实现上述：应该按一方排序 另一方使用优先级队列优化

#### 代码

```c++
class Solution {
public:
    int scheduleCourse(vector<vector<int>>& courses) {
        sort(courses.begin(), courses.end(), [](const auto& c0, const auto& c1) {
            return c0[1] < c1[1];
        });

        priority_queue<int> q;
        // 优先队列中所有课程的总时间
        int total = 0;

        for (const auto& course: courses) {
            int ti = course[0], di = course[1];
            if (total + ti <= di) {
                total += ti;
                q.push(ti);
            }
            else { //表示直接向上累计 失败
                //但是当前的截止时间大于堆内所以课程的截止时间
                //只要当前的持续时间 小于 堆内最大的持续时间 就应该替换
                //因为这个课程是最优的 持续时间短 截止时间晚
                if (!q.empty() && q.top() > ti) {
                    total -= q.top() - ti;
                    q.pop();
                    q.push(ti);
                }   
            }
        }
        return q.size();
    }
};
```

---
date: '2022-04-01T10:42:00+08:00'
categories:
- 算法整理
tags:
- 算法总结
---

### [剑指 Offer II 002. 二进制加法](https://leetcode-cn.com/problems/JFETK5/)

难度简单27

给定两个 01 字符串 `a` 和 `b` ，请计算它们的和，并以二进制字符串的形式输出。

输入为 **非空** 字符串且只包含数字 `1` 和 `0`。

 

**示例 1:**

```
输入: a = "11", b = "10"
输出: "101"
```

**示例 2:**

```
输入: a = "1010", b = "1011"
输出: "10101"
```

#### 思路

1. 模拟相加 注意下写法
2. 位运算

#### 代码

模拟

```c++
class Solution {
public:
    string addBinary(string a, string b) {
        string ans;
        reverse(a.begin(), a.end());
        reverse(b.begin(), b.end());
        int n = max(a.size(), b.size()), carry = 0;
        for(int i = 0; i<n; i++){
            carry+= i<a.size()?a[i] =='1':0;
            carry+= i<b.size()?b[i] =='1':0;
            ans += to_string(carry%2);
            carry/=2;
        }
        if (carry) {
            ans.push_back('1');
        }
        reverse(ans.begin(), ans.end());
        return ans;
    }
};
```

### [989. 数组形式的整数加法](https://leetcode-cn.com/problems/add-to-array-form-of-integer/)

难度简单191

整数的 **数组形式** `num` 是按照从左到右的顺序表示其数字的数组。

- 例如，对于 `num = 1321` ，数组形式是 `[1,3,2,1]` 。

给定 `num` ，整数的 **数组形式** ，和整数 `k` ，返回 *整数 `num + k` 的 **数组形式*** 。

 



**示例 1：**

```
输入：num = [1,2,0,0], k = 34
输出：[1,2,3,4]
解释：1200 + 34 = 1234
```

**示例 2：**

```
输入：num = [2,7,4], k = 181
输出：[4,5,5]
解释：274 + 181 = 455
```

**示例 3：**

```
输入：num = [2,1,5], k = 806
输出：[1,0,2,1]
解释：215 + 806 = 1021
```

#### 思路

k转为vector 按位相加

#### 代码

```c++
class Solution {
public:
    vector<int> addToArrayForm(vector<int>& num, int k) {
        vector<int> ans;
        vector<int> num2;
        while(k){
            int temp = k%10;
            k/=10;
            num2.push_back(temp);
        }
        reverse(num.begin(), num.end());
        int maxSize = max(num.size(), num2.size());
        int carry = 0;
        for(int i = 0; i<maxSize; i++){
            carry+=i<num.size()?num[i]:0;
            carry+=i<num2.size()?num2[i]:0;
            ans.push_back(carry%10);
            carry/=10;
        }
        if(carry) ans.push_back(1);
        reverse(ans.begin(), ans.end());
        return ans;
    }
};
```

### [66. 加一](https://leetcode-cn.com/problems/plus-one/)

难度简单972

给定一个由 **整数** 组成的 **非空** 数组所表示的非负整数，在该数的基础上加一。

最高位数字存放在数组的首位， 数组中每个元素只存储**单个**数字。

你可以假设除了整数 0 之外，这个整数不会以零开头。

 

**示例 1：**

```
输入：digits = [1,2,3]
输出：[1,2,4]
解释：输入数组表示数字 123。
```

**示例 2：**

```
输入：digits = [4,3,2,1]
输出：[4,3,2,2]
解释：输入数组表示数字 4321。
```

**示例 3：**

```
输入：digits = [0]
输出：[1]
```

#### 代码

```c++
//统一写法
class Solution {
public:
    vector<int> plusOne(vector<int>& digits) {
        vector<int> ans(digits.size());
        int carry = 0;
        for(int i = digits.size()-1; i>=0; i--){
            if(i == digits.size()-1){
                carry++;
            }
            carry+=digits[i];
            ans[i] = (carry%10);
            carry/=10;
        }
        if(carry) ans.insert(ans.begin(), 1);
        return ans;
    }
};

//原地修改
class Solution {
public:
    vector<int> plusOne(vector<int>& digits) {
        for(int i = digits.size()-1; i>=0; i--){
            if (digits[i] == 9){
                digits[i] = 0;
            }else{
                digits[i]++;
                break;
            }
        }

        if(digits[0] == 0){
            digits[0] = 1;
            digits.push_back(0); 
        }
        return digits;
    }
};
```

### [415. 字符串相加](https://leetcode-cn.com/problems/add-strings/)

难度简单534

给定两个字符串形式的非负整数 `num1` 和`num2` ，计算它们的和并同样以字符串形式返回。

你不能使用任何內建的用于处理大整数的库（比如 `BigInteger`）， 也不能直接将输入的字符串转换为整数形式。

 

**示例 1：**

```
输入：num1 = "11", num2 = "123"
输出："134"
```

#### 代码

```c++
class Solution {
public:
    string addStrings(string num1, string num2) {
        string ans = "";
        int maxSize = max(num1.size(), num2.size());
        reverse(num1.begin(), num1.end());
        reverse(num2.begin(), num2.end());
        int carry = 0;
        for(int i = 0; i<maxSize; i++){
            carry+=i<num1.size()?(num1[i] - '0'):0;
            carry+=i<num2.size()?(num2[i] - '0'):0;
            ans+=to_string(carry%10);a
            carry/=10;
        }
        if(carry) ans+="1";
        reverse(ans.begin(), ans.end());
        return ans;
    }
};
```

### [2. 两数相加](https://leetcode-cn.com/problems/add-two-numbers/) 链表

[思路](https://leetcode-cn.com/problems/add-two-numbers/#)

难度中等7812

给你两个 **非空** 的链表，表示两个非负的整数。它们每位数字都是按照 **逆序** 的方式存储的，并且每个节点只能存储 **一位** 数字。

请你将两个数相加，并以相同形式返回一个表示和的链表。

你可以假设除了数字 0 之外，这两个数都不会以 0 开头。

 

**示例 1：**

![img](./assets/addtwonumber1-2.jpg)

```
输入：l1 = [2,4,3], l2 = [5,6,4]
输出：[7,0,8]
解释：342 + 465 = 807.
```

**示例 2：**

```
输入：l1 = [0], l2 = [0]
输出：[0]
```

**示例 3：**

```
输入：l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
输出：[8,9,9,9,0,0,0,1]
```

#### 思路

就模拟吗

#### 代码

```c++
class Solution {
public:
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        ListNode* ans = new ListNode();
        ListNode* temp = ans;
        int carry = 0;
        while(l1 || l2){
            carry+= l1?l1->val:0;
            carry+= l2?l2->val:0;
            l1 = l1?l1->next:l1;
            l2 = l2?l2->next:l2;
            temp->next = new ListNode(carry%10);
            temp = temp->next;
            carry/=10;
        }
        if(carry) temp->next = new ListNode(1);
        return ans->next;
    }
};
```

### [剑指 Offer II 025. 链表中的两数相加](https://leetcode-cn.com/problems/lMSNwu/)

难度中等42

给定两个 **非空链表** `l1`和 `l2` 来代表两个非负整数。数字最高位位于链表开始位置。它们的每个节点只存储一位数字。将这两数相加会返回一个新的链表。

可以假设除了数字 0 之外，这两个数字都不会以零开头。

 

**示例1：**

![img](./assets/1626420025-fZfzMX-image-2.png)

```
输入：l1 = [7,2,4,3], l2 = [5,6,4]
输出：[7,8,0,7]
```

**示例2：**

```
输入：l1 = [2,4,3], l2 = [5,6,4]
输出：[8,0,7]
```

#### 思路

反转 套上面 再反转

#### 代码

```c++
class Solution {
public:
    ListNode* reverseList(ListNode* head){
        if(head == nullptr || head->next == nullptr)
            return head;
        ListNode* last = reverseList(head->next);
        head->next->next = head;
        head->next = nullptr;
        return last;
    }

    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        ListNode* L1 = reverseList(l1);
        ListNode* L2 = reverseList(l2);
        //这样写 不存在内存泄漏 同时 又有了一个可以直接移动的指针
        ListNode dumpyHead;  
        ListNode* pre = &dumpyHead;
        int carry = 0;
        while(L1 || L2){
            carry += L1?L1->val:0;
            carry += L2?L2->val:0;
            pre->next = new ListNode(carry%10);
            carry /= 10;         
            pre = pre->next;
            L1 = L1?L1->next:L1;
            L2 = L2?L2->next:L2;
        }
        //md又忘了
        if(carry) pre->next = new ListNode(1);
        return reverseList(dumpyHead.next);
    }
};
```

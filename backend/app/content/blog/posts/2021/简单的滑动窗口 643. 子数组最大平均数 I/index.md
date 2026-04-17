---
date: '2021-12-02T19:13:48+08:00'
tags:
- leetcode
---

给你一个由 n 个元素组成的整数数组 nums 和一个整数 k 。

请你找出平均数最大且 长度为 k 的连续子数组，并输出该最大平均数。

任何误差小于 10-5 的答案都将被视为正确答案。

&nbsp;

示例 1：

输入：nums = [1,12,-5,-6,50,3], k = 4
输出：12.75
解释：最大平均数 (12-5-6+50)/4 = 51/4 = 12.75
示例 2：

输入：nums = [5], k = 1
输出：5.00000

<div class="cnblogs_code">
<pre><span style="color: #008080;"> 1</span> <span style="color: #0000ff;">class</span><span style="color: #000000;"> Solution {
</span><span style="color: #008080;"> 2</span> <span style="color: #0000ff;">public</span><span style="color: #000000;">:
</span><span style="color: #008080;"> 3</span>     <span style="color: #008000;">//</span><span style="color: #008000;"> double findMaxAverage(vector&lt;int&gt;&amp; nums, int k) {
</span><span style="color: #008080;"> 4</span>     <span style="color: #008000;">//</span><span style="color: #008000;">     double res = -10000.0;
</span><span style="color: #008080;"> 5</span>     <span style="color: #008000;">//</span><span style="color: #008000;">     double sum = 0;
</span><span style="color: #008080;"> 6</span>     <span style="color: #008000;">//</span><span style="color: #008000;">     double ave;
</span><span style="color: #008080;"> 7</span>     <span style="color: #008000;">//</span><span style="color: #008000;">     for(int i = 0; i&lt;=nums.size()-k; i++){
</span><span style="color: #008080;"> 8</span>     <span style="color: #008000;">//</span><span style="color: #008000;">         if( i == 0){
</span><span style="color: #008080;"> 9</span>     <span style="color: #008000;">//</span><span style="color: #008000;">             for(int j = 0; j&lt;k; j++){
</span><span style="color: #008080;">10</span>     <span style="color: #008000;">//</span><span style="color: #008000;">                 sum+=nums[i+j];
</span><span style="color: #008080;">11</span>     <span style="color: #008000;">//</span><span style="color: #008000;">             }
</span><span style="color: #008080;">12</span>     <span style="color: #008000;">//</span><span style="color: #008000;">         }else{
</span><span style="color: #008080;">13</span>     <span style="color: #008000;">//</span><span style="color: #008000;">             sum-=nums[i-1];
</span><span style="color: #008080;">14</span>     <span style="color: #008000;">//</span><span style="color: #008000;">             sum+=nums[i+k-1];
</span><span style="color: #008080;">15</span>     <span style="color: #008000;">//</span><span style="color: #008000;">         }
</span><span style="color: #008080;">16</span>     <span style="color: #008000;">//</span><span style="color: #008000;">         ave = sum/k;
</span><span style="color: #008080;">17</span>     <span style="color: #008000;">//</span><span style="color: #008000;">         cout &lt;&lt;ave&lt;&lt;endl;
</span><span style="color: #008080;">18</span>     <span style="color: #008000;">//</span><span style="color: #008000;">         res = res&gt;ave?res:ave;
</span><span style="color: #008080;">19</span>     <span style="color: #008000;">//</span><span style="color: #008000;">     }
</span><span style="color: #008080;">20</span>     <span style="color: #008000;">//</span><span style="color: #008000;">     return res;
</span><span style="color: #008080;">21</span>     <span style="color: #008000;">//</span><span style="color: #008000;"> }</span>
<span style="color: #008080;">22</span>     <span style="color: #0000ff;">double</span> findMaxAverage(vector&lt;<span style="color: #0000ff;">int</span>&gt;&amp; nums, <span style="color: #0000ff;">int</span><span style="color: #000000;"> k) {
</span><span style="color: #008080;">23</span>         <span style="color: #0000ff;">int</span> sum = <span style="color: #800080;">0</span><span style="color: #000000;">;
</span><span style="color: #008080;">24</span>         <span style="color: #0000ff;">int</span> n =<span style="color: #000000;"> nums.size();
</span><span style="color: #008080;">25</span>         <span style="color: #0000ff;">for</span> (<span style="color: #0000ff;">int</span> i = <span style="color: #800080;">0</span>; i &lt; k; i++<span style="color: #000000;">) {
</span><span style="color: #008080;">26</span>             sum +=<span style="color: #000000;"> nums[i];
</span><span style="color: #008080;">27</span> <span style="color: #000000;">        }
</span><span style="color: #008080;">28</span>         <span style="color: #0000ff;">int</span> maxSum =<span style="color: #000000;"> sum;
</span><span style="color: #008080;">29</span>         <span style="color: #0000ff;">for</span> (<span style="color: #0000ff;">int</span> i = k; i &lt; n; i++<span style="color: #000000;">) {
</span><span style="color: #008080;">30</span>             sum = sum - nums[i - k] +<span style="color: #000000;"> nums[i];
</span><span style="color: #008080;">31</span>             maxSum =<span style="color: #000000;"> max(maxSum, sum);
</span><span style="color: #008080;">32</span> <span style="color: #000000;">        }
</span><span style="color: #008080;">33</span>         <span style="color: #0000ff;">return</span> static_cast&lt;<span style="color: #0000ff;">double</span>&gt;(maxSum) /<span style="color: #000000;"> k;
</span><span style="color: #008080;">34</span> <span style="color: #000000;">    }
</span><span style="color: #008080;">35</span> 
<span style="color: #008080;">36</span> };</pre>
</div>

&nbsp;

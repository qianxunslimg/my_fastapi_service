---
date: '2021-12-02T19:11:08+08:00'
tags:
- leetcode
---

包含整数的二维矩阵 M 表示一个图片的灰度。你需要设计一个平滑器来让每一个单元的灰度成为平均灰度&nbsp;(向下舍入) ，平均灰度的计算是周围的8个单元和它本身的值求平均，如果周围的单元格不足八个，则尽可能多的利用它们。

示例 1:

输入:
[[1,1,1],
 [1,0,1],
 [1,1,1]]
输出:
[[0, 0, 0],
 [0, 0, 0],
 [0, 0, 0]]
解释:
对于点 (0,0), (0,2), (2,0), (2,2): 平均(3/4) = 平均(0.75) = 0
对于点 (0,1), (1,0), (1,2), (2,1): 平均(5/6) = 平均(0.83333333) = 0
对于点 (1,1): 平均(8/9) = 平均(0.88888889) = 0

<div class="cnblogs_code">
<pre><span style="color: #008080;"> 1</span>     vector&lt;vector&lt;<span style="color: #0000ff;">int</span>&gt;&gt; imageSmoother(vector&lt;vector&lt;<span style="color: #0000ff;">int</span>&gt;&gt;&amp;<span style="color: #000000;"> img) {
</span><span style="color: #008080;"> 2</span>         <span style="color: #0000ff;">const</span> <span style="color: #0000ff;">int</span> n =<span style="color: #000000;"> img.size();
</span><span style="color: #008080;"> 3</span>         <span style="color: #0000ff;">const</span> <span style="color: #0000ff;">int</span> m = img[<span style="color: #800080;">0</span><span style="color: #000000;">].size();
</span><span style="color: #008080;"> 4</span>         vector&lt;vector&lt;<span style="color: #0000ff;">int</span>&gt;&gt; ans(n, vector&lt;<span style="color: #0000ff;">int</span>&gt;<span style="color: #000000;">(m));
</span><span style="color: #008080;"> 5</span>         <span style="color: #0000ff;">for</span>(<span style="color: #0000ff;">int</span> i = <span style="color: #800080;">0</span>; i &lt; n; ++i){  <span style="color: #008000;">//</span><span style="color: #008000;">遍历每一个点</span>
<span style="color: #008080;"> 6</span>             <span style="color: #0000ff;">for</span>(<span style="color: #0000ff;">int</span> j = <span style="color: #800080;">0</span>; j &lt; m; ++<span style="color: #000000;">j){
</span><span style="color: #008080;"> 7</span>                 <span style="color: #0000ff;">int</span> sum = <span style="color: #800080;">0</span>, num = <span style="color: #800080;">0</span><span style="color: #000000;">;
</span><span style="color: #008080;"> 8</span>                 <span style="color: #0000ff;">for</span>(<span style="color: #0000ff;">int</span> k = -<span style="color: #800080;">1</span>; k &lt;= <span style="color: #800080;">1</span>; ++k){  <span style="color: #008000;">//</span><span style="color: #008000;">遍历周围的格子</span>
<span style="color: #008080;"> 9</span>                     <span style="color: #0000ff;">for</span>(<span style="color: #0000ff;">int</span> l = -<span style="color: #800080;">1</span>; l &lt;= <span style="color: #800080;">1</span>; ++l){   <span style="color: #008000;">//</span><span style="color: #008000;">判断是否出界</span>
<span style="color: #008080;">10</span>                         <span style="color: #0000ff;">if</span>(i + k &gt;= <span style="color: #800080;">0</span> &amp;&amp; i + k &lt; n &amp;&amp; j + l &gt;= <span style="color: #800080;">0</span> &amp;&amp; j + l &lt;<span style="color: #000000;"> m){
</span><span style="color: #008080;">11</span>                             ++num; <span style="color: #008000;">//</span><span style="color: #008000;">没有出界，格子个数+1</span>
<span style="color: #008080;">12</span>                             sum += img[i + k][j + l]; <span style="color: #008000;">//</span><span style="color: #008000;">计算总和</span>
<span style="color: #008080;">13</span> <span style="color: #000000;">                        }
</span><span style="color: #008080;">14</span> <span style="color: #000000;">                    }
</span><span style="color: #008080;">15</span> <span style="color: #000000;">                }
</span><span style="color: #008080;">16</span>                 ans[i][j] = sum / num; <span style="color: #008000;">//</span><span style="color: #008000;">计算平均值</span>
<span style="color: #008080;">17</span> <span style="color: #000000;">            }
</span><span style="color: #008080;">18</span> <span style="color: #000000;">        }
</span><span style="color: #008080;">19</span>         <span style="color: #0000ff;">return</span><span style="color: #000000;"> ans;
</span><span style="color: #008080;">20</span>     }</pre>
</div>

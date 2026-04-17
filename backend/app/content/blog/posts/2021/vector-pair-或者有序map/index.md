---
date: '2021-12-02T19:26:18+08:00'
title: vector<pair>或者有序map
tags:
- leetcode
---

功能相同

<div class="cnblogs_code">
<pre><span style="color: #008080;"> 1</span>   <span style="color: #0000ff;">static</span> <span style="color: #0000ff;">bool</span> sortPair(pair&lt;<span style="color: #0000ff;">int</span>, <span style="color: #0000ff;">int</span>&gt; a, pair&lt;<span style="color: #0000ff;">int</span>, <span style="color: #0000ff;">int</span>&gt;<span style="color: #000000;"> b) {
</span><span style="color: #008080;"> 2</span>     <span style="color: #0000ff;">return</span> a.second &gt;<span style="color: #000000;"> b.second;
</span><span style="color: #008080;"> 3</span> <span style="color: #000000;">  }
</span><span style="color: #008080;"> 4</span>   vector&lt;<span style="color: #0000ff;">string</span>&gt; findRelativeRanks(vector&lt;<span style="color: #0000ff;">int</span>&gt; &amp;<span style="color: #000000;">score) {
</span><span style="color: #008080;"> 5</span>     vector&lt;<span style="color: #0000ff;">string</span>&gt;<span style="color: #000000;"> res(score.size());
</span><span style="color: #008080;"> 6</span> 
<span style="color: #008080;"> 7</span>     vector&lt;pair&lt;<span style="color: #0000ff;">int</span>, <span style="color: #0000ff;">int</span>&gt;&gt;<span style="color: #000000;"> pairr;
</span><span style="color: #008080;"> 8</span> 
<span style="color: #008080;"> 9</span>     <span style="color: #0000ff;">for</span> (<span style="color: #0000ff;">int</span> i = <span style="color: #800080;">0</span>; i &lt; score.size(); i++<span style="color: #000000;">) {
</span><span style="color: #008080;">10</span>       pairr.push_back(pair&lt;<span style="color: #0000ff;">int</span>, <span style="color: #0000ff;">int</span>&gt;<span style="color: #000000;">(i, score[i]));
</span><span style="color: #008080;">11</span> <span style="color: #000000;">    }
</span><span style="color: #008080;">12</span> 
<span style="color: #008080;">13</span> <span style="color: #000000;">    sort(pairr.begin(), pairr.end(), sortPair);
</span><span style="color: #008080;">14</span>     <span style="color: #0000ff;">for</span> (<span style="color: #0000ff;">int</span> i = <span style="color: #800080;">0</span>; i &lt; pairr.size(); i++<span style="color: #000000;">) {
</span><span style="color: #008080;">15</span>       <span style="color: #0000ff;">switch</span><span style="color: #000000;"> (i) {
</span><span style="color: #008080;">16</span>       <span style="color: #0000ff;">case</span> <span style="color: #800080;">0</span><span style="color: #000000;">:
</span><span style="color: #008080;">17</span>         res[pairr[i].first] = <span style="color: #800000;">"</span><span style="color: #800000;">Gold Medal</span><span style="color: #800000;">"</span><span style="color: #000000;">;
</span><span style="color: #008080;">18</span>         <span style="color: #0000ff;">break</span><span style="color: #000000;">;
</span><span style="color: #008080;">19</span>       <span style="color: #0000ff;">case</span> <span style="color: #800080;">1</span><span style="color: #000000;">:
</span><span style="color: #008080;">20</span>         res[pairr[i].first] = <span style="color: #800000;">"</span><span style="color: #800000;">Silver Medal</span><span style="color: #800000;">"</span><span style="color: #000000;">;
</span><span style="color: #008080;">21</span>         <span style="color: #0000ff;">break</span><span style="color: #000000;">;
</span><span style="color: #008080;">22</span>       <span style="color: #0000ff;">case</span> <span style="color: #800080;">2</span><span style="color: #000000;">:
</span><span style="color: #008080;">23</span>         res[pairr[i].first] = <span style="color: #800000;">"</span><span style="color: #800000;">Bronze Medal</span><span style="color: #800000;">"</span><span style="color: #000000;">;
</span><span style="color: #008080;">24</span>         <span style="color: #0000ff;">break</span><span style="color: #000000;">;
</span><span style="color: #008080;">25</span>       <span style="color: #0000ff;">default</span><span style="color: #000000;">:
</span><span style="color: #008080;">26</span>         res[pairr[i].first] = to_string(i + <span style="color: #800080;">1</span><span style="color: #000000;">);
</span><span style="color: #008080;">27</span>         <span style="color: #0000ff;">break</span><span style="color: #000000;">;
</span><span style="color: #008080;">28</span> <span style="color: #000000;">      }
</span><span style="color: #008080;">29</span> <span style="color: #000000;">    }
</span><span style="color: #008080;">30</span>     <span style="color: #0000ff;">return</span><span style="color: #000000;"> res;
</span><span style="color: #008080;">31</span>   }</pre>
</div>
<div class="cnblogs_code">
<pre><span style="color: #008080;"> 1</span>     vector&lt;<span style="color: #0000ff;">string</span>&gt; findRelativeRanks(vector&lt;<span style="color: #0000ff;">int</span>&gt;&amp;<span style="color: #000000;"> score) {
</span><span style="color: #008080;"> 2</span>         <span style="color: #0000ff;">int</span> n=<span style="color: #000000;">score.size();
</span><span style="color: #008080;"> 3</span>         map&lt;<span style="color: #0000ff;">int</span>,<span style="color: #0000ff;">int</span>,greater&lt;<span style="color: #0000ff;">int</span>&gt;&gt;<span style="color: #000000;">num2index;
</span><span style="color: #008080;"> 4</span>         <span style="color: #0000ff;">for</span>(<span style="color: #0000ff;">int</span> i=<span style="color: #800080;">0</span>;i&lt;n;i++)num2index[score[i]]=<span style="color: #000000;">i;
</span><span style="color: #008080;"> 5</span>         vector&lt;<span style="color: #0000ff;">string</span>&gt;<span style="color: #000000;">ans(n);
</span><span style="color: #008080;"> 6</span>         <span style="color: #0000ff;">int</span> i=<span style="color: #800080;">0</span><span style="color: #000000;">;
</span><span style="color: #008080;"> 7</span>         <span style="color: #0000ff;">for</span><span style="color: #000000;">(auto mPair:num2index){
</span><span style="color: #008080;"> 8</span>             <span style="color: #0000ff;">int</span> index=<span style="color: #000000;">mPair.second;
</span><span style="color: #008080;"> 9</span>             <span style="color: #0000ff;">if</span>(i==<span style="color: #800080;">0</span><span style="color: #000000;">){
</span><span style="color: #008080;">10</span>                 ans[index]=<span style="color: #800000;">"</span><span style="color: #800000;">Gold Medal</span><span style="color: #800000;">"</span><span style="color: #000000;">;
</span><span style="color: #008080;">11</span>             }<span style="color: #0000ff;">else</span> <span style="color: #0000ff;">if</span>(i==<span style="color: #800080;">1</span><span style="color: #000000;">){
</span><span style="color: #008080;">12</span>                 ans[index]=<span style="color: #800000;">"</span><span style="color: #800000;">Silver Medal</span><span style="color: #800000;">"</span><span style="color: #000000;">;
</span><span style="color: #008080;">13</span>             }<span style="color: #0000ff;">else</span> <span style="color: #0000ff;">if</span>(i==<span style="color: #800080;">2</span><span style="color: #000000;">){
</span><span style="color: #008080;">14</span>                 ans[index]=<span style="color: #800000;">"</span><span style="color: #800000;">Bronze Medal</span><span style="color: #800000;">"</span><span style="color: #000000;">;
</span><span style="color: #008080;">15</span>             }<span style="color: #0000ff;">else</span> ans[index]+=to_string(i+<span style="color: #800080;">1</span><span style="color: #000000;">);
</span><span style="color: #008080;">16</span>             i++<span style="color: #000000;">;
</span><span style="color: #008080;">17</span> <span style="color: #000000;">        }
</span><span style="color: #008080;">18</span>         <span style="color: #0000ff;">return</span><span style="color: #000000;"> ans;
</span><span style="color: #008080;">19</span>     }</pre>
</div>

&nbsp;

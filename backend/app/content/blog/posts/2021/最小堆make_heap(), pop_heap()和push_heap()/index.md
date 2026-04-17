---
date: '2021-12-02T19:28:59+08:00'
tags:
- leetcode
---

![](./assets/2092994-20211114224004410-1010288954-2.png)

&nbsp;

&nbsp;

&nbsp;

make_heap
在容器范围内，就地建堆，保证最大值在所给范围的最前面，其他值的位置不确定

pop_heap
将堆顶(所给范围的最前面)元素移动到所给范围的最后，并且将新的最大值置于所给范围的最前面

push_heap
当已建堆的容器范围内有新的元素插入末尾后，应当调用push_heap将该元素插入堆中。

<div class="cnblogs_code">
<pre><span style="color: #008080;"> 1</span> #include&lt;iostream&gt;
<span style="color: #008080;"> 2</span> #include&lt;vector&gt;
<span style="color: #008080;"> 3</span> #include&lt;ctime&gt;
<span style="color: #008080;"> 4</span> #include&lt;deque&gt;
<span style="color: #008080;"> 5</span> #include&lt;list&gt;
<span style="color: #008080;"> 6</span> #include&lt;algorithm&gt;
<span style="color: #008080;"> 7</span> #include&lt;queue&gt;
<span style="color: #008080;"> 8</span> #include&lt;functional&gt;<span style="color: #008000;">//</span><span style="color: #008000;">greater使用</span>
<span style="color: #008080;"> 9</span>  
<span style="color: #008080;">10</span> <span style="color: #0000ff;">using</span> <span style="color: #0000ff;">namespace</span><span style="color: #000000;"> std;
</span><span style="color: #008080;">11</span>  
<span style="color: #008080;">12</span> <span style="color: #0000ff;">void</span> print(vector&lt;<span style="color: #0000ff;">int</span>&gt;<span style="color: #000000;"> a) {
</span><span style="color: #008080;">13</span>     <span style="color: #0000ff;">for</span> (<span style="color: #0000ff;">int</span> i = <span style="color: #800080;">0</span>; i &lt; a.size(); i++<span style="color: #000000;">) {
</span><span style="color: #008080;">14</span>         cout &lt;&lt; a[i] &lt;&lt; <span style="color: #800000;">"</span> <span style="color: #800000;">"</span><span style="color: #000000;">;
</span><span style="color: #008080;">15</span> <span style="color: #000000;">    }
</span><span style="color: #008080;">16</span>     cout &lt;&lt;<span style="color: #000000;"> endl;
</span><span style="color: #008080;">17</span> <span style="color: #000000;">}
</span><span style="color: #008080;">18</span>  
<span style="color: #008080;">19</span> <span style="color: #0000ff;">int</span><span style="color: #000000;"> main() {
</span><span style="color: #008080;">20</span>  
<span style="color: #008080;">21</span>     <span style="color: #008000;">//</span><span style="color: #008000;">堆排序算法（heapsort）
</span><span style="color: #008080;">22</span>     <span style="color: #008000;">//</span><span style="color: #008000;">make_heap();
</span><span style="color: #008080;">23</span>     <span style="color: #008000;">//</span><span style="color: #008000;">push_heap()
</span><span style="color: #008080;">24</span>     <span style="color: #008000;">//</span><span style="color: #008000;">sort_heap()
</span><span style="color: #008080;">25</span>     <span style="color: #008000;">//</span><span style="color: #008000;">pop_heap()
</span><span style="color: #008080;">26</span>     <span style="color: #008000;">//</span><span style="color: #008000;">堆就是一种特殊的二叉树，最关心的就是根
</span><span style="color: #008080;">27</span>     <span style="color: #008000;">//</span><span style="color: #008000;">大根堆，小根堆</span>
<span style="color: #008080;">28</span>  
<span style="color: #008080;">29</span>     vector&lt;<span style="color: #0000ff;">int</span>&gt; ivec{<span style="color: #800080;">3</span>,<span style="color: #800080;">4</span>,<span style="color: #800080;">5</span>,<span style="color: #800080;">6</span>,<span style="color: #800080;">7</span>,<span style="color: #800080;">5</span>,<span style="color: #800080;">6</span>,<span style="color: #800080;">7</span>,<span style="color: #800080;">8</span>,<span style="color: #800080;">9</span>,<span style="color: #800080;">1</span>,<span style="color: #800080;">2</span>,<span style="color: #800080;">3</span>,<span style="color: #800080;">4</span><span style="color: #000000;">};
</span><span style="color: #008080;">30</span> <span style="color: #000000;">    print(ivec);
</span><span style="color: #008080;">31</span>     <span style="color: #008000;">//</span><span style="color: #008000;">向量里所有的数据变成一个堆</span>
<span style="color: #008080;">32</span>  
<span style="color: #008080;">33</span> <span style="color: #000000;">    make_heap(ivec.begin(), ivec.end());
</span><span style="color: #008080;">34</span> <span style="color: #000000;">    print(ivec);
</span><span style="color: #008080;">35</span>  
<span style="color: #008080;">36</span>     pop_heap(ivec.begin(), ivec.end());<span style="color: #008000;">//</span><span style="color: #008000;">最大的数据取走，但是并没s有删除
</span><span style="color: #008080;">37</span>     <span style="color: #008000;">//</span><span style="color: #008000;">把最大的数据放在结尾，剩下的元素排成一个堆</span>
<span style="color: #008080;">38</span> <span style="color: #000000;">    print(ivec);
</span><span style="color: #008080;">39</span> <span style="color: #000000;">    ivec.pop_back();
</span><span style="color: #008080;">40</span>     <span style="color: #008000;">//</span><span style="color: #008000;">push_heap 使用首先要先把数据加在向量里</span>
<span style="color: #008080;">41</span>  
<span style="color: #008080;">42</span>     ivec.push_back(<span style="color: #800080;">17</span><span style="color: #000000;">);
</span><span style="color: #008080;">43</span> <span style="color: #000000;">    make_heap(ivec.begin(), ivec.end());
</span><span style="color: #008080;">44</span> <span style="color: #000000;">    print(ivec);
</span><span style="color: #008080;">45</span>  
<span style="color: #008080;">46</span>     <span style="color: #008000;">//</span><span style="color: #008000;">sort_heap 把堆变成不是堆,普通的排序</span>
<span style="color: #008080;">47</span> <span style="color: #000000;">    sort_heap(ivec.begin(), ivec.end());
</span><span style="color: #008080;">48</span> <span style="color: #000000;">    print(ivec);
</span><span style="color: #008080;">49</span>  
<span style="color: #008080;">50</span>     system(<span style="color: #800000;">"</span><span style="color: #800000;">pause</span><span style="color: #800000;">"</span><span style="color: #000000;">);
</span><span style="color: #008080;">51</span> }</pre>
</div>


![](./assets/2092994-20211114224224870-302527741-2.png)

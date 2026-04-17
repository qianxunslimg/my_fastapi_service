---
date: '2021-09-01T19:32:31+08:00'
tags:
- 开发随笔
---

<div class="com-markdown-collpase-main">
<div class="rno-markdown J-articleContent">
<pre class="prism-token token  language-javascript">自己查到的三处说法的对比：</pre>
<pre class="prism-token token  language-javascript">一、转自知道的答案：https<span class="token operator">:<span class="token operator">/<span class="token operator">/zhidao<span class="token punctuation">.baidu<span class="token punctuation">.com<span class="token operator">/question<span class="token operator">/<span class="token number">323662520.html<span class="token operator">?qq<span class="token operator">-pf<span class="token operator">-to<span class="token operator">=pcqq<span class="token punctuation">.c2c#</span></span></span></span></span></span></span></span></span></span></span></span></span></pre>
<pre class="prism-token token  language-javascript"><span class="token function">vector，clear<span class="token punctuation">(<span class="token punctuation">)<span class="token function">并不真正释放内存<span class="token punctuation">(这是为优化效率所做的事<span class="token punctuation">)<span class="token function">，clear实际所做的是为vector中所保存的所有对象调用析构函数<span class="token punctuation">(如果有的话<span class="token punctuation">)<span class="token punctuation">,然后初始化size这些东西，让觉得把所有的对象清除了。
　　真正释放内存是在vector的析构函数里进行的，所以一旦超出vector的作用域（如函数返回<span class="token punctuation">)，首先它所保存的所有对象会被析构，然后会调用allocator中的deallocate函数回收对象本身的内存。
　　所以，某些编译器clear后还能访问到对象数据（因为它根本没清除），在一些比较新的<span class="token constant">C<span class="token operator">++<span class="token function">编译器上<span class="token punctuation">(例如<span class="token constant">VS2008<span class="token punctuation">)<span class="token function">，当进行数组引用时<span class="token punctuation">(例如a<span class="token punctuation">[<span class="token number">2<span class="token punctuation">]这种用法<span class="token punctuation">)<span class="token punctuation">,<span class="token constant">STL库中会有一些check函数根据当前容器的size值来判断下标引用是否超出范围，如果超出，则会执行这样一句：
　　<span class="token function">_THROW<span class="token punctuation">(out_of_range<span class="token punctuation">, <span class="token string">"invalid vector&lt;T&gt; subscript"<span class="token punctuation">)<span class="token punctuation">;
　　即抛出一个越界异常，clear后没有捕获异常，程序在新编译器编译后就会崩溃掉。</span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></pre>
<pre class="prism-token token  language-javascript"><span class="token operator">--<span class="token operator">--<span class="token operator">--<span class="token operator">--<span class="token operator">--<span class="token operator">--<span class="token operator">--<span class="token operator">--<span class="token operator">--<span class="token operator">--<span class="token operator">--<span class="token operator">--<span class="token operator">-分割线<span class="token operator">--<span class="token operator">--<span class="token operator">--<span class="token operator">--<span class="token operator">--<span class="token operator">--<span class="token operator">--<span class="token operator">--<span class="token operator">--<span class="token operator">--<span class="token operator">--<span class="token operator">--<span class="token operator">--<span class="token operator">--<span class="token operator">--<span class="token operator">--<span class="token operator">--<span class="token operator">--<span class="token operator">--<span class="token operator">--<span class="token operator">--<span class="token operator">--<span class="token operator">--<span class="token operator">--<span class="token operator">--<span class="token operator">--<span class="token operator">--<span class="token operator">--<span class="token operator">--<span class="token operator">--<span class="token operator">--</span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></pre>


二、转自博客：https://www.cnblogs.com/summerRQ/articles/2407974.html

vector ： C++ STL中的顺序容器，封装数组

1. vector容器的内存自增长&nbsp;

与其他容器不同，其内存空间只会增长，不会减小。先来看看"C++ Primer"中怎么说：为了支持快速的随机访问，vector容器的元素以连续方式存放，每一个元素都紧挨着前一个元素存储。设想一下，当vector添加一个元素时，为了满足连续存放这个特性，都需要重新分配空间、拷贝元素、撤销旧空间，这样性能难以接受。因此STL实现者在对vector进行内存分配时，其实际分配的容量要比当前所需的空间多一些。就是说，vector容器预留了一些额外的存储区，用于存放新添加的元素，这样就不必为每个新元素重新分配整个容器的内存空间。

关于vector的内存空间，有两个函数需要注意：size()成员指当前拥有的元素个数；capacity()成员指当前(容器必须分配新存储空间之前)可以存储的元素个数。reserve()成员可以用来控制容器的预留空间。vector另外一个特性在于它的内存空间会自增长，每当vector容器不得不分配新的存储空间时，会以加倍当前容量的分配策略实现重新分配。例如，当前capacity为50，当添加第51个元素时，预留空间不够用了，vector容器会重新分配大小为100的内存空间，作为新连续存储的位置。

2.&nbsp;vector内存释放

由于vector的内存占用空间只增不减，比如你首先分配了10,000个字节，然后erase掉后面9,999个，留下一个有效元素，但是内存占用仍为10,000个。所有内存空间是在vector析构时候才能被系统回收。empty()用来检测容器是否为空的，clear()可以清空所有元素。但是即使clear()，vector所占用的内存空间依然如故，无法保证内存的回收。

如果需要空间动态缩小，可以考虑使用deque。如果非vector不可，可以用swap()来帮助你释放内存。具体方法如下：

<pre class="prism-token token  language-javascript">vector<span class="token operator">&lt;int<span class="token operator">&gt; nums<span class="token punctuation">; 
nums<span class="token punctuation">.<span class="token function">push_back<span class="token punctuation">(<span class="token number">1<span class="token punctuation">)<span class="token punctuation">;
nums<span class="token punctuation">.<span class="token function">push_back<span class="token punctuation">(<span class="token number">1<span class="token punctuation">)<span class="token punctuation">;
nums<span class="token punctuation">.<span class="token function">push_back<span class="token punctuation">(<span class="token number">2<span class="token punctuation">)<span class="token punctuation">;
nums<span class="token punctuation">.<span class="token function">push_back<span class="token punctuation">(<span class="token number">2<span class="token punctuation">)<span class="token punctuation">; 
vector<span class="token operator">&lt;int<span class="token operator">&gt;<span class="token punctuation">(<span class="token punctuation">)<span class="token punctuation">.<span class="token function">swap<span class="token punctuation">(nums<span class="token punctuation">)<span class="token punctuation">; <span class="token comment">//或者nums.swap(vector&lt;int&gt; ())</span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></pre>


或者如下所示，使用一对大括号，意思一样的：

<pre class="prism-token token  language-javascript"><span class="token comment">//加一对大括号是可以让tmp退出{}的时候自动析构
<span class="token punctuation">{ 
    std<span class="token operator">:<span class="token operator">:vector<span class="token operator">&lt;int<span class="token operator">&gt; tmp <span class="token operator">=   nums<span class="token punctuation">;  
    nums<span class="token punctuation">.<span class="token function">swap<span class="token punctuation">(tmp<span class="token punctuation">)<span class="token punctuation">; 
<span class="token punctuation">}</span></span></span></span></span></span></span></span></span></span></span></span></span></span></pre>


&nbsp;swap()是交换函数，使vector离开其自身的作用域，从而强制释放vector所占的内存空间，总而言之，释放vector内存最简单的方法是vector&lt;int&gt;.swap(nums)。当时如果nums是一个类的成员，不能把vector&lt;int&gt;.swap(nums)写进类的析构函数中，否则会导致double free or corruption (fasttop)的错误，原因可能是重复释放内存。标准解决方法如下：

<pre class="prism-token token  language-javascript">template <span class="token operator">&lt; <span class="token keyword">class <span class="token class-name">T <span class="token operator">&gt;
<span class="token keyword">void <span class="token function">ClearVector<span class="token punctuation">( <span class="token parameter">vector<span class="token operator">&lt; <span class="token constant">T <span class="token operator">&gt;<span class="token operator">&amp; vt <span class="token punctuation">) 
<span class="token punctuation">{
    vector<span class="token operator">&lt; <span class="token constant">T <span class="token operator">&gt; vtTemp<span class="token punctuation">; 
    veTemp<span class="token punctuation">.<span class="token function">swap<span class="token punctuation">( vt <span class="token punctuation">)<span class="token punctuation">;
<span class="token punctuation">}</span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></pre>


3. 利用vector释放指针

如果vector中存放的是指针，那么当vector销毁时，这些指针指向的对象不会被销毁，那么内存就不会被释放。如下面这种情况，vector中的元素时由new操作动态申请出来的对象指针：

<pre class="prism-token token  language-javascript">#include <span class="token operator">&lt;vector<span class="token operator">&gt; 
using namespace std<span class="token punctuation">; 
vector<span class="token operator">&lt;<span class="token keyword">void <span class="token operator">*<span class="token operator">&gt; v<span class="token punctuation">;</span></span></span></span></span></span></span></span></pre>


每次new之后调用v.push_back()该指针，在程序退出或者根据需要，用以下代码进行内存的释放：&nbsp;

<pre class="prism-token token  language-javascript"><span class="token keyword">for <span class="token punctuation">(vector<span class="token operator">&lt;<span class="token keyword">void <span class="token operator">*<span class="token operator">&gt;<span class="token operator">:<span class="token operator">:iterator it <span class="token operator">= v<span class="token punctuation">.<span class="token function">begin<span class="token punctuation">(<span class="token punctuation">)<span class="token punctuation">; it <span class="token operator">!= v<span class="token punctuation">.<span class="token function">end<span class="token punctuation">(<span class="token punctuation">)<span class="token punctuation">; it <span class="token operator">++<span class="token punctuation">) 
    <span class="token keyword">if <span class="token punctuation">(<span class="token constant">NULL <span class="token operator">!= <span class="token operator">*it<span class="token punctuation">) 
    <span class="token punctuation">{
        <span class="token keyword">delete <span class="token operator">*it<span class="token punctuation">; 
        <span class="token operator">*it <span class="token operator">= <span class="token constant">NULL<span class="token punctuation">;
    <span class="token punctuation">}
v<span class="token punctuation">.<span class="token function">clear<span class="token punctuation">(<span class="token punctuation">)<span class="token punctuation">;</span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></span></pre>


三、转自博客：https://blog.csdn.net/hk_john/article/details/72463318

最近经常用到vector容器，发现它的clear（）函数有点意思，经过验证之后进行一下总结。

clear（）函数的调用方式是，vector&lt;datatype&gt; temp（50）;//定义了50个datatype大小的空间。temp.clear();

作用：将会清空temp中的所有元素，包括temp开辟的空间（size），但是capacity会保留，即不可以以temp[1]这种形式赋初值，只能通过temp.push_back(value)的形式赋初值。

同样对于vector&lt;vector&lt;datatype&gt; &gt; temp1（50）这种类型的变量，使用temp1.clear()之后将会不能用temp1[1].push_back(value)进行赋初值，只能使用temp1.push_back(temp)；的形式。

下面的代码是可以运行的。

<pre class="prism-token token  language-javascript"></pre>

1.  #include &lt;iostream&gt;
2.  #include&lt;vector&gt;
    3.4.  using namespace std;
    5.6.  int main(){
    7.8.  vector&lt;vector&lt;int&gt;&gt; test(50);
3.  vector&lt;int&gt; temp;
4.  test[10].push_back(1);
5.  cout&lt;&lt;test[10][0]&lt;&lt;endl;
6.  test.clear();
    13.14.15.  for(int i=0;i&lt;51;i++)
7.  test.push_back(temp);
    17.18.  system("pause");
8.  return 0;
9.  }

但是这样是会越界错误的。

<pre class="prism-token token  language-javascript"></pre>

1.  #include &lt;iostream&gt;
2.  #include&lt;vector&gt;
    3.4.  using namespace std;
    5.6.  int main(){
    7.8.  vector&lt;vector&lt;int&gt;&gt; test(50);
3.  vector&lt;int&gt; temp;
4.  test[10].push_back(1);
5.  cout&lt;&lt;test[10][0]&lt;&lt;endl;
6.  test.clear();
    13.14.  for(int i=0;i&lt;50;i++)
7.  test[i].push_back(1);
    16.17.  system("pause");
8.  return 0;
9.  }

并且即使我们使用

<pre class="prism-token token  language-javascript"></pre>

1.  for(int i=0;i&lt;100;i++)
2.  test[i].push_back(1);

都是可以的，因为size已经被清除了。

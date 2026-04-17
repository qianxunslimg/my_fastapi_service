---
date: '2021-12-02T19:27:19+08:00'
tags:
- leetcode
---

<pre><span style="color: #008080;">1</span>  
<span style="color: #008080;">2</span> <span style="color: #0000ff;">long</span> <span style="color: #0000ff;">long</span> C(<span style="color: #0000ff;">int</span> N, <span style="color: #0000ff;">int</span><span style="color: #000000;"> M) {
</span><span style="color: #008080;">3</span>     <span style="color: #0000ff;">long</span> <span style="color: #0000ff;">long</span> sum = <span style="color: #800080;">1</span><span style="color: #000000;">;
</span><span style="color: #008080;">4</span>     <span style="color: #0000ff;">for</span>(<span style="color: #0000ff;">int</span> i=<span style="color: #800080;">1</span>;i&lt;=M; i++<span style="color: #000000;">) {
</span><span style="color: #008080;">5</span>         sum=sum*(N-M+i)/<span style="color: #000000;">i;
</span><span style="color: #008080;">6</span> <span style="color: #000000;">    }
</span><span style="color: #008080;">7</span>     <span style="color: #0000ff;">return</span><span style="color: #000000;"> sum;
</span><span style="color: #008080;">8</span> }</pre>

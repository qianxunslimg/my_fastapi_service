---
date: '2021-12-02T19:16:42+08:00'
tags:
- 开发随笔
---

#### 最近写一个Qt小程序用到了QString的截断，在绝对路径中取文件的名字，再拼接到新路径中，用到了两个方法：

### 方法一：由于对QString没有深入了解，所以采用的QString--&gt;string--&gt;QString，代码如下：

```c++
std::string pur = purposelist[i].toStdString();//都转换为string
// qDebug()<<pur<<endl;
std::string sdir = dstpath.toStdString();
int pos = pur.find_last_of('/'); //找到最后/
std::string s(pur.substr(pos + 1));
sdir.append("/");
sdir.append(s);
QString qsdir = QString(QString::fromLocal8Bit(sdir.c_str()));
qDebug() << qsdir << endl;
```



### 用这种方法出现的问题是，string中的中文字符转到QString会乱码...

&nbsp;

### 方法二：QString直接进行截断拼接

```c++
//QString截断学习
QString src("E:/qq接收文件/MobileFile/thumb/碎裂收据.jpg");
qDebug()<<"original path: "<<src<<endl;
QString dir("E:/目标文件夹");
qDebug()<<"the last string '/' pos is "<<src.lastIndexOf('/')<<endl;
QString filename = src.right(src.size() - (src.lastIndexOf("/")+1));
qDebug()<<"the true filename is "<<filename<<endl;
```

### 复盘，刚接触qt的自己好蠢，事实上 qstring可能是c++下最好用的string了

QString存储字符串采用的是Unicode码,每一个字符是一个十六位的QChar, 而不是八位的char, 所以处理中文字符没有问题, 而且一个汉字是一个字符。

#### 函数

**1、append()和prepend()**

append()在字符串后面添加字符串,prepend()在字符串前面添加字符串。

如下：

```text
QString str1="卖", str2 = "拐";
str1 = str1.append(str2);	//"卖拐"
str2 = str2.prepend(str1);	//"拐卖"
```

**2、toUpper()和toLower()**

toUpper()是将字符串中的字母全部转化为大写字母,toLower()是将所有的字母全部转化为小写字母。

如下：

```text
QString str1 = "Hello World", str2;
str2 = str1.toUpper();	//"HELLO WORLD"
str2 = str1.toLower();	//"hello world"
```

**3、cont()、size()和length()**

count()、size()和length()这三个函数都是返回字符串的个数的,这3个函数是相同的。注意：一个汉字算是一个字符

如下：

```text
QString str = "NI 好";
N = str.count();	//N == 3
N = str.size();		//N == 3
N = str.length();	//N == 3
```

**4、trimmed()和simplified()**

trimmed()是去掉字符串首尾的空格,simplified()不仅去掉首尾的空格,中间连续的空格也能用一个空格替换。

如下：

```text
QString str1 = " Are    you  ok?   ";
str2 = str1.trimmed();		//"Are    you  ok?"
str2 = str1.simplified()	//"Are you ok?"
```

**5、indexOf()和lastIndexOf()**

查找字符串的位置

如下：

```text
QString str1 = "G:\Qt5Book\Qt5.9Study\qw.cpp";
N = str1.indexOf("5.9");			//N == 13
N = str1.lastIndexOf("\\");			//N == 21
注意："\"是转义字符,如果要查找"\",需要输入"\\"
```

**6、isNull()和isEmpty()**

这两个函数都用来判断字符串是否为空,但是稍微有差别。如果一个空字符串,只有"\0",isNull()返回false,而isEmpty()返回true;只有未赋值的字符串,isNull()才返回true。

如下：

```text
QString str1, str2="";
N = str1.isNull();	//true	未赋值字符串变量
N = str2.isNull();	//false	只有"\0"的字符串,也不是Null
N = str1.isEmpty(); //true
N = str2.isEmpty(); //true
```

**7、contains()**

判断字符串内是否包含某个字符,可指定是否区分大小写。

如下：

```c++
QString str1 = "G:\Qt5Book\Qt5.9Study\qw.cpp";
N = str1.contains(".cpp", Qt::CaseInsensitive);		//true 不区分大小写	
N = str1.contains(".CPP", Qt::CaseSensitive);		//false 区分大小写
```

**8、endsWith()和startsWith()**

startsWith()判断是否以某个字符串开头,endsWith()表示是否以某个字符串结尾。

如下：

```c++
QString str1 = "G:\Qt5Book\Qt5.9Study\qw.cpp";
N = str1.endsWith(".cpp", Qt::CaseInsensitive);		//true 不区分大小写	
N = str1.endsWith(".CPP", Qt::CaseSensitive);		//false 区分大小写
N = str.startsWith("g:");							//true 缺省为不区分大小写
```

**9、left()和right()**

left()表示取一个字符串左边多少个字符,right()表示取一个字符串右边多少个字符。注意：一个汉字被当作一个字符;

```c++
QString str2, str1="学生姓名, 男, 1984-3-4, 汉族, 山东";
N = str1.indexOf(",");					//N == 4,第一个","出现的位置
str2 = str1.left(N);					//str2 == "学生姓名"
N = str1.lastIndexOf(",");				//N ==18,最后一个逗号出现的位置
str2 = str1.right(str1.size()-N-1);		//str2 = "山东",提取最后一个逗号之间的字符串
```

**10、section()**

从字符串中提取以se为分隔符,从start到end的字符串。

```c++
QString str1 = "G:\Qt5Book\Qt5.9Study\qw.cpp", str2;
str2 = str1.section(",",0,0);	//str2 == "学生姓名"
str2 = str1.section(",",1,1);	//str2 == "男"
str2 = str1.section(",",0,1);	//str2 == "学生姓名,男"
str2 = str1.section(",",4,4);	//str2 == "山东"
```

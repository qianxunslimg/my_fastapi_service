---
date: '2021-12-02T19:40:46+08:00'
---

QT的路径格式使用 / 或 \\

读写文本

```c++
 1     //写文本
 2     QFile f("F:/src/1.txt");
 3     if(!f.open(QIODevice::WriteOnly | QIODevice::Text))
 4     {
 5         qDebug() << "Open failed." << endl;
 6     }
 7 
 8     QTextStream txtOutput(&f);
 9     QString s1("123");
10     quint32 n1(123);
11 
12     txtOutput << s1 << endl;
13     txtOutput << n1 << endl;
14 
15     f.close();
16 
17 
18    //读文本
19     QFile f("F:/src/1.txt");
20     if(!f.open(QIODevice::ReadOnly | QIODevice::Text))
21     {
22         qDebug() << "Open failed." << endl;
23     }
24 
25     QTextStream txtInput(&f);
26     QString lineStr;
27     while(!txtInput.atEnd())
28     {
29         lineStr = txtInput.readLine();
30         qDebug() << lineStr << endl;
31     }
32 
33     f.close();
```

 

查找路径下所有特定文件（和文件夹）

```c++
 1 void fllemanage::on_pushButton_clicked()
 2 {
 3     //    int count = 0;
 4     //    QString dirpath = "C:/Users/00/Desktop/git clone/OpenCV-Python-Tutorial/.idea";
 5     //    //设置要遍历的目录
 6     //    QDir dir(dirpath);
 7     //    qDebug()<<dirpath<<endl;
 8     //    //设置文件过滤器
 9     //    QStringList nameFilters;
10     //    //设置文件过滤格式
11     //    nameFilters << "*.xml";
12     //    dir.setNameFilters(nameFilters);
13     //    qDebug()<<dir.entryList()<<endl;
14     //    qDebug()<<dir.entryInfoList()<<endl;
15     //    //将过滤后的文件名称存入到files列表中
16     //    QStringList files = dir.entryList(nameFilters, QDir::Files|QDir::Readable, QDir::Name);
17     //    for(int i = 0; i<files.size(); i++)
18     //    {
19     //        qDebug()<<"now, it's output from QStringlist"<<endl;
20     //        qDebug()<<files[i]<<endl;
21     //    }
22 
23     QStringList list = findALLfiles("C:/Users/00/Desktop/vsrun/123");
24     //QStringList list = findALLfiles("C:/Users/00/Desktop/vsrun");
25     //for(int i = 0 ; i <list.size(); i++)
26       //qDebug() <<list[i]<<endl;
27     QStringList purposelist;
28     purposelist = list.filter(".txt");
29     int count = 0;
30     for (int i = 0; i < purposelist.size(); i++)
31     {
32         qDebug() << purposelist[i] << endl;
33         count++;
34     }
35     qDebug() << "the max file has " << list.size() << endl;
36     qDebug() << "the purpose file has " << count << endl;
37 
38     //新建文件夹（目标文件保存的位置）
39 //     QDir dir("C:/Users/00/Desktop/vsrun");
40 //     if(!dir.exists("copy to here")){
41 //         dir.mkdir("copy to here");
42 //     }
43     QString toDir = "C:/Users/00/Desktop/123";
44     //toDir.replace("\\","/");
45 
46     QDir dir(toDir);
47     if (!dir.exists(toDir)) {
48         dir.mkdir(toDir);
49     }
50 
51     QFile destFile(toDir);
52     bool success = true;
53     success &= destFile.open(QFile::WriteOnly | QFile::Truncate);
54 
55     for (int i = 0; i < purposelist.size(); i++)
56     {
57         if (QFile::copy(purposelist[i], toDir)) {  //将文件复制到新的文件路径下
58             {//QFile::copy(purposelist[i],toDir);
59                 qDebug() << QStringLiteral("复制成功");
60             }
61         }
62     }
63 }
64 
65 //迭代器遍历所有文件并返回
66 QStringList fllemanage::findALLfiles(const QString &dir_path) {
67     QStringList get_files;
68     QDir dir(dir_path);
69     if (!dir.exists())
70     {
71         qDebug() << "it is not true dir_path";
72     }
73 
74     /*设置过滤参数，QDir::NoDotAndDotDot表示不会去遍历上层目录*/
75     QDirIterator dir_iterator(dir_path, QDir::Files | QDir::Dirs | QDir::NoDotAndDotDot, QDirIterator::Subdirectories);
76 
77     while (dir_iterator.hasNext())
78     {
79         dir_iterator.next();
80         QFileInfo file_info = dir_iterator.fileInfo();
81         QString files = file_info.absoluteFilePath();
82         get_files.append(files);
83     }
84 
85     return get_files;
86 }
```

 

QFile copy（报错未实现 QIodevce not opened） 

```c++
    //    copy测试！！！！！！
    //    QFile src("F:/src");
    //    QFile dst("F:/dst");

    //    bool success = true;
    //    success &= src.open( QFile::ReadOnly );
    //    success &= dst.open( QFile::WriteOnly | QFile::Truncate );
    //    success &= dst.write( src.readAll() ) >= 0;

    //   QFile::copy("F:/src/1.txt" , "F:/dst");
    //    src.close();
    //    dst.close();
```

更新：QFile copy 函数写法：

```c++
QFile::copy("F:/src/1.txt" , "F:/dst/2.txt")；  //（具体文件名 to 具体文件名）


copy函数不能对string类型的路径进行操作，可从QString转string操作再转QString：

```

 

```c++
        std::string pur = purposelist[i].toStdString();//都转换为string
       // qDebug()<<pur<<endl;
        std::string sdir = toDir.toStdString();
        int pos = pur.find_last_of('/'); //找到最后/
        std::string s(pur.substr(pos+1));
        sdir.append("/");
        sdir.append(s);
        QString qsdir = QString(QString::fromLocal8Bit(sdir.c_str()));
        qDebug()<<qsdir<<endl;
 
```

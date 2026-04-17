---
date: '2021-12-02T19:40:01+08:00'
---

```c++
#include "fllemanage.h"
#include "ui_fllemanage.h"

fllemanage::fllemanage(QWidget *parent)
	: QWidget(parent)
	, ui(new Ui::fllemanage)
{
	ui->setupUi(this);

        //copy测试！！！！！！
//        QFile src("F:/src");
//        QFile dst("F:/dst");

//        bool success = true;
//        success &= src.open( QFile::ReadOnly );
//        success &= dst.open( QFile::WriteOnly | QFile::Truncate );
//        success &= dst.write( src.readAll() ) >= 0;

//       QFile::copy("F:/src/1.txt" , "F:/dst/2.txt");
//        src.close();
//        dst.close();

	//    //写文本
	//    QFile f("F:/src/1.txt");
	//    if(!f.open(QIODevice::WriteOnly | QIODevice::Text))
	//    {
	//        qDebug() << "Open failed." << endl;
	//    }

	//    QTextStream txtOutput(&f);
	//    QString s1("123");
	//    quint32 n1(123);

	//    txtOutput << s1 << endl;
	//    txtOutput << n1 << endl;

	//    f.close();

	//   //读文本
	//    QFile f("F:/src/1.txt");
	//    if(!f.open(QIODevice::ReadOnly | QIODevice::Text))
	//    {
	//        qDebug() << "Open failed." << endl;
	//    }

	//    QTextStream txtInput(&f);
	//    QString lineStr;
	//    while(!txtInput.atEnd())
	//    {
	//        lineStr = txtInput.readLine();
	//        qDebug() << lineStr << endl;
	//    }

	//    f.close();
}

fllemanage::~fllemanage()
{
	delete ui;
}

void fllemanage::on_pushButton_clicked()
{
	//    int count = 0;
	//    QString dirpath = "C:/Users/00/Desktop/git clone/OpenCV-Python-Tutorial/.idea";
	//    //设置要遍历的目录
	//    QDir dir(dirpath);
	//    qDebug()<<dirpath<<endl;
	//    //设置文件过滤器
	//    QStringList nameFilters;
	//    //设置文件过滤格式
	//    nameFilters << "*.xml";
	//    dir.setNameFilters(nameFilters);
	//    qDebug()<<dir.entryList()<<endl;
	//    qDebug()<<dir.entryInfoList()<<endl;
	//    //将过滤后的文件名称存入到files列表中
	//    QStringList files = dir.entryList(nameFilters, QDir::Files|QDir::Readable, QDir::Name);
	//    for(int i = 0; i<files.size(); i++)
	//    {
	//        qDebug()<<"now, it's output from QStringlist"<<endl;
	//        qDebug()<<files[i]<<endl;
	//    }

    //QStringList list = findALLfiles("C:/Users/00/Desktop/vsrun/123");
    //QStringList list = findALLfiles("C:/Users/00/Desktop/vsrun");
    QStringList list = findALLfiles("C:/Users/00/Desktop/git clone");
                                                                        //for(int i = 0 ; i <list.size(); i++)
	  //qDebug() <<list[i]<<endl;
	QStringList purposelist;
    purposelist = list.filter(".jpg");
	int count = 0;
	for (int i = 0; i < purposelist.size(); i++)
	{
		qDebug() << purposelist[i] << endl;
		count++;
	}
	qDebug() << "the max file has " << list.size() << endl;
	qDebug() << "the purpose file has " << count << endl;

	//新建文件夹（目标文件保存的位置）
//     QDir dir("C:/Users/00/Desktop/vsrun");
//     if(!dir.exists("copy to here")){
//         dir.mkdir("copy to here");
//     }
    QString toDir = "C:/Users/00/Desktop/123";

	//toDir.replace("\\","/");

	QDir dir(toDir);
	if (!dir.exists(toDir)) {
		dir.mkdir(toDir);
	}

	QFile destFile(toDir);
	bool success = true;
	success &= destFile.open(QFile::WriteOnly | QFile::Truncate);

	for (int i = 0; i < purposelist.size(); i++)
    {
        std::string pur = purposelist[i].toStdString();//都转换为string
       // qDebug()<<pur<<endl;
        std::string sdir = toDir.toStdString();

        int pos = pur.find_last_of('/'); //找到最后/
        std::string s(pur.substr(pos+1));
        sdir.append("/");

        sdir.append(s);
        QString qsdir = QString(QString::fromLocal8Bit(sdir.c_str()));
        qDebug()<<qsdir<<endl;
        if (QFile::copy(purposelist[i], qsdir)) {  //将文件复制到新的文件路径下
            {
                if(QFile::copy(purposelist[i],toDir))
                 qDebug() << QStringLiteral("复制成功");
			}
		}
	}
}

//迭代器遍历所有文件并返回
QStringList fllemanage::findALLfiles(const QString &dir_path) {
	QStringList get_files;
	QDir dir(dir_path);
	if (!dir.exists())
	{
		qDebug() << "it is not true dir_path";
	}

	/*设置过滤参数，QDir::NoDotAndDotDot表示不会去遍历上层目录*/
	QDirIterator dir_iterator(dir_path, QDir::Files | QDir::Dirs | QDir::NoDotAndDotDot, QDirIterator::Subdirectories);

	while (dir_iterator.hasNext())
	{
		dir_iterator.next();
		QFileInfo file_info = dir_iterator.fileInfo();
		QString files = file_info.absoluteFilePath();
		get_files.append(files);
	}

	return get_files;
}
```

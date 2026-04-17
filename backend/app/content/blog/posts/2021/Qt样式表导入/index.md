---
date: '2021-07-26T19:28:00+08:00'
tags:
- 开发随笔
---

```c++
#include "select.h"
#include <QtWidgets/QApplication>
int main(int argc, char *argv[]) {
  QApplication a(argc, argv);
  select1 w;

  QFile qssFile(
      "D://qq received//select//select//lightblue.css"); //资源文件":/css.qss"
  qssFile.open(QFile::ReadOnly);
  if (qssFile.isOpen()) {
    QString qss = QLatin1String(qssFile.readAll()); //读取
    qApp->setStyleSheet(qss);                       //设置
    qssFile.close();
  }

  w.show();
  return a.exec();
}
```

另外 qt有一个样式表生成的小工具 quicreator 可以自行查找

---
date: '2021-09-26T19:28:00+08:00'
tags:
- 开发随笔
---

#### 起因

本身软件的文件读取逻辑是csv存储工程测点路径 然后根据路径去指定目录下找指定格式的文件读取 这个文件逻辑也是我们的采集设备采集完成后，结果文件的保存逻辑

奈何甲方使用习惯不同，习惯ctrl A全选 所有文件放在一个文件夹下和csv匹配，只好添加此逻辑

实现过程中，按照网上的方法，发现mfc的CFileDialog读取多个文件有个最大数量的限制，选的多，实际读取到的并不全

#### 解决方法

设置CFileDialog的相关属性

```c++
  allDisp.clear();
  if (!m_sparkFile) // liu的文件逻辑
  {
    // dlg.InitList(strFileName, m_listSource);
    CFileDialog alldlg(TRUE, NULL, NULL,
                       OFN_HIDEREADONLY | OFN_OVERWRITEPROMPT |
                           OFN_ALLOWMULTISELECT | OFN_EXPLORER,
                       _T("Disp(*disp)|*.disp||"));
    //添加这些
		//////////////////////////////////////////
    DWORD MAXFILE = 4000;
    alldlg.m_ofn.nMaxFile = MAXFILE;
    char *pc = new char[MAXFILE];
    alldlg.m_ofn.lpstrFile = pc;
    alldlg.m_ofn.lpstrFile[0] = NULL;
		//////////////////////////////////////////
    
    if (IDOK != alldlg.DoModal())
      return;

    POSITION pos = alldlg.GetStartPosition();

    while (pos) {
      allDisp.insert(alldlg.GetNextPathName(pos));
    }
    dispPath = alldlg.GetPathName();
  }
```

---
date: '2021-08-26T19:28:00+08:00'
tags:
- 开发随笔
---

#### 说明

1. 做一个实际工程应用的项目 甲方是将图片拖到cad里进行观看 因此就要求比例尺等的信息保存 cad支持的只有tif和bmp，而我的软件的成图是基于opencv的 opencv的imwrite还是过于粗糙，因此查阅整理了一个完整bmp的函数
2. bmp的头信息是很复杂的，并不是单纯的改个文件名就可以，这也是为什么 mfc的icon那么难搞 网上找遍格式转换的网站 只有那么一两个的转换结果可以使用（简直折磨）
3. bmp格式这里不加赘述了 可以参考[这个](https://blog.csdn.net/u012877472/article/details/50272771)

#### 实现

bmp.h

```c++
#ifndef BMP_H
#define BMP_H
typedef unsigned char LBYTE;  //
typedef unsigned short LWORD; //
typedef unsigned int LDWORD;
typedef long LLONG; //

#pragma pack(2)
typedef struct {
  LWORD bfType;
  LDWORD bfSize;
  LWORD bfReserved1;
  LWORD bfReserved2;
  LDWORD bfOffBits;
} LBITMAPFILEHEADER;
// #pragma pack(pop)

typedef struct {
  LDWORD biSize;
  LLONG biWidth;
  LLONG biHeight;
  LWORD biPlanes;
  LWORD biBitCount;
  LDWORD biCompression;
  LDWORD biSizeImage;
  LLONG biXPelsPerMeter;
  LLONG biYPelsPerMeter;
  LDWORD biClrUsed;
  LDWORD biClrImportant;
} LBITMAPINFOHEADER;

typedef struct {
  LBYTE rgbBlue;
  LBYTE rgbGreen;
  LBYTE rgbRed;
  LBYTE rgbReserved;
} LRGBQUAD;

typedef struct {
  unsigned char *buf;
  int width_x;
  int height_y;
  int deepth;
  LRGBQUAD *palette;
} LBmpbase;

// bool saveBmp(char*, unsigned char*, int, int, int, RGBQUAD*);
// Bmpbase readbmp(char*);
/*bool saveBmp(char *, unsigned char *, int, int, int, LRGBQUAD *);*/

bool SaveBmp(char *fileName, unsigned char *imgBuffer, int imWidth,
             int imHeight, int x_scale, int y_scale, int m_colorTable);
#endif

```

bmp.cpp

参数说明，其他参数没有什么好说明的 从英文可以看出来 以此是文件名，图像的data, 宽 高 宽比例尺 高比例尺 

最后一个参数是灰度彩色的标志位 `0表示灰度图 ` 非0为彩色

```c++
#include "stdafx.h"

//
#include "bmp.h"

bool SaveBmp(char *fileName, unsigned char *imgBuffer, int imWidth,
             int imHeight, int x_scale, int y_scale, int m_colorTable) {
  if (!imgBuffer) {
    return 0;
  }
  int biBitCount;

  if (m_colorTable) {
    biBitCount = 24;
  } else if (m_colorTable == 0) {
    biBitCount = 8;
  }
  int colorTablesize;
  if (m_colorTable) {
    colorTablesize = 0;
  } else if (m_colorTable == 0) {
    colorTablesize = 1024;
  }
  //颜色表大小，以字节为单位，灰度图颜色表大小1024，彩色图为0
  int lineByte = (imWidth * biBitCount / 8 + 3) / 4 * 4;
  FILE *fp = fopen(fileName, "wb");
  if (!fp) {
    return 0;
  }
  LBITMAPFILEHEADER filehead;
  filehead.bfType = 0x4D42;
  filehead.bfSize = sizeof(LBITMAPFILEHEADER) + sizeof(LBITMAPINFOHEADER) +
                    colorTablesize + lineByte * imHeight;
  filehead.bfReserved1 = 0;
  filehead.bfReserved2 = 0;
  filehead.bfOffBits = 54 + colorTablesize;
  //写位图文件头进文件
  fwrite(&filehead, sizeof(LBITMAPFILEHEADER), 1, fp);

  //申请位图文件信息头结构变量， 填写文件信息头信息
  LBITMAPINFOHEADER infoHead;
  infoHead.biBitCount = biBitCount;
  infoHead.biClrImportant = 0;
  infoHead.biClrUsed = 0;
  infoHead.biSize = 40;
  infoHead.biWidth = imWidth;
  infoHead.biHeight = imHeight;
  infoHead.biPlanes = 1;
  infoHead.biCompression = BI_RGB;
  infoHead.biSizeImage = lineByte * imHeight;
  infoHead.biXPelsPerMeter = x_scale;
  infoHead.biYPelsPerMeter = y_scale;
  fwrite(&infoHead, sizeof(LBITMAPINFOHEADER), 1, fp);

  if (m_colorTable == 0) {
    LRGBQUAD *pColorTable = new LRGBQUAD[256];

    for (int i = 0; i < 256; i++) {
      pColorTable[i].rgbBlue = i;
      pColorTable[i].rgbGreen = i;
      pColorTable[i].rgbRed = i;
      pColorTable[i].rgbReserved = 0;
    }
    fwrite(pColorTable, sizeof(LRGBQUAD), 256, fp); //彩色图 无需写入颜色表
  }

  //写位图数据进文件
  fwrite(imgBuffer, imHeight * lineByte, 1, fp);

  fclose(fp);
  return 1;
}
```

#### 调用

其实还有一个注意的点就是 `bmp还涉及到一个反转的问题` 从opencv的mat格式 存储为bmp是需要对mat进行一下`反转`

我的调用如下

```c++
    Mat res;
    flip(img, res, 0); // bmp需要垂直反转

    CString strID;
    strID.Format("_%ld.bmp", m_conTab.GetCurSel() + 1);
    strFileName.Replace(".bmp", strID);
    if (i == 0 || i == 2) {
      //深度图按设定的比例尺保存
      SaveBmp((LPSTR)(LPCTSTR)strFileName, res.data, m_pView->m_dwWidth,
              m_pView->m_dwHeight,
              round((double)1000 * m_xactualScale / m_nHScales[i]),
              round((double)1000 * m_yactualScale / m_nVScales[i]), m_colorMap);
    } else {
      //频率和hv图片等比保存
      SaveBmp((LPSTR)(LPCTSTR)strFileName, res.data, m_pView->m_dwWidth,
              m_pView->m_dwHeight,
              round((double)1000 * m_xactualScale / m_nHScales[i]),
              round((double)1000 * m_xactualScale / m_nHScales[i]), m_colorMap);
    }
```

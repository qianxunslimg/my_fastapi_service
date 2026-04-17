---
date: '2023-04-19T01:59:00+08:00'
tags:
- 自驾相关
---

总是一遍一遍配置 一遍一遍找教程 记录一下

### 1. ubuntu换源

参考这个网站的源[ubuntu | 镜像站使用帮助 | 清华大学开源软件镜像站 | Tsinghua Open Source Mirror](https://mirror.tuna.tsinghua.edu.cn/help/ubuntu/)

执行如下：

```bash
sudo gedit /etc/cat/sources.list
```

直接替换源即可

### 2. ROS安装

参考网站[小鱼的一键安装系列 | 鱼香ROS (fishros.org.cn)](https://fishros.org.cn/forum/topic/20/小鱼的一键安装系列?lang=zh-CN)

直接输入指令

```bash
wget http://fishros.com/install -O fishros && . fishros
```

根据需求 选择即可

根据如下教程`测试ros2是否安装成功`

1. 新开一个terminal，运行以下命令，打开小乌龟窗口：

   ```bash
   ros2 run turtlesim turtlesim_node       # 启动乌龟GUI节点界面，乌龟可以在界面中运动
   ```

2. 新开一个terminal，运行以下命令，打开乌龟控制窗口，可使用方向键控制乌龟运动：

   ```bash
   ros2 run turtlesim turtle_teleop_key    # 启动键盘控制节点，可以通过键盘控制乌龟运动
   ```

### 3. 安装c++相关

#### gcc

ubuntu自带gcc，查看版本

```bash
gcc -v
```

#### g++

```bash
sudo apt-get install build-essential
```

查看版本

```bash
g++ -v
```

#### make

ubuntu自带make，查看版本

```bash
make -v
```

#### cmake

ubuntu基本也自带cmake，查看版本

```bash
cmake --version
```

不带的话就

```bash
sudo apt install cmake
```

版本提升

[正确的方式升级ubuntu的cmake - Oontinue - 博客园 (cnblogs.com)](https://www.cnblogs.com/Maker-Liu/p/16550381.html)

### 4. 安装vscode

1. 软件商店直接下载

2. 下载dbkg包，然后

   ```bash
   sudo dpkg -i ***.deb
   ```

3. snap命令

   ```bash
   sudo snap install --classic code
   ```

### 5. 安装python pip

python肯定自带

```bash
python --version
python3 --version #3.6
```

安装python3.8，搜到的教程可以直接使用[Ubuntu安装Python3.8 | AI技术聚合 (aitechtogether.com)](https://aitechtogether.com/python/50592.html)

```bash
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.8
python3.8 --version


#设置为默认的python3
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
```

安装pip3

```bash
sudo apt-get install python3-pip
```

换源，建立sh 然后`sudo sh **.sh`

```bash
#!/bin/bash

set -ex

# 更换国内镜像源，这里使用的是 aliyun

mkdir -p ~/.pip

touch ~/.pip/pip.conf

echo "[global]
timeout = 6000
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = mirrors.aliyun.com
" > ~/.pip/pip.conf

# example
# pip3 install numpy
```

### 6. 安装jupyter notebook

```bash
python3 -m pip install --upgrade pip
sudo python3 -m pip install jupyter
```

### 7. docker安装

~~官方脚本安装~~ 网太差 版本也可能不对应

```bash
 curl -fsSL https://test.docker.com -o test-docker.sh
 sudo sh test-docker.sh
```

参考[Docker之Ubuntu18.04简单安装 - 个人文章 - SegmentFault 思否](https://segmentfault.com/a/1190000022374119)

在https://download.docker.com/linux/ubuntu/dists下载deb安装包 

ubuntu1804代号是bionic 下载地址 https://download.docker.com/linux/ubuntu/dists/bionic/pool/stable/amd64/ 下载速度也是一言难尽

```bash
sudo dpkg -i package.deb
```

还有就是之前的大佬制作的一键安装 没有测试

```bash
wget http://fishros.com/install -O fishros && . fishros
```

### 8. QT安装

下载.run安装包 直接

```bash
sudo ./qt-opensource-linux-x64-5.12.2.run 
# 依赖安装
sudo apt-get install libqt4-dev
```

### 9. clion安装

1. 下载tar包 解压 然后执行clion.sh  (感觉不好，同学电脑上没有添加到可执行文件夹)
2. snap安装 sudo snap install clion --classic

### 10. ubuntu字体设置

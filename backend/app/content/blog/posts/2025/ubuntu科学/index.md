---
date: '2025-08-21T16:28:00+08:00'
tags:
- 开发随笔
---

### 1. 代理配置

<img src="./assets/image-20250831162851046-2.png" alt="image-20250831162851046" style="zoom:50%;" />

### 2. clash-linux

```bash
# 1. 直接执行 生成默认配置文件 然后c掉
./clash-linux-amd64
# 2. 更新配置到yaml
wget -O ~/.config/clash/config.yaml 订阅地址
# 3. 重新启动clash
./clash-linux-amd64
# 4. 网页配置规则
http://clash.razord.top/#/proxies
```

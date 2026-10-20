---
title: 角落里的旧小主机，改成家里的常开服务器
summary: 一台吃灰的迷你主机重新上岗：Docker 跑一堆自托管服务，内网穿透让外面也能用，现在还没折腾完。
status: 折腾中
startDate: 2026-09-02
cost: 0
hours: 18
stack: [Docker, Ubuntu, Cloudflare Tunnel, Nginx]
tags: [服务器, Docker, 自托管, 内网穿透, Linux]
featured: true
changelog:
  - date: 2026-09-02
    note: 装系统，Docker + Portainer 跑起来。
  - date: 2026-09-15
    note: 接了 5 个服务：文件同步、RSS、代码片段、下载、监控。
  - date: 2026-10-06
    note: 换成 Cloudflare Tunnel，砍掉公网端口转发。
---

## 背景

家里一台迷你主机空了半年。性能对写代码的日常来说不够用，但**当一台 7×24 的小服务器绰绰有余**。

想让它干的事：

- 放一些自托管服务（RSS 阅读、代码片段、文件同步）
- 定时跑抓取和备份脚本
- 手机上、公司里也能访问到

## 方案

三个关键选择：

**1. 系统：Ubuntu Server LTS 而不是 Windows**
不吃内存、SSH 就能管、Docker 生态完整。图形界面完全不需要。

**2. 服务编排：Docker Compose，一个服务一个 `compose.yaml`**
不用 Portainer 的堆栈管理，目录结构就是：

```
/srv
├── rss/compose.yaml
├── snippets/compose.yaml
└── files/compose.yaml
```

升级就是 `cd rss && docker compose pull && docker compose up -d`，清楚得不用记。

**3. 外网访问：Cloudflare Tunnel，不做端口转发**

| 方案 | 问题 |
| --- | --- |
| 路由器端口转发 + DDNS | 家庭 IP 暴露在公网，被扫是必然的 |
| 第三方内网穿透 | 免费版限速、域名丑 |
| **Cloudflare Tunnel** | 不需要公网 IP，出站连接，Cloudflare 那边管证书和防护 |

## 过程

装系统、Docker、建普通用户，这些是标准流程。真正花时间的是隧道：

```bash
# 一次性：登录并创建隧道
cloudflared tunnel login
cloudflared tunnel create homelab

# 一个隧道塞多个域名
cloudflared tunnel route dns homelab rss.example.com
cloudflared tunnel route dns homelab files.example.com

# 用 systemd 常驻
sudo cloudflared service install
```

`config.yml` 里按 hostname 分流到本机不同端口，一套隧道管所有服务，加一个服务只要加三行。

## 踩坑

| 现象 | 原因 | 解法 |
| --- | --- | --- |
| 隧道跑起来但一直 502 | 容器只监听 `127.0.0.1`，隧道从容器网络访问不到 | Nginx 反代一层，或让容器监听 `0.0.0.0` 并只映射本机端口 |
| 上传大文件突然断 | Cloudflare 免费版上传上限 100MB | 走分片上传，或大文件走局域网/别的通道 |
| 重启后容器没起来 | `restart: unless-stopped` 写了但 compose 文件在别的目录 | `docker compose -f` 的全路径要一致 |
| 日志把磁盘吃满 | 默认 json-file 无上限 | 全局配置 `max-size: 10m, max-file: 3` |

## 结果

**还在折腾中。** 目前稳定跑着 5 个服务，CPU 常年 5% 以下，功耗待机 8W 左右。

已经想清楚但还没做的：

- [ ] 全站统一认证（现在是每个服务各自一套账号）
- [ ] 自动快照到第二块盘
- [ ] 一块小屏幕显示实时状态

说实话，自托管这件事的性价比经常是负的——花的时间远超省下的订阅费。
但能随手改一行配置就拥有自己想要的行为，这个感觉挺值。

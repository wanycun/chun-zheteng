---
title: Tailscale 组网：把 Muse 和两台 NAS 拉进同一个网
summary: 免费、不用公网 IP、不开端口，三台设备进同一个虚拟内网，SSH 免验证直连。踩过「改策略不重启」和「密钥栏粘进报错日志」两个坑，这条通道是后面所有折腾的地基。
status: 已跑通
startDate: 2026-11-03
endDate: 2026-11-05
cost: 0
stack: [Tailscale, Tailscale SSH, 飞牛 NAS, Muse]
tags: [Muse, Tailscale, 飞牛 NAS]
cover: /covers/muse-nas-network-cover.png
---

## 项目速览

muse 是国外助手，自带 Tailscale 连接器——装上就能把设备拉进同一个虚拟内网。
组好之后 muse 能直接登录两台 NAS 干活：ARM 盒子（家里副机）+ x86 机子（主机），我动嘴，它进机器。

两个真金白银换来的坑：

- **改策略要重启**：Tailscale 控制台 → Access controls → `ssh` 字段的 `action` 从 `check` 改成 `accept`，弹验证链接的毛病就断了；但改完不重启目标机的 Tailscale 服务等于没改
- **密钥栏别粘错**：ARM 盒子登录状态掉了，重登时密钥栏粘进去的是上一次的报错日志——飞牛那个应用把各框内容不加引号直接拼命令，错误把错误自己喂给了命令。重装 + 可复用授权码重登记解决，代价是设备换了新地址，还要去「高级功能」里手动重开 Tailscale SSH

## 关键数字

| 项 | 值 |
| --- | --- |
| 设备 | 3 台（muse / ARM 盒子 / x86 主机） |
| 花费 | ¥0（免费档） |
| 公网 IP / 端口映射 | 都不需要 |
| 故障定位 | 22:12 日志实锤，22:19 收官 |

## 全文

完整排查过程（含误诊 DNS 那段弯路）写在笔记里：
**[Muse 接管我的两台 NAS](/notes/muse-nas-network/)**

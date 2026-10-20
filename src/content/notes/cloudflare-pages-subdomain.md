---
title: Cloudflare Pages 绑子域的两个坑
date: 2026-08-15
tags: [Cloudflare, 建站, 部署]
summary: 自定义域一直「验证中」，以及绑定后 www 和裸域不对——都是 DNS 记录类型的问题。
---

## 坑一：一直卡在「正在验证」

在 Pages 项目里加自定义域 `w.example.com` 之后，状态死活不动。原因通常是：

- 这个域名的 **zone 不在同一个 Cloudflare 账号**下 —— Pages 没法自动建记录
- 或者 DNS 里已经有一条手动加的、指错的记录挡住了

判断方法：项目设置里的域名状态会写 `CNAME record not found`，去 DNS 面板看一眼有没有这条记录。

正确的记录是：

```
w    CNAME    <项目名>.pages.dev    （Proxy 状态：已开启）
```

## 坑二：把根域和子域混着加

想在同一个项目上同时支持 `example.com` 和 `www.example.com`，会碰到：

- 根域（apex）不能直接 CNAME，Cloudflare 会帮你转成 `A` 记录 + CNAME flattening，通常能用
- 但**两个都加到一个 Pages 项目上，跳转方向需要自己定**，否则两边内容重复、SEO 分散

更省事的做法：只绑一个，另一个用 **Redirect Rules** 301 过去。

```text
# 只绑 w.example.com，然后加一条重定向规则
https://example.com/*  →  https://w.example.com/$1 （301）
```

## 顺带记一个

证书签发通常几十秒到几分钟。如果超过 15 分钟还是「待验证」，先点一次 **重新验证**，
再不行就删了域名重加一遍——比等更快。

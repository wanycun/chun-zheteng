---
title: Cloudflare Pages 绑子域：DNS 不会自己长出来
date: 2026-08-15
tags: [Cloudflare, 建站, 部署]
summary: 自定义域加进 Pages 后一直「待验证」，DNS 里也没有记录。原因有两个：记录要自己加，授权令牌没 DNS 权限。
---

给 Pages 项目加了 `w.example.com`，状态一直卡在「正在验证」，去 DNS 面板一看——**根本没有这条记录**。

## 坑一：以为 Pages 会自动建记录

在主域和 Pages 项目同一个账号的情况下，大多数时候它会自动建。
但这次没有，而且 `wrangler` 的 OAuth 令牌**没有 DNS 写权限**，所以也建不了。

手动补一条就完了：

```
类型   名称   内容                     代理状态
CNAME  w      <项目名>.pages.dev        已代理（橙色云）
```

`wrangler login` 申请到的权限里包括 `pages:write`、`zone:read`、`ssl_certs:write`，**但不含 `dns:write`**——
所以"用 API 自动加记录"这条路走不通，只能在面板里点，或者单独建一个带 `Zone.DNS:Edit` 的 Token。

## 坑二：记录加了还是 522，然后突然就好了

刚加完记录，访问返回 `HTTP 522`（Cloudflare 连不上源站），本地 `nslookup` 还是 NXDOMAIN。
这是三件事同时发生：

1. 本地 DNS 有**负缓存**，NXDOMAIN 会被缓存几分钟 → `ipconfig /flushdns`
2. 边缘节点还在下发新记录
3. Pages 那边域名验证还没跑完，验证完成前不一定能正确路由

等了大约两分钟，域名状态从 `pending` 变成 `active`，522 自己就没了，证书也签好了。
**遇到 522 先别改配置，等两分钟再看。**

## 顺带记两条

- 证书签发通常几十秒到几分钟；超过 15 分钟还是「待验证」，先点一次重新验证，不行就删了域名重加，比干等快
- 根域（apex）不能直接 CNAME，Cloudflare 会自动做 flattening；但**同一个项目同时绑根域和 `www` 容易出现内容重复**，更省事的做法是只绑一个，另一个用 Redirect Rule 301 过去

---
title: npm 装不动的时候，先别怀疑网络
date: 2026-07-22
tags: [npm, 网络, 排查]
summary: 装包卡住、超时、ETIMEDOUT 的排查顺序，以及国内环境下换源的正确姿态。
---

一条命令看当前用的源：

```bash
npm config get registry
```

临时换源只对这次生效（不改全局配置，推荐）：

```bash
npm i --registry=https://registry.npmmirror.com
```

真要换默认源，用 `.npmrc` 而不是命令行：

```ini
# 项目根目录 .npmrc，跟着仓库走，团队一致
registry=https://registry.npmmirror.com
```

## 排查顺序

1. `npm config get registry` —— 先确认源对不对，别急着怀疑人生
2. `npm ping` —— 源本身通不通
3. 删 `node_modules` 和 `package-lock.json` 重装 —— 依赖树插件的概率最大
4. `npm cache verify` —— 缓存坏了会报出一堆莫名其妙的 `EINTEGRITY`
5. 最后才考虑网络：`curl -I https://registry.npmjs.org/xxx`

## 两个常见坑

**别用 `npm config set registry` 全局改**
以后装 `@scope/xxx` 私有包会直接 404，因为镜像站没有你的私有源。项目级 `.npmrc` 更安全。

**`EINTEGRITY` 不一定是网络问题**
是本地缓存里的 tarball 校验和对不上。清缓存比反复重试有用：

```bash
npm cache clean --force && npm i
```

顺带一提，能换 `pnpm` 就换，装大项目能快一个量级，而且对磁盘友好得多。

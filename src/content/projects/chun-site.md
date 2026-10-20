---
title: 用 Astro + Cloudflare Pages 搭本站
summary: 折腾记录散在笔记软件里太难受，索性自己搭一个：Astro 出静态页，Cloudflare Pages 免费托管，一条命令发布。
status: 已跑通
startDate: 2026-10-20
endDate: 2026-10-20
cost: 0
hours: 6
stack: [Astro, Tailwind CSS, Cloudflare Pages, Markdown]
tags: [建站, Cloudflare, 静态站, Astro]
featured: true
changelog:
  - date: 2026-10-20
    note: 首版上线，首页 / 项目 / 笔记 / 标签 / 关于齐活。
  - date: 2026-10-20
    note: 绑定 w.wanyc.xyz，HTTPS 自动签发。
---

## 背景

折腾的东西越来越多，记录却散在几个地方：聊天记录里、临时 txt 里、脑子以为还记得的地方。
真正想回头查「当时那个端口冲突怎么解的」，得翻半天。

想要的东西其实很简单：

- 一个自己的地方，域名自己说了算
- 写东西就是写文件，别逼我开后台登录
- 不花钱，或者一年只花域名的钱
- 打开要快，手机上看也不难看

## 方案

对比了三类：

| 方案 | 好处 | 为什么没选 |
| --- | --- | --- |
| WordPress / 看图什么 | 功能全、插件多 | 要服务器、要维护、要防升级炸站 |
| Hexo / Hugo | 生态成熟、主题多 | 想改设计得跟主题打架，改起来慢 |
| **Astro 自己写** | 布局完全自己控制、默认零 JS、构建快 | 要自己写样式，但一次写完就完事了 |

托管选 **Cloudflare Pages**：免费、无限带宽、自带 HTTPS、绑定自定义域一条 CNAME 就行。
对比 Vercel 免费版，主要是国内访问稳定性和额度都更省心。

## 过程

初始化其实没什么可说的，`npm create astro` 之后把默认模板全删了重写：

```bash
npm create astro@latest -- --template minimal
npm i && npm i tailwindcss @tailwindcss/vite @astrojs/rss @astrojs/sitemap
```

内容用 Astro 5 的 **content collections**，一个项目 = 一个 Markdown 文件：

```
src/content/projects/
├── chun-site.md
├── win-backup.md
└── homelab-mini.md
```

frontmatter 里定死几个字段：`status`（折腾中 / 已跑通 / 暂停 / 已废弃 / 翻车）、`stack`、`tags`、`hours`、`cost`。
schema 用 zod 校验，写错字段名会在构建期直接报错，不会悄悄不显示。

部署就一步：

```bash
npm run deploy
# = astro build && wrangler pages deploy dist --project-name chun
```

## 踩坑

| 现象 | 原因 | 解法 |
| --- | --- | --- |
| 本地 `dist/` 上传后样式全丢 | 用相对路径 `<a href="./xxx">`，但站点部署在子路径 | 用 Astro 的 `site` 配置 + 绝对路径 |
| 深色模式刷新闪白一瞬 | 主题在 JS 里读完再切，晚于首屏渲染 | 在 `<head>` 里同步执行一段内联脚本改 `class` |
| 卡片缺封面图很难看 | 不想给每条都找图 | 按 id 哈希生成渐变底色 + 大字母，永不空缺 |
| Cloudflare 绑定域名一直验证中 | 域名的 NS 不在同一个 CF 账号下 | 确认 zone 在账号里，再加自定义域 |

## 结果

跑通了。当前这页就是产物。

- 构建时间：约 2 秒
- 单页体积：HTML + CSS 一共不到 60KB，零首屏 JS
- 费用：托管 0 元，域名是原本就有的
- 发布体验：改一个 md，一条命令，20 秒后线上生效

值不值：**值**。写记录的阻力从「打开某个 App」降到「新建一个文件」，这才是能坚持下去的关键。

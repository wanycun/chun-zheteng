---
title: 用 Astro + Cloudflare Pages 搭本站
summary: 折腾记录散在几个地方太难受，索性自己搭一个：Astro 出静态页，Cloudflare Pages 免费托管，push 到 GitHub 就自动部署。
status: 已跑通
startDate: 2026-10-20
cost: 0
hours: 8
stack: [Astro, Tailwind CSS, Markdown, Cloudflare Pages, GitHub Actions]
cover: /covers/chun-site-cover.jpg
tags: [建站, Cloudflare, 静态站, Astro]
featured: true
repo: https://github.com/wanycun/chun-zheteng
demo: https://w.wanyc.xyz
changelog:
  - date: 2026-10-20
    note: 首版上线，首页 / 项目 / 笔记 / 标签 / 关于齐活。
  - date: 2026-10-20
    note: 绑定 w.wanyc.xyz，Cloudflare 自动签发证书。
  - date: 2026-10-20
    note: 接上 GitHub，push 到 main 自动构建部署。
  - date: 2026-10-20
    note: 接入 Cloudflare Web Analytics（无 Cookie）。
---

## 背景

折腾的东西越来越多，记录却散在几个地方：聊天记录里、临时 txt 里、脑子以为还记得的地方。
真正想回头查"当时那个端口冲突怎么解的"，得翻半天。

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
| Hexo / Hugo | 生态成熟、主题多 | 想改设计得跟主题打架 |
| **Astro 自己写** | 布局完全自己控制、默认零 JS、构建 2 秒 | 要自己写样式，但一次写完就完事 |

托管选 **Cloudflare Pages**：免费、无限带宽、自带 HTTPS、绑自定义域就是一条 CNAME。
部署方式从一开始的 `wrangler` 直传，换成了 **GitHub → Pages 自动构建**，因为"改完忘了发"这种事一定会发生。

## 过程

内容用 Astro 5 的 **content collections**，一个项目 = 一个 Markdown 文件，frontmatter 用 zod 校验：

```yaml
title: 用 Astro + Cloudflare Pages 搭本站
status: 已跑通        # 折腾中 / 已跑通 / 暂停 / 已废弃 / 翻车
stack: [Astro, Tailwind CSS]
tags: [建站, Cloudflare]
```

写错字段名会在**构建期直接报错**，不会悄悄不显示——这一点比什么都省心。

发布链路最后长这样：

```
本地写 md → git push → Cloudflare 拉代码 → npm run build → 发布到 w.wanyc.xyz
```

Pages 那边的配置就三行：构建命令 `npm run build`、输出目录 `dist`、生产分支 `main`。

## 踩坑

| 现象 | 原因 | 解法 |
| --- | --- | --- |
| 加完自定义域一直"待验证"，DNS 里也没有记录 | 授权 wrangler 的 OAuth 令牌没有 DNS 写权限，Pages 没自动建记录 | 手动加一条 `w` CNAME 指向 `chun-2wh.pages.dev`，橙云开启 |
| 深色模式刷新闪白一瞬 | 等 JS 读完主题再切，晚于首屏渲染 | 在 `<head>` 里同步执行一段内联脚本改 `class` |
| 卡片缺封面图时出现空洞 | 不想给每条都找图 | 按 id 哈希生成渐变底色 + 大字母，永不空缺 |
| GitHub 上推送时卡在授权 | 22 端口被拒、GCM 的 OAuth 页面按钮不可点 | 改用 SSH over 443（`ssh.github.com:443`） |
| 首页置顶项目和"最近"重复 | 两个区块都从同一个列表取 | 取最近时排除已置顶的 |

## 结果

跑通了，就是你现在看的这一页。三个主要界面长这样：

<div style="display:flex;flex-wrap:wrap;gap:12px;margin:1.5em 0">
  <img src="/covers/site-list.jpg" alt="全部项目列表：状态筛选、搜索、卡片网格" style="flex:1 1 280px;min-width:0;border-radius:12px" />
  <img src="/covers/site-detail.jpg" alt="项目详情页：状态、耗时花费、技术栈、正文" style="flex:1 1 280px;min-width:0;border-radius:12px" />
  <img src="/covers/site-notes.jpg" alt="折腾笔记列表：按年份分组" style="flex:1 1 280px;min-width:0;border-radius:12px" />
</div>

<p style="font-size:13px;color:var(--ink-mute);margin-top:-.6em">左：全部项目（按状态筛选 + 关键词搜索）｜中：项目详情（状态 / 耗时 / 花费 / 技术栈）｜右：笔记列表（按年份分组）</p>

- 53 个页面，构建 2 秒内
- 首屏零 JS，单页 HTML+CSS 不到 60KB
- 费用：托管 0 元，域名是原本就有的
- 发布体验：改一个 md，`git push`，一分钟内线上生效
- 统计：Cloudflare Web Analytics，无 Cookie，不影响首屏

值不值：**值**。写记录的阻力从"打开某个 App"降到"新建一个文件"，这才是能坚持下去的关键。

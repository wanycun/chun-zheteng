# CHUN折腾 · 个人网站搭建方案

> 目标：一个只放「我折腾过的项目」的静态个人站，内容用 Markdown 写，托管在 Cloudflare Pages，零成本，域名 `w.wanyc.xyz`。

---

## 1. 一句话定位

**CHUN折腾 = 一个折腾者的项目流水账**：做过什么、怎么做的、踩了哪些坑、最后跑没跑通。

不是博客、不是教程站、不是作品集门面。围绕「项目」组织内容，每个项目是一条完整的记录：动机 → 方案 → 过程 → 踩坑 → 结果 → 花费/耗时 → 后续更新。

---

## 2. 参考站拆解（haoyongzhai.com）

我先看了参考站，它的骨架是这样：

| 部分 | 参考站做法 |
|---|---|
| 顶栏 | Logo + 图标化导航（🏠首页 / 📦网盘 / 📖教程 / 🐳懒人包）+ 全站搜索 + 社媒图标 + 主题切换 |
| 首页 | 巨型 Hero（站名 + 一句话 + 数据：601 视频 / 30 图文 / 7 系统），下面是卡片网格 |
| 列表页 | 卡片 = 封面图 + 时长/日期 + 标题 + 标签 chips + 分页（12 页） |
| 详情页 | 长文 + 标签 + 页脚转载声明 |
| 其它 | RSS 订阅、关于本站、`llms.txt`（给 AI 读的站内目录） |

**借什么**：卡片网格 + 标签 chips + 状态徽标 + 搜索 + RSS + 关于页 + 极简顶栏。这套骨架对"大量条目 + 分类浏览"很合适，项目记录正好是这个形态。

**不借什么**：
- 它是 VitePress 的「文档站」观感（侧边栏、深目录），我们做项目站，改成更松的卡片流；
- 它是视频/教程聚合，内容形态是"外链到 B 站"；我们是自有长文，详情页要有信息密度；
- 12 页分页换成「标签筛选 + 状态筛选」，条目少于 100 时不需要页码。

---

## 3. 域名与品牌

| 项 | 确定值 | 说明 |
|---|---|---|
| 站点域名 | `w.wanyc.xyz` | 已核实 `wanyc.xyz` 的 NS 在 Cloudflare（`ernest.ns.cloudflare.com` / `arely.ns.cloudflare.com`），加个子域 CNAME 即可，不用改 NS、不影响主域 |
| 主域 | `wanyc.xyz` 保持原样 | 只借用 `w` 这个子域，将来主域做别的也不冲突 |
| 站点名 | **CHUN折腾** | 站内 H1、`<title>` 后缀、RSS、OG 图统一 |
| 副标题 | 折腾过的项目，都在这里 | Hero 区一句话 |
| canonical | `https://w.wanyc.xyz` | 全站绝对链接、sitemap 用这个 |
| favicon | 字母标 `C` + 齿轮点缀 | SVG，深浅色各一套 |
| 备用访问 | `chun.pages.dev`（Cloudflare 默认域） | 自定义域绑好后自动 301 到主域 |

**为什么用子域**：Pages 绑定自定义域时，Cloudflare 会自动建 CNAME 并签发证书，全程不用碰主域解析；出问题只影响这一个子域。

---

## 4. 网站结构（信息架构）

### 4.1 路由表

| 路由 | 页面 | 内容 |
|---|---|---|
| `/` | 首页 | Hero + 置顶项目 + 最近更新 + 标签云 |
| `/projects/` | 项目列表 | 全部项目卡片，可按「状态 / 标签」筛选，支持搜索 |
| `/projects/<slug>/` | 项目详情 | 一次折腾的完整记录（结构见 4.3） |
| `/notes/` | 折腾笔记 | 碎记录：一条命令、一个配置、一次踩坑，短平快，可选启用 |
| `/notes/<slug>/` | 笔记详情 | 短文 |
| `/tags/` | 标签总览 | 所有标签 + 数量 |
| `/tags/<tag>/` | 标签页 | 该标签下的项目与笔记 |
| `/about/` | 关于 | 我是谁、折腾些什么、联系方式 |
| `/search/` | 搜索（可选） | 本地全文搜索（Pagefind，纯静态） |
| `/rss.xml` | RSS | 项目 + 笔记混合订阅 |
| `/sitemap-index.xml` | 站点地图 | 提交搜索引擎用 |
| `/404` | 404 | 自定义 |

### 4.2 导航

顶栏：`CHUN折腾` · 项目 · 笔记 · 标签 · 关于 ｜ 右侧：搜索按钮 · 主题切换 · GitHub

移动端：折叠成汉堡菜单，标签行横向滚动。

### 4.3 首页分区（从上到下）

1. **Hero**：大字站名 `CHUN折腾` + 副标题 + 三个统计数字（项目 N 个 / 标签 N 个 / 最后更新 日期）
2. **置顶项目**（featured，1~3 个，大卡片，带封面图）
3. **最近更新**（最新 6~9 个项目卡片）
4. **标签云**（点击进标签页）
5. **页脚**：RSS、GitHub、备案信息位（可选）、版权

### 4.4 项目详情页结构

这是全站最重要的模板，固定骨架，写起来不纠结：

```
[状态徽标] [标题]
[一句话摘要 —— 30 秒读完做了什么、成没成]
时间：2026-03 起 · 耗时约 6 小时 · 花费 0 元
技术栈：Astro / Cloudflare Pages / Markdown
链接：仓库 · 演示

────────────────────────
1. 背景      为什么想搞这个
2. 方案      选了什么路，为什么不用另一条
3. 过程      关键步骤 + 命令/代码片段
4. 踩坑      错误信息 → 原因 → 解法（这块最值钱）
5. 结果      跑通没有、代价、值不值
6. 更新日志   时间线形式，随项目演进追加
────────────────────────
[标签] [相关项目]
```

---

## 5. 内容模型（frontmatter）

一个项目 = 一个 Markdown 文件，放 `src/content/projects/`。写新项目就是复制模板改字段。

```yaml
---
title: 用 Astro + Cloudflare Pages 搭本站
slug: chun-site
summary: 25 分钟建站，0 元托管，一条命令发布。
status: 已跑通          # 折腾中 / 已跑通 / 暂停 / 已废弃 / 翻车
startDate: 2026-03-01
endDate: 2026-03-02      # 可空 → 显示「进行中」
cost: 0                  # 花费（元）
hours: 6                 # 耗时（小时）
stack: [Astro, Tailwind, Cloudflare Pages]
tags: [建站, Cloudflare, 静态站]
cover: ./cover.jpg       # 可空 → 用渐变色块兜底
repo: https://github.com/xxx
demo: https://w.wanyc.xyz
featured: true           # 首页置顶
draft: false             # true 则不构建、不发布
changelog:
  - date: 2026-03-02
    note: 绑定自定义域名，全站上线
  - date: 2026-03-05
    note: 加 RSS 与 sitemap
---
```

**字段说明**：`status` 决定卡片徽标颜色；`cover` 缺失时按 `slug` 哈希生成一个渐变色块，所以不写封面也不丑；`draft: true` 的文件不会出现在线上。

笔记（`src/content/notes/`）字段更少：`title / date / tags / summary`。

---

## 6. 技术选型

| 层 | 选择 | 理由 |
|---|---|---|
| 框架 | **Astro 5** | 内容驱动，默认零 JS，`content collections` 原生支持 Markdown 类型校验，构建产物是纯静态 `dist/` |
| 样式 | **Tailwind CSS v4** | 原子类 + 设计 token，改主题改一处 |
| 内容 | Markdown / MDX | 写作 = 建文件，不需要后台 |
| 搜索 | Pagefind（可选二期） | 构建后生成静态索引，不依赖服务端 |
| 托管 | **Cloudflare Pages** | 免费、无限带宽、全球 CDN、自动 HTTPS |
| 部署 | `wrangler` 直传 | 本地 build 后上传，不依赖 GitHub；后续想接自动构建再加 |
| 运行时 | Node 24（已装） | `npx wrangler` 免装 |

**为什么不直接抄参考站的 VitePress**：VitePress 是文档站定位，侧边栏 + 深目录，塞项目卡片得反向对着默认样式打架；Astro 的布局完全自己写，卡片流、标签筛选、首页 Hero 都好实现，且同样零 JS。

**为什么不用 Next.js**：静态个人站用不上 SSR/RSC，Astro 构建更快、产物更小。

---

## 7. Cloudflare 托管方案

### 7.1 架构

```
本地 Markdown ──(npm run build)──> dist/ 静态文件
                                        │
                          npx wrangler pages deploy
                                        │
                                        ▼
                        Cloudflare Pages 项目 "chun"
                                        │
                         自定义域 w.wanyc.xyz（自动 CNAME + 证书）
```

### 7.2 免费额度（Pages）

- 带宽、请求：**不计量、不收费**
- 构建：500 次/月（本地部署方式其实不吃这个额度）
- 站点文件：单个项目 20,000 个文件上限
- 自定义域 + 自动 HTTPS：免费、自动续期

### 7.3 部署命令

```bash
npm run build            # 生成 dist/
npm run deploy           # = wrangler pages deploy dist --project-name chun
```

绑好域名后，**发布 = 改 Markdown + 跑一条 `npm run deploy`**，几十秒生效。

### 7.4 需要先连上 Cloudflare（要你配合一次）

本机目前没有 wrangler 凭据，二选一：

| 方式 | 操作 | 持久性 |
|---|---|---|
| **A. 浏览器登录（推荐）** | 我执行 `npx wrangler login`，浏览器弹授权页，你点一下「Allow」 | 凭据存本机，之后免登录 |
| B. API Token | 你在 CF 面板建一个 `Cloudflare Pages:Edit`（+ `Zone:DNS:Edit`）Token 发我 | 我直接写进本机环境变量 |

> 无论哪种：我不会把密钥写进代码或公开仓库，只存本地。域名绑定后由我验证 HTTPS、CNAME 和 404。

### 7.5 费用

| 项 | 费用 |
|---|---|
| 托管（Pages） | 0 |
| HTTPS 证书 | 0 |
| 域名 `wanyc.xyz` | 你已有的年费，本次不新增 |

---

## 8. 视觉设计

- **配色**：暗色优先。底色 `#0b0d10`，卡片 `#14171c`，文字 `#e6e8eb`；强调色「折腾橙」`#f97316`。亮色模式反相，同一套 token 切换。
- **字体**：中文系统栈（PingFang SC / 微软雅黑 / Noto Sans SC）；数字与代码用等宽（JetBrains Mono / Consolas），用来强化"折腾"的工程感。
- **卡片**：16:9 封面（或渐变兜底）+ 状态徽标（折腾中=橙 / 已跑通=绿 / 暂停=灰 / 已废弃=暗红）+ 标题 + 摘要两行截断 + 标签 chips + 日期。
- **动效**：hover 上浮 2px + 边框高亮；滚动淡入；全部尊重 `prefers-reduced-motion`。
- **响应式**：≤640 单列，641–1024 两列，>1024 三列。
- **SEO**：每页 title/description/OG/Twitter Card、JSON-LD（Person + TechArticle）、sitemap、RSS、语义化 HTML。

---

## 9. 实施步骤与交付物

| # | 步骤 | 产出 | 预计 |
|---|---|---|---|
| M0 | 方案确认（当前） | 本文档 | — |
| M1 | 初始化 Astro + Tailwind + 设计 token + 布局骨架 | 可 `npm run dev` 的空站 | 15 min |
| M2 | 内容集合 + 三个核心模板（首页 / 列表 / 详情） | 页面跑通，假数据 | 40 min |
| M3 | 标签页、关于页、RSS、sitemap、404、Pagefind 搜索 | 功能齐 | 25 min |
| M4 | 填 5 篇示例项目（真实结构，可替换） | 站内有内容可看 | 20 min |
| M5 | Cloudflare 登录 → 建 Pages 项目 → 绑 `w.wanyc.xyz` → 上线 | `https://w.wanyc.xyz` 可访问 | 20 min |
| M6 | 验收 + 写 `README.md`（怎么加项目、怎么发布、怎么改样式） | 交付文档 | 10 min |

**交付物**：
1. 可访问的 `https://w.wanyc.xyz`
2. 源码 + `README.md` 操作手册
3. 项目模板（新建项目一条 `npm run new:project` 或复制模板文件）

---

## 10. 需要你决定的三件事

1. **Cloudflare 授权**：浏览器登录（推荐，你点一下）还是给 API Token？
2. **示例内容**：M4 我先放 5 篇示例项目占位（结构是真的，内容你后面替换），还是只留 1 篇模板、站内先空着？
3. **「笔记」模块**：要不要？要 = 多一个 `/notes/` 短记录流；不要 = 全站只有项目，更聚焦。

---

## 11. 边界（这次不做）

- ❌ 评论系统（需要后端/第三方服务）
- ❌ 后台 CMS（Markdown 就是 CMS，改文件即改站）
- ❌ 用户登录、访问统计报表（可后加 Cloudflare Web Analytics，免费且无 Cookie）
- ❌ 图片上传服务（图片放仓库 `public/` 或外部图床）
- ❌ 中英双语（先中文，结构留好 i18n 位置）

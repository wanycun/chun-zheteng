# CHUN折腾

> 折腾过的项目，都在这里 —— <https://w.wanyc.xyz>

个人项目记录站。每个项目 = 一个 Markdown 文件，纯静态输出，托管在 Cloudflare Pages。

---

## 技术栈

| 层 | 用的什么 |
| --- | --- |
| 框架 | Astro 5（静态输出，默认零 JS） |
| 样式 | Tailwind CSS 4 + CSS 变量设计 token |
| 内容 | Markdown + Astro Content Collections（zod 校验） |
| 托管 | Cloudflare Pages（免费 / 全球 CDN / 自动 HTTPS） |
| 部署 | `wrangler pages deploy` 直传 |

---

## 目录结构

```
个人网站/
├── src/
│   ├── content.config.ts        # 内容集合的字段定义（改字段改这里）
│   ├── content/
│   │   ├── projects/            # 一个项目 = 一个 .md
│   │   └── notes/               # 一条笔记 = 一个 .md
│   ├── components/              # Header / Footer / 卡片 / 徽标
│   ├── layouts/Base.astro       # <head>、主题、SEO、JSON-LD
│   ├── lib/site.ts              # 站点名、简介、社交链接、工具函数
│   ├── pages/
│   │   ├── index.astro          # 首页
│   │   ├── projects/            # 列表 + 详情
│   │   ├── notes/               # 列表 + 详情
│   │   ├── tags/                # 标签总览 + 标签页
│   │   ├── about.astro          # 关于
│   │   ├── 404.astro
│   │   └── rss.xml.ts           # RSS
│   └── styles/global.css        # 设计 token + 组件样式 + 文章排版
├── public/
│   ├── favicon.svg
│   ├── og.png                   # 社交分享图（1200×630）
│   ├── robots.txt
│   └── _headers                 # Cloudflare Pages 响应头（缓存 / 安全）
├── scripts/
│   ├── new-project.mjs          # 新建项目/笔记的脚手架
│   └── make-og.py               # 重新生成 og.png
└── astro.config.mjs             # site 域名、sitemap、Tailwind 插件
```

---

## 本地开发

```bash
npm install
npm run dev        # http://localhost:4321
npm run build      # 输出到 dist/
npm run preview    # 预览 dist/ 的构建结果
```

---

## 写一篇新记录

### 方式一：用脚手架（推荐）

```bash
# 新项目
npm run new:project -- my-project "我的项目标题"

# 新笔记（前缀 note:）
npm run new:project -- note:my-note "一条笔记标题"
```

会在 `src/content/projects/`（或 `notes/`）生成一个带完整 frontmatter 和分节模板的文件，填完就能发。

### 方式二：手动复制

复制任意已有文件改个名字，注意 frontmatter 必须符合 `src/content.config.ts` 里的字段：

```yaml
title: 项目标题            # 必填
summary: 一句话摘要         # 必填，出现在卡片和列表
status: 已跑通             # 折腾中 / 已跑通 / 暂停 / 已废弃 / 翻车
startDate: 2026-10-20     # 必填
endDate: 2026-10-20       # 可空 → 显示「进行中」
cost: 0                   # 花费（元）
hours: 6                  # 耗时（小时），可空
stack: [Astro, Cloudflare] # 技术栈
tags: [建站, 静态站]        # 标签（同时决定 /tags/ 页面）
cover: /covers/xxx.jpg    # 可空 → 用按 id 生成的渐变色块
repo: https://github.com/xxx
demo: https://example.com
featured: true            # 首页靠前
draft: false              # true = 不构建、不发布
changelog:                # 更新日志（可选）
  - date: 2026-10-21
    note: 补了一段踩坑记录
```

**字段写错会在 `npm run build` 时直接报错**，不会静默丢内容。

### 建议的正文结构

```markdown
## 背景      为什么想搞
## 方案      选了什么路，为什么不用另一条
## 过程      关键步骤 + 命令/代码
## 踩坑      现象 → 原因 → 解法（用表格最好看）
## 结果      跑通没有、耗时、花费、值不值
```

这五个 `##` 会自动生成详情页右侧的目录。

---

## 发布

```bash
npm run deploy
# = astro build && wrangler pages deploy dist --project-name chun
```

第一次需要登录 Cloudflare：

```bash
npx wrangler login          # 浏览器点一下授权
npx wrangler whoami         # 确认当前账号
```

发布完几十秒生效。**改 Markdown → 跑一条命令 → 线上更新**，全程不需要登任何后台。

---

## 改站点信息

| 想改什么 | 改哪里 |
| --- | --- |
| 站点名 / 副标题 / 简介 / 域名 / 社交链接 | `src/lib/site.ts` |
| 首页 Hero 文案、按钮、统计 | `src/pages/index.astro` |
| 顶部导航项 | `src/components/Header.astro` 的 `nav` 数组 |
| 配色 / 圆角 / 字号 | `src/styles/global.css` 里的 `:root` 与 `.dark` 变量 |
| 关于页正文 | `src/pages/about.astro` |
| 社交分享图 | 改 `scripts/make-og.py` 后重新运行（见下） |

重新生成分享图（需要 Python + Pillow）：

```bash
python scripts/make-og.py
```

---

## 部署信息

| 项 | 值 |
| --- | --- |
| Cloudflare Pages 项目名 | `chun` |
| 生产域名 | `w.wanyc.xyz` |
| 备用域名 | `chun.pages.dev` |
| DNS | `w` CNAME → `chun.pages.dev`（Proxy 开启） |
| 证书 | Cloudflare 自动签发，自动续期 |

绑自定义域：Cloudflare 面板 → Workers & Pages → `chun` → Custom domains → 添加 `w.wanyc.xyz`。

---

## 关于示例内容

仓库里现有的 **5 个项目 + 4 条笔记都是示例**，用来展示结构和排版。写自己的第一篇时：

1. 直接改文件名和内容，或删掉不要的
2. 别忘了一起改 `src/content/projects/` 里的 `chun-site.md`（它描述的就是本站本身，可以留着）

示例内容里的技术细节是真实可查的通用做法（robocopy、Cloudflare Tunnel、Astro content collections 等），
但**不代表你的真实经历**，替换成自己的记录即可。

---

## 已知取舍

- 不做评论、不做登录、不做后台 —— 因此也不需要数据库和服务器
- 搜索是浏览器端过滤（数据在页面里），项目数上百之后可以换 Pagefind
- 封面图手动放 `public/` 或外链；不写封面会用渐变兜底，所以永远不会出现空洞的灰块
- 主题默认跟随系统（深色优先），用户手动切换后记住选择

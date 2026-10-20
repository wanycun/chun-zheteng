#!/usr/bin/env node
/**
 * 新建项目 / 笔记的脚手架。
 *
 *   npm run new:project -- my-project "我的项目标题"
 *   npm run new:project -- note:my-note "一条笔记标题"
 *
 * 生成后直接编辑文件即可，dev 模式会自动热更新。
 */
import { mkdir, writeFile, access } from 'node:fs/promises';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const today = new Date().toISOString().slice(0, 10);

const args = process.argv.slice(2);
const rawSlug = args[0];
const rawTitle = args.slice(1).join(' ') || '未命名';

if (!rawSlug) {
  console.error('用法: npm run new:project -- <slug> "<标题>"');
  console.error('      npm run new:project -- note:<slug> "<标题>"');
  process.exit(1);
}

const isNote = rawSlug.startsWith('note:');
const slug = isNote ? rawSlug.slice(5) : rawSlug;
const dir = join(root, 'src', 'content', isNote ? 'notes' : 'projects');
const file = join(dir, `${slug}.md`);

const projectTemplate = `---
title: ${rawTitle}
summary: 一句话说清这次折腾做了什么、成没成。
status: 折腾中 # 折腾中 / 已跑通 / 暂停 / 已废弃 / 翻车
startDate: ${today}
# endDate: ${today}
cost: 0
# hours: 0
stack: []
tags: []
# cover: /covers/xxx.jpg
# repo: https://github.com/xxx
# demo: https://example.com
featured: false
# changelog:
#   - date: ${today}
#     note: 第一次记录
---

## 背景

为什么想搞这个？现在的痛点是什么。

## 方案

选了什么路，为什么不用另一条。

## 过程

关键步骤、命令、代码片段。

\`\`\`bash
echo "命令写这里"
\`\`\`

## 踩坑

| 现象 | 原因 | 解法 |
| --- | --- | --- |
| 报错了 | 为什么 | 怎么解的 |

## 结果

跑通没有、花了多少时间、值不值。
`;

const noteTemplate = `---
title: ${rawTitle}
date: ${today}
tags: []
summary: 一句话说明这条笔记解决什么问题。
---

正文。

\`\`\`bash
echo "命令写这里"
\`\`\`
`;

try {
  await access(file);
  console.error(`文件已存在: ${file}`);
  process.exit(1);
} catch {
  /* 不存在，继续 */
}

await mkdir(dir, { recursive: true });
await writeFile(file, isNote ? noteTemplate : projectTemplate, 'utf8');

console.log(`✓ 已创建 ${isNote ? '笔记' : '项目'}: ${file}`);
console.log('  下一步: 编辑内容 → npm run dev 预览 → npm run deploy 发布');

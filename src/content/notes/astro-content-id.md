---
title: Astro 5 内容集合里，slug 变成了 id
date: 2026-09-28
tags: [Astro, 建站, 踩坑]
summary: 从 Astro 4 升到 5 之后，entry.slug 全变 undefined，路由直接 404。原因和迁移办法都在这。
---

旧写法：

```astro
<a href={`/projects/${entry.slug}/`}>{entry.data.title}</a>
```

升级后页面上全是 `/projects/undefined/`。

原因：Astro 5 的 content collections 换了 **glob loader**，
`slug` 不再由文件名自动推导，统一改用 `id`（默认就是去掉扩展名的文件名）。

改三处就行：

```astro
<!-- 1. 生成路由 -->
export async function getStaticPaths() {
  const entries = await getCollection('projects');
  return entries.map((entry) => ({
    params: { slug: entry.id },
    props: { entry },
  }));
}
```

```astro
<!-- 2. 链接 -->
<a href={`/projects/${entry.id}/`}>…</a>
```

```ts
// 3. schema 里如果原来有 slug 字段，删掉或自己填
```

需要自定义 id（比如文件名里有空格或中文）时，给 glob loader 传 `generateId`：

```ts
import { glob } from 'astro/loaders';

export const collections = {
  projects: defineCollection({
    loader: glob({
      pattern: '**/*.md',
      base: './src/content/projects',
      generateId: ({ entry }) => entry.replace(/\.md$/, ''),
    }),
    schema: projectSchema,
  }),
};
```

不过更推荐直接用英文文件名，`id` 自动就是它，省一层维护。

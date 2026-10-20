import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

/** 项目状态：决定卡片徽标颜色与排序提示 */
export const STATUS = ['折腾中', '已跑通', '暂停', '已废弃', '翻车'] as const;

const projects = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/projects' }),
  schema: z.object({
    title: z.string(),
    summary: z.string(),
    status: z.enum(STATUS).default('折腾中'),
    startDate: z.coerce.date(),
    endDate: z.coerce.date().optional(),
    cost: z.number().default(0),
    hours: z.number().optional(),
    stack: z.array(z.string()).default([]),
    tags: z.array(z.string()).default([]),
    /** 封面图：public 下的路径或外链，留空则用渐变兜底 */
    cover: z.string().optional(),
    repo: z.string().optional(),
    demo: z.string().optional(),
    featured: z.boolean().default(false),
    draft: z.boolean().default(false),
    changelog: z
      .array(z.object({ date: z.coerce.date(), note: z.string() }))
      .default([]),
  }),
});

const notes = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/notes' }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    tags: z.array(z.string()).default([]),
    summary: z.string().optional(),
    draft: z.boolean().default(false),
  }),
});

export const collections = { projects, notes };

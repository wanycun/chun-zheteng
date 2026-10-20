import rss from '@astrojs/rss';
import type { APIContext } from 'astro';
import { getCollection } from 'astro:content';
import { SITE } from '../lib/site';

export async function GET(context: APIContext) {
  const projects = (await getCollection('projects')).filter((p) => !p.data.draft);
  const notes = (await getCollection('notes')).filter((n) => !n.data.draft);

  const items = [
    ...projects.map((p) => ({
      title: p.data.title,
      pubDate: p.data.endDate ?? p.data.startDate,
      description: p.data.summary,
      link: `/projects/${p.id}/`,
      categories: p.data.tags,
    })),
    ...notes.map((n) => ({
      title: n.data.title,
      pubDate: n.data.date,
      description: n.data.summary ?? '',
      link: `/notes/${n.id}/`,
      categories: n.data.tags,
    })),
  ].sort((a, b) => b.pubDate.getTime() - a.pubDate.getTime());

  return rss({
    title: SITE.name,
    description: SITE.description,
    site: context.site ?? SITE.url,
    items,
    customData: `<language>zh-cn</language>`,
  });
}

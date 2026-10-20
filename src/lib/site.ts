export const SITE = {
  name: 'CHUN折腾',
  tagline: '折腾过的项目，都在这里',
  description:
    'CHUN 折腾记——把折腾过的软硬件项目记下来：为什么搞、怎么搞、踩了哪些坑、最后跑没跑通。',
  url: 'https://w.wanyc.xyz',
  author: 'CHUN',
  lang: 'zh-CN',
  /** 页脚 / 关于页展示，留空则不渲染 */
  social: {
    github: 'https://github.com/wanycun/chun-zheteng',
    email: '',
  },
  /** Cloudflare Web Analytics 站点 token；留空则不注入统计脚本 */
  analytics: {
    token: '894af42870f64bf0a1a4408722bd11ad',
  },
};

/** 状态 → 颜色 key（对应 global.css 里的 .badge[data-status]） */
export const STATUS_COLOR: Record<string, string> = {
  折腾中: 'warn',
  已跑通: 'ok',
  暂停: 'idle',
  已废弃: 'idle',
  翻车: 'bad',
};

export function formatDate(date: Date): string {
  return date.toISOString().slice(0, 10);
}

export function isoDate(date: Date): string {
  return date.toISOString().slice(0, 10);
}

/** 无封面时，按 id 生成一个稳定的渐变色块 */
export function gradientFor(seed: string): string {
  let h = 0;
  for (let i = 0; i < seed.length; i++) h = (h * 31 + seed.charCodeAt(i)) % 360;
  const hue = h;
  return `linear-gradient(135deg, hsl(${hue} 52% 22%) 0%, hsl(${(hue + 42) % 360} 58% 11%) 100%)`;
}

/** 粗略估阅读时长：中文按 400 字/分钟，英文按 200 词/分钟 */
export function readingTime(markdown: string): number {
  const text = markdown.replace(/```[\s\S]*?```/g, ' ');
  const cjk = (text.match(/[\u4e00-\u9fa5]/g) || []).length;
  const words = (text.match(/[A-Za-z0-9_]+/g) || []).length;
  return Math.max(1, Math.round(cjk / 400 + words / 200));
}

export function tagSlug(tag: string): string {
  return encodeURIComponent(tag);
}

export function tagHref(tag: string): string {
  return `/tags/${tagSlug(tag)}/`;
}

/** 项目排序：进行中优先，其次按开始时间倒序 */
export function sortProjects<T extends { data: { startDate: Date; status: string } }>(a: T, b: T): number {
  const weight = (s: string) => (s === '折腾中' ? 0 : 1);
  const wa = weight(a.data.status);
  const wb = weight(b.data.status);
  if (wa !== wb) return wa - wb;
  return b.data.startDate.getTime() - a.data.startDate.getTime();
}

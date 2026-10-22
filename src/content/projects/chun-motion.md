---
title: 给这个站拍一支 25 秒的介绍片
summary: 站点是什么，20 秒说明白，比让人读 9 篇强。用 huashu-motion 把站自己的 UI 重建一遍：HTML + GSAP 写成片子，本地 Chrome 一帧一帧截，Edge TTS 念口播。
status: 已跑通
startDate: 2026-10-21
endDate: 2026-10-22
cost: 0
hours: 6
stack: [huashu-motion, GSAP, HTML/CSS, Edge TTS, FFmpeg, Chrome DevTools Protocol]
cover: /covers/chun-motion-cover.jpg
tags: [视频, 动效, TTS, 自动化]
demo: /media/chun-motion-site.mp4
changelog:
  - date: 2026-10-21
    note: 第一版，14.2 秒，只有音乐和音效，没有口播。
  - date: 2026-10-21
    note: 加 Edge TTS 口播（云希），片长拉到 23 秒，音乐自动给人声让位。
  - date: 2026-10-22
    note: 片头重做：徽标盖章 + 站名 + 网址，然后收进页头；加「关于这个站」打字面板。
  - date: 2026-10-22
    note: 口播换晓晓；第二句提到 1.1 倍速才塞得进打字段；母带归一到 -14 LUFS。
---

## 背景

站里 9 个项目，一个比一个长，每个都是几个月甚至半年的折腾。但打开首页，看到的只是 9 张卡片——
「这个站到底在干什么」这件事，得点进去读三篇才有感觉。

想用 20 秒把三件事说清楚：这是个什么站、里面记什么、还有几个没跑通。

## 方案

三条路都想过：

| 方案 | 好处 | 为什么没选 |
| --- | --- | --- |
| 屏幕录制 + 剪辑软件 | 快，所见即所得 | 镜头运动、转场全得手拖；改一个字要重录 |
| 自己写 HTML + GSAP 再录屏 | 画面完全可控 | 录屏会掉帧，时间轴对不准 |
| **写成片子，程序逐帧渲染** | 每一帧都是代码算出来的，改一行就是改一帧 | 要学一套工具 |

选了第三条，用的是 `huashu-motion` 这个 skill——它把「片子」定义成一个 HTML 文件加一条时间轴，
再用本地 Chrome 按时间戳逐帧截图、ffmpeg 合成。好处是**没有"渲染时偶发"这回事**：
同一帧不管播放到还是直接跳过去，出来的像素都一样。

画面全部照抄站点：深色主题那套 CSS 变量、C 徽标、卡片圆角、状态圆点、标签胶囊、等宽字那一行 `日期 · 技术栈`。
不发明任何视觉语言——片子应该看起来像这个站的一部分，而不是套在它外面的广告。

口播用 Edge TTS（微软的神经网络语音），走 [wangwangit/tts](https://github.com/wangwangit/tts) 那个服务的 OpenAI 兼容接口。

## 过程

成片先放这儿：

<div style="margin:1.5em 0">
  <video controls playsinline preload="metadata" poster="/covers/chun-motion-poster.jpg" src="/media/chun-motion-site.mp4" style="width:100%;border-radius:12px;border:1px solid var(--border);background:#0b0d10"></video>
</div>

<p style="font-size:13px;color:var(--ink-mute);margin-top:-.6em">25.4 秒 / 1920×1080 / 30fps，五句口播，音乐在人声下面让 12 dB 并挖掉 2 kHz。</p>

结构就六段：

1. **片头**（0–3.4s）——C 徽标盖章落下，站名滑进来，一句话 + 网址胶囊
2. **关于这个站**（3.4–9.6s）——片头收进页头，导航出现；一块终端面板逐字打出「把折腾过的软硬件项目记下来：为什么搞、怎么搞、踩了哪些坑」
3. **项目墙**（9.6–14.3s）——筛选胶囊 + 9 张卡按时间倒序落位，间隔从 0.55 秒收缩到 0.42 秒
4. **扫光**（14.3–17.3s）——整墙推近，一道橙线从上扫下来
5. **停顿**（17.3–20.3s）——压暗，一句话：每一个都是一次真实的动手
6. **落款**（20.3–25.4s）——站名 + 网址

口播五句不是整段合成的，是**一句一句生成再拼**：

```bash
# 每句单独合成（Edge TTS，OpenAI 兼容接口）
curl -s https://tts.wangwangit.com/v1/audio/speech \
  -H 'Content-Type: application/json' \
  -d '{"model":"tts-1","input":"这是我的个人纯折腾网站。","voice":"zh-CN-XiaoxiaoNeural","speed":1.0}' \
  -o n1.mp3

# 按剪辑点拼到时间轴上：0.4s / 3.8s / 10.1s / 17.25s / 20.75s
ffmpeg -i n1.wav -i n2.wav -i n3.wav -i n4.wav -i n5.wav -filter_complex \
  "[0:a]adelay=400:all=1[a];[1:a]adelay=3800:all=1[b];[2:a]adelay=10100:all=1[c];\
   [3:a]adelay=17250:all=1[d];[4:a]adelay=20750:all=1[e];\
   [a][b][c][d][e]amix=inputs=5:normalize=0[out]" -map "[out]" voice.wav
```

这么干的好处：每句话钉死在某个段落上，画面改了就调 `adelay` 的数字，不用让整段音频自己凑。
坏处是句与句之间的呼吸感得自己设计，不能靠 AI 一口气念完的自然停顿。

## 踩坑

| 现象 | 原因 | 解法 |
| --- | --- | --- |
| 一开始每张截图都超时，浏览器"起来就退" | 这台机器的 DSH 是管理员权限跑的，Chrome 拒绝以管理员启动，会自己降权重开、启动器瞬间退出；而工具把"启动器退出"当成"浏览器死了" | 改走 WebSocket 版 CDP，并容忍启动器进程退出 |
| 1080p 截图必断连（1006，可复现） | Chrome 155 在 WebSocket 通道上回大 PNG 会直接把连接掐掉，但 JPEG 正常 | 抓 q100 JPEG，再用 ffmpeg 转 PNG，上层调用方完全无感 |
| 卡片排到第三行被画幅切掉 | `height: 252px` + `padding: 38px`，默认 `content-box`，实际占 290 | 全程 `box-sizing: border-box` |
| 打字机效果不动，文字一次性全出来 | 元素上挂了 `data-var-text`，运行时把文本重写回整段，把逐字 `<span>` 冲掉了 | 改成从 `OM.vars()` 取文本、代码里自己拆字 |
| 扫光被判成"布局动画"报错 | 动的是 `top` | 改成 transform 的 `y` |
| 调口播接口 403 | Cloudflare 拦脚本 UA | 带上浏览器 UA 和 Referer |
| Kokoro 的中文听着不对 | 它的中文走 espeak，没有声调，工具自己都警告了 | 换 Edge TTS |
| 音乐盖住人声 | 人声原始电平只有 -24.9 LUFS | 人声归一到 -11.5，`om sound` 自动把音乐压 12 LU、在 2 kHz 挖洞 |
| 第二句口播超时 | 晓晓念 6.29 秒，会盖过打字段收尾 | 这一句单独提到 1.1 倍速（6.29 → 5.71 秒），其余保持原速 |

## 结果

<div style="display:flex;flex-wrap:wrap;gap:12px;margin:1.5em 0">
  <img src="/covers/chun-motion-about.jpg" alt="关于这个站：终端面板逐字打出站点介绍" style="flex:1 1 280px;min-width:0;border-radius:12px" />
  <img src="/covers/chun-motion-wall.jpg" alt="9 张项目卡整墙落定" style="flex:1 1 280px;min-width:0;border-radius:12px" />
</div>

<p style="font-size:13px;color:var(--ink-mute);margin-top:-.6em">左：逐字打出的「关于这个站」，底部一条进度条走满｜右：9 张项目卡落定之后的整墙。</p>

- 25.4 秒 / 1920×1080 / 30fps，H.264 + AAC，**-14.2 LUFS**（社交平台不用再压）
- 全程可改：在 studio 里按 C 点画面上任何一处提意见，改的就是那一帧，不用重剪
- 片头有两条音色版本（云希 / 晓晓），最后留下的是晓晓
- 花费 0 元：Chrome 是现成的，TTS 免费，渲染在本机跑

一个副作用：片子里说「九个项目」，而这篇加进来之后站里就是 **10 个** 了。
片子是先拍的，这是时间顺序，不是 bug——下次拍就得说十个了。

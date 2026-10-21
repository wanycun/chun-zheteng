"""把横向的浏览器截图做成 1200x675 的项目封面：截图铺底 + 左侧渐变压暗 + 文字。"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1200, 675
ORANGE = (249, 115, 22)
WHITE = (231, 233, 236)
GRAY = (166, 171, 180)
DIM = (109, 115, 125)
FONT_DIR = "C:/Windows/Fonts"


def pick(names):
    for n in names:
        p = os.path.join(FONT_DIR, n)
        if os.path.exists(p):
            return p
    raise SystemExit("font not found")


BOLD = pick(["msyhbd.ttc", "msyh.ttc", "simhei.ttf"])
REG = pick(["msyh.ttc", "simhei.ttf", "arial.ttf"])
MONO = pick(["consola.ttf", "CascadiaMono.ttf", "arial.ttf"])

src, out = sys.argv[1], sys.argv[2]

shot = Image.open(src).convert("RGB")
# 去掉浏览器/站点头部，让正文成为主体
shot = shot.crop((0, 78, shot.width, shot.height))

# 等比铺满
scale = max(W / shot.width, H / shot.height)
shot = shot.resize((max(W, int(shot.width * scale)), max(H, int(shot.height * scale))), Image.LANCZOS)
left = (shot.width - W) // 2
top = (shot.height - H) // 2
shot = shot.crop((left, top, left + W, top + H))

img = shot.convert("RGBA")

# 左侧渐变压暗（保证文字可读）
grad = Image.new("L", (W, 1), 0)
gd = ImageDraw.Draw(grad)
for x in range(W):
    t = x / 620.0
    a = 242 if t < 1 else max(0, 242 * (1 - (t - 1) / 0.35))
    gd.point((x, 0), int(a))
grad = grad.resize((W, H))
overlay = Image.new("RGBA", (W, H), (8, 10, 13, 255))
overlay.putalpha(grad)
img = Image.alpha_composite(img, overlay)

# 整体再压一点，避免截图太抢
img = Image.alpha_composite(img, Image.new("RGBA", (W, H), (8, 10, 13, 40)))

img = img.convert("RGB")
d = ImageDraw.Draw(img)
PAD = 84

d.rectangle([PAD, 176, PAD + 52, 181], fill=ORANGE)
d.text((PAD, 200), "CHUN折腾", font=ImageFont.truetype(BOLD, 76), fill=WHITE)
d.text((PAD, 318), "个人项目记录站 · 自己搭的", font=ImageFont.truetype(REG, 30), fill=GRAY)

# 等宽字体（Consolas）没有中文字形，英文段用等宽、中文段回退到雅黑
mono_f = ImageFont.truetype(MONO, 21)
reg_f = ImageFont.truetype(REG, 21)
seg_x = PAD
for seg, f in [("Astro · Cloudflare Pages · ", mono_f), ("GitHub 自动部署", reg_f)]:
    d.text((seg_x, 372), seg, font=f, fill=DIM)
    seg_x += d.textlength(seg, font=f)

tag_font = ImageFont.truetype(REG, 22)
x = PAD
for label in ["已跑通", "持续使用中"]:
    w = d.textlength(label, font=tag_font)
    d.rounded_rectangle([x, 442, x + w + 28, 484], radius=999, outline=ORANGE, width=1)
    d.text((x + 14, 452), label, font=tag_font, fill=ORANGE)
    x += w + 44

img.save(out, "JPEG", quality=88, optimize=True)
print("written:", out, img.size)

"""生成 1200x630 的社交分享图（og.png）。"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1200, 630
BG = (11, 13, 16)
ORANGE = (249, 115, 22)
WHITE = (231, 233, 236)
GRAY = (166, 171, 180)
DIM = (109, 115, 125)

FONT_DIR = "C:/Windows/Fonts"
BOLD_CANDIDATES = ["msyhbd.ttc", "msyh.ttc", "simhei.ttf", "arialbd.ttf"]
REG_CANDIDATES = ["msyh.ttc", "simhei.ttf", "arial.ttf"]
MONO_CANDIDATES = ["consola.ttf", "CascadiaMono.ttf", "arial.ttf"]


def pick(cands):
    for c in cands:
        p = os.path.join(FONT_DIR, c)
        if os.path.exists(p):
            return p
    raise SystemExit("no usable font found")


def font(path, size):
    return ImageFont.truetype(path, size)


bold_path = pick(BOLD_CANDIDATES)
reg_path = pick(REG_CANDIDATES)
mono_path = pick(MONO_CANDIDATES)

img = Image.new("RGB", (W, H), BG)

# 柔光：两团橙色/蓝色光晕
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([-260, -420, 620, 260], fill=(249, 115, 22, 46))
gd.ellipse([720, -460, 1500, 180], fill=(59, 130, 246, 34))
glow = glow.filter(ImageFilter.GaussianBlur(120))
img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")

d = ImageDraw.Draw(img)

PAD = 88

# 顶部 C 标（弧线）
cx, cy, r, sw = PAD + 26, 150, 26, 9
d.arc([cx - r, cy - r, cx + r, cy + r], start=38, end=322, fill=ORANGE, width=sw)

# 小标签
small = font(reg_path, 24)
d.text((PAD + 76, 128), "个人项目流水账 · w.wanyc.xyz", font=small, fill=DIM)

# 主标题 CHUN折腾
big = font(bold_path, 118)
x, y = PAD - 6, 236
d.text((x, y), "CHUN", font=big, fill=WHITE)
chun_w = d.textlength("CHUN", font=big)
d.text((x + chun_w, y), "折腾", font=big, fill=ORANGE)

# 分割线
d.line([(PAD, 418), (PAD + 92, 418)], fill=ORANGE, width=5)

# 副标题
tagline = font(reg_path, 34)
d.text((PAD, 452), "折腾过的项目，都在这里", font=tagline, fill=GRAY)

# 说明
desc = font(reg_path, 24)
d.text((PAD, 512), "做过什么 · 怎么做的 · 踩了哪些坑 · 跑没跑通", font=desc, fill=DIM)

# 右下角域名
mono = font(mono_path, 26)
domain = "w.wanyc.xyz"
dw = d.textlength(domain, font=mono)
d.text((W - PAD - dw, H - PAD - 8), domain, font=mono, fill=DIM)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "public", "og.png")
img.save(out, "PNG", optimize=True)
print("written:", os.path.abspath(out), img.size)

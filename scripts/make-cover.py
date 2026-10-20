"""把手机截图做成 1200x675 的项目封面（左文右图）。"""
import os
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1200, 675
BG = (11, 13, 16)
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

shot_path = sys.argv[1]
out_path = sys.argv[2]

# ── 背景光晕 ───────────────────────────────────────────────
img = Image.new("RGB", (W, H), BG)
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([-300, -380, 620, 300], fill=(249, 115, 22, 46))
gd.ellipse([760, -420, 1560, 220], fill=(59, 130, 246, 34))
glow = glow.filter(ImageFilter.GaussianBlur(120))
img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")

# ── 右侧手机截图 ───────────────────────────────────────────
shot = Image.open(shot_path).convert("RGB")
target_h = 620
scale = target_h / shot.height
shot = shot.resize((max(1, int(shot.width * scale)), target_h), Image.LANCZOS)

radius = 34
mask = Image.new("L", shot.size, 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, shot.width - 1, shot.height - 1], radius=radius, fill=255)

px = W - shot.width - 96
py = (H - target_h) // 2

# 手机轮廓暗影
shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(shadow).rounded_rectangle(
    [px - 10, py - 10, px + shot.width + 10, py + shot.height + 10], radius=radius + 8, fill=(0, 0, 0, 150)
)
shadow = shadow.filter(ImageFilter.GaussianBlur(28))
img = Image.alpha_composite(img.convert("RGBA"), shadow).convert("RGB")

img.paste(shot, (px, py), mask)

# 细边框
d = ImageDraw.Draw(img)
d.rounded_rectangle([px, py, px + shot.width - 1, py + shot.height - 1], radius=radius, outline=(42, 47, 56), width=2)

# ── 左侧文字 ───────────────────────────────────────────────
PAD = 84
d.text((PAD, 196), "车来了", font=ImageFont.truetype(BOLD, 88), fill=WHITE)

d.rectangle([PAD, 318, PAD + 64, 323], fill=ORANGE)

d.text((PAD, 356), "广州实时公交 · 自建网页版", font=ImageFont.truetype(REG, 32), fill=GRAY)
d.text((PAD, 410), "飞牛 NAS 上跑服务 · iPhone 打开即用", font=ImageFont.truetype(REG, 24), fill=DIM)

# 底部标签
tag_font = ImageFont.truetype(REG, 22)
x = PAD
for label in ["已跑通", "在持续使用"]:
    w = d.textlength(label, font=tag_font)
    d.rounded_rectangle([x, 492, x + w + 28, 534], radius=999, outline=(249, 115, 22), width=1)
    d.text((x + 14, 502), label, font=tag_font, fill=ORANGE)
    x += w + 44

img.save(out_path, "JPEG", quality=88, optimize=True)
print("written:", out_path, img.size)

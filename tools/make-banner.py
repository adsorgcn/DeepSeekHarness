# -*- coding: utf-8 -*-
# 生成仓库社媒头图（GitHub social preview）——工程书地板：无渐变、无紫色、无光晕、无圆角卡片。
# 纯排版海报：墨色底 + 白色大字 + 一点朱砂。受众=纯新手，卖的是「DSH 全套」，冲击力在文案。
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 640
INK = (18, 18, 22)
PAPER = (246, 244, 240)
VERMILION = (228, 87, 46)
FAINT = (150, 148, 158)

FONT_DIR = r"C:\Windows\Fonts"
def font(name, size):
    for n in name:
        p = os.path.join(FONT_DIR, n)
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()

heiti = font(["msyhbd.ttc", "msyh.ttc", "simhei.ttf"], 84)
heiti_small = font(["msyhbd.ttc", "msyh.ttc", "simhei.ttf"], 34)
mono = font(["consola.ttf", "cour.ttf"], 26)

img = Image.new("RGB", (W, H), INK)
d = ImageDraw.Draw(img)

# 左上：仓库地址（小字等宽）
d.text((64, 48), "github.com/adsorgcn/DeepSeekHarness", font=mono, fill=FAINT)

# 中线：两句文案
d.text((64, 210), "别人的 DSH 是个聊天框。", font=heiti, fill=PAPER)
d.text((64, 330), "你的，", font=heiti, fill=PAPER)
w1 = d.textlength("你的，", font=heiti)
d.text((64 + w1, 330), "一句话满配。", font=heiti, fill=VERMILION)

# 底部：套装清单
d.text((64, 500), "记忆体 · 新手教程 · 一键安装 · 技能库", font=heiti_small, fill=FAINT)

# 一条朱砂竖线：唯一的结构性装饰
d.rectangle([44, 210, 52, 438], fill=VERMILION)

out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
os.makedirs(out, exist_ok=True)
path = os.path.join(out, "social-preview.png")
img.save(path)
print("OK", path)

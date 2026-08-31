# -*- coding: utf-8 -*-
# Create English variants of the CorpID logined header images:
#   corpid_logined_header.jpg   -> corpid_logined_header_en.jpg
#   corpid_logined_header_2.jpg -> corpid_logined_header_2_en.jpg
# Replaces the baked-in Chinese "搜尋" placeholder and "AI 助手" button text
# with "Search" and "AI Assistant", sampling background colors from the image.

import io
from PIL import Image, ImageDraw, ImageFont

BASE = r"C:/Projects/CorpID/Mock-HTML/Mobile/IAM_To_CorpID/images"

ARIAL = r"C:/Windows/Fonts/arial.ttf"
ARIAL_BD = r"C:/Windows/Fonts/arialbd.ttf"

def median_color(img, box, dark_only=False):
    """Median color of pixels in box; if dark_only, use the darkest quartile."""
    region = img.crop(box).convert("RGB")
    px = list(region.getdata())
    if dark_only:
        px.sort(key=lambda p: p[0] + p[1] + p[2])
        px = px[: max(1, len(px) // 4)]
    n = len(px)
    r = sorted(p[0] for p in px)[n // 2]
    g = sorted(p[1] for p in px)[n // 2]
    b = sorted(p[2] for p in px)[n // 2]
    return (r, g, b)

def process(src, dst):
    img = Image.open(src).convert("RGB")
    draw = ImageDraw.Draw(img)

    # --- "搜尋" placeholder on the white search pill (orig coords ~x160..250, y790..838) ---
    white = median_color(img, (270, 795, 320, 840))           # blank pill area right of text
    gray = median_color(img, (160, 792, 250, 838), dark_only=True)  # glyph pixels
    draw.rectangle([148, 782, 265, 850], fill=white)
    f_search = ImageFont.truetype(ARIAL, 44)
    draw.text((160, 816), "Search", font=f_search, fill=gray, anchor="lm")

    # --- "AI 助手" blue pill (text ~x980..1085, y780..825; pill ~x905..1155, y757..853) ---
    blue = median_color(img, (920, 792, 950, 822))            # pill interior left of text
    draw.rectangle([965, 770, 1105, 842], fill=blue)
    # fit "AI Assistant" into the pill interior (width <= 240px), centered
    size = 48
    while size > 10:
        f_ai = ImageFont.truetype(ARIAL_BD, size)
        if draw.textlength("AI Assistant", font=f_ai) <= 240:
            break
        size -= 2
    draw.text((1032, 806), "AI Assistant", font=f_ai, fill=(255, 255, 255), anchor="mm")

    img.save(dst  , quality=92)
    print("saved", dst, "| white", white, "| gray", gray, "| blue", blue, "| ai size", size)

process(BASE + r"/corpid_logined_header.jpg", BASE + r"/corpid_logined_header_en.jpg")
process(BASE + r"/corpid_logined_header_2.jpg", BASE + r"/corpid_logined_header_2_en.jpg")

# -*- coding: utf-8 -*-
# Stamp the white QR icon from the ver5b-style CorpID header onto the
# ver6b-style header (same position), for both the Chinese originals and
# the English variants. Only near-white pixels are transferred
# (alpha = whiteness), so the destination's blue-sky background is preserved.
from PIL import Image

BASE = r"C:/Projects/CorpID/Mock-HTML/Mobile/IAM_To_CorpID/images"

def stamp_qr(src_path, dst_path):
    src = Image.open(src_path).convert("RGB")
    dst = Image.open(dst_path).convert("RGB")

    # 1. locate the QR icon in the source: near-white pixels in the right-side sky area
    RX0, RY0, RX1, RY1 = 1000, 520, 1180, 670
    minx, miny, maxx, maxy = RX1, RY1, RX0, RY0
    sp = src.load()
    for y in range(RY0, RY1):
        for x in range(RX0, RX1):
            r, g, b = sp[x, y][:3]
            if min(r, g, b) > 220:
                minx = min(minx, x); maxx = max(maxx, x)
                miny = min(miny, y); maxy = max(maxy, y)
    print("icon bbox in", src_path.rsplit('/', 1)[-1], ":", (minx, miny, maxx, maxy))

    # 2. build a white RGBA overlay with alpha = whiteness of the source pixels
    box = (minx - 4, miny - 4, maxx + 5, maxy + 5)
    patch = src.crop(box)
    w, h = patch.size
    overlay = Image.new("RGBA", (w, h))
    op = overlay.load()
    pp = patch.load()
    for y in range(h):
        for x in range(w):
            r, g, b = pp[x, y][:3]
            a = (min(r, g, b) - 140) / 90.0
            a = 0.0 if a < 0 else (1.0 if a > 1 else a)
            op[x, y] = (255, 255, 255, int(a * 255))

    # 3. composite onto the destination at the same coordinates
    region = dst.crop(box).convert("RGBA")
    region.alpha_composite(overlay)
    dst.paste(region.convert("RGB"), box)

    dst.save(dst_path, quality=92)
    print("saved", dst_path, "patch at", box)

stamp_qr(BASE + r"/corpid_logined_header.jpg",    BASE + r"/corpid_logined_header_2.jpg")
stamp_qr(BASE + r"/corpid_logined_header_en.jpg", BASE + r"/corpid_logined_header_2_en.jpg")

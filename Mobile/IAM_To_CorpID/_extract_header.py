import cv2
import numpy as np
import sys

SRC = sys.argv[1] if len(sys.argv) > 1 else r"D:/Projects/CorpID/Mock-HTML/mock-images/IAM_Homepage.jpg"
DST = sys.argv[2] if len(sys.argv) > 2 else r"D:/Projects/CorpID/Mock-HTML/mock-images/iam_home_header.jpg"
NAME_X1 = int(sys.argv[3]) if len(sys.argv) > 3 else 310  # right edge of 2nd-line text rect

img = cv2.imread(SRC)
# Crop the hero photo: full width, top of screen down to just above the white card
crop = img[0:500, 0:1206].copy().astype(np.float32)
H, W = crop.shape[:2]

def feather_blend(base, fill, x0, y0, x1, y1, dilate_px=15, blur_sigma=8.0):
    m = np.zeros(base.shape[:2], np.uint8)
    cv2.rectangle(m, (x0, y0), (x1, y1), 255, -1)
    soft = cv2.dilate(m, np.ones((dilate_px, dilate_px), np.uint8))
    soft = cv2.GaussianBlur(soft, (0, 0), blur_sigma).astype(np.float32) / 255.0
    soft3 = cv2.merge([soft, soft, soft])
    return fill * soft3 + base * (1 - soft3)

def vfill(im, x0, y0, x1, y1, anchor=6, blur_sigma=10.0):
    """Fill rect by per-column vertical interpolation between the rows just
    above and below the rect, then smooth."""
    out = im.copy()
    top = im[y0 - anchor, x0:x1].copy()
    bot = im[y1 + anchor, x0:x1].copy()
    n = y1 - y0
    t = (np.arange(n, dtype=np.float32) / max(n - 1, 1))[:, None, None]
    patch = top[None, :, :] * (1 - t) + bot[None, :, :] * t
    out[y0:y1, x0:x1] = patch
    out = cv2.GaussianBlur(out, (0, 0), blur_sigma)
    return feather_blend(im, out, x0, y0, x1, y1)

out = crop.copy()
# Only remove the left-hand-side text; keep status bar and weather pill in the photo.
# "登入 >" first (lower rect), then "午安" above it (its lower anchor is then clean)
out = vfill(out, 30, 295, NAME_X1, 410)
out = vfill(out, 30, 190, 210, 285)

out = np.clip(out, 0, 255).astype(np.uint8)
# Pad the bottom (replicate) so the photo fills the hero down to the white card
out = cv2.copyMakeBorder(out, 0, 40, 0, 0, cv2.BORDER_REPLICATE)
cv2.imwrite(DST, out, [cv2.IMWRITE_JPEG_QUALITY, 92])
print("saved", DST, out.shape)

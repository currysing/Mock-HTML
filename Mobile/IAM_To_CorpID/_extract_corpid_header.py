import cv2
import numpy as np

SRC = r"D:/Projects/CorpID/Mock-HTML/mock-images/CorpID_logined.jpg"
DST = r"D:/Projects/CorpID/Mock-HTML/mock-images/corpid_logined_header.jpg"

img = cv2.imread(SRC)
# Hero photo: top of screen down to where the light content card starts
crop = img[0:935, 0:1206].copy().astype(np.float32)
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
    out[y0:y1, x0:x1] = top[None, :, :] * (1 - t) + bot[None, :, :] * t
    out = cv2.GaussianBlur(out, (0, 0), blur_sigma)
    return feather_blend(im, out, x0, y0, x1, y1)

out = crop.copy()
# Remove only the left-side identity text; keep status bar, logo, pills,
# right-side QR icon and the search bar in the photo.
out = vfill(out, 45, 355, 490, 450)    # 測試員 + eye + small QR
out = vfill(out, 45, 495, 480, 585)    # 仁一有限公司
out = vfill(out, 45, 600, 920, 690)    # BELIZABETH HK LIMITED

cv2.imwrite(DST, np.clip(out, 0, 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 92])
print("saved", DST, out.shape)

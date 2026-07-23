import os
from PIL import Image, ImageDraw, ImageFont

# Set output folder
output_dir = "generated_buttons"
os.makedirs(output_dir, exist_ok=True)

# 1. ADJUST SIZE & CORNERS HERE
width, height = 360, 120    # Updated to 360px width x 120px height
corner_radius = 45          # Greatly increased for highly rounded pill-shaped corners

# Color profiles
green_bg = (24, 106, 81, 255)  
blue_bg = (0, 90, 204, 255)    
white = (255, 255, 255, 255)
cyan = (0, 210, 200, 255)

def draw_pill_rectangle(draw, x0, y0, x1, y1, radius, fill):
    """Draws a smooth anti-aliased rounded button container."""
    draw.rectangle([x0 + radius, y0, x1 - radius, y1], fill=fill)
    draw.rectangle([x0, y0 + radius, x1, y1 - radius], fill=fill)
    draw.pieslice([x0, y0, x0 + radius * 2, y0 + radius * 2], 180, 270, fill=fill)
    draw.pieslice([x1 - radius * 2, y0, x1, y0 + radius * 2], 270, 360, fill=fill)
    draw.pieslice([x0, y1 - radius * 2, x0 + radius * 2, y1], 90, 180, fill=fill)
    draw.pieslice([x1 - radius * 2, y1 - radius * 2, x1, y1], 0, 90, fill=fill)

def get_font(size):
    """Finds a system fallback CJK sans-serif font for Chinese layout."""
    font_names = ["msjh.ttc", "msjh.ttf", "NotoSansTC-Regular.otf", "PingFang.ttc", "Arial Unicode.ttf"]
    for name in font_names:
        try: return ImageFont.truetype(name, size)
        except IOError: continue
    return ImageFont.load_default()

# ----------------- GENERATE GREEN BUTTON (個人) -----------------
img_green = Image.new("RGBA", (width, height), (0, 0, 0, 0))
draw_g = ImageDraw.Draw(img_green)
draw_pill_rectangle(draw_g, 0, 0, width, height, corner_radius, fill=green_bg)

# Draw Redesigned Smartphone Vector Asset
px, py = 45, 30
pw, ph = 42, 60
pr = 8
draw_g.rectangle([px, py + pr, px + pw, py + ph - pr], fill=green_bg, outline=white, width=3)
draw_g.rectangle([px + pr, py, px + pw - pr, py + ph], fill=green_bg, outline=white, width=3)
draw_g.pieslice([px, py, px + pr*2, py + pr*2], 180, 270, fill=green_bg, outline=white, width=3)
draw_g.pieslice([px + pw - pr*2, py, px + pw, py + pr*2], 270, 360, fill=green_bg, outline=white, width=3)
draw_g.pieslice([px, py + ph - pr*2, px + pr*2, py + ph], 90, 180, fill=green_bg, outline=white, width=3)
draw_g.pieslice([px + pw - pr*2, py + ph - pr*2, px + pw, py + ph], 0, 90, fill=green_bg, outline=white, width=3)
draw_g.rectangle([px + 2, py + 2, px + pw - 2, py + ph - 2], fill=green_bg)
draw_g.line([px + 15, py + ph - 6, px + pw - 15, py + ph - 6], fill=white, width=2)
draw_g.ellipse([px + 15, py + 16, px + 27, py + 28], fill=green_bg, outline=white, width=2)
draw_g.arc([px + 9, py + 28, px + 33, py + 44], 180, 360, fill=white, width=2)
draw_g.rectangle([px - 12, py, px - 7, py + 5], fill=white)
draw_g.rectangle([px - 6, py - 8, px - 1, py - 3], fill=white)
draw_g.rectangle([px - 15, py - 10, px - 11, py - 6], fill=white)
draw_g.rectangle([px - 2, py + 8, px + 3, py + 13], fill=white)

# Render Text
font = get_font(40)
draw_g.text((140, 34), "個人", fill=white, font=font)
img_green.save(os.path.join(output_dir, "green_button_rounded.png"))


# ----------------- GENERATE BLUE BUTTON (企業) -----------------
img_blue = Image.new("RGBA", (width, height), (0, 0, 0, 0))
draw_b = ImageDraw.Draw(img_blue)
draw_pill_rectangle(draw_b, 0, 0, width, height, corner_radius, fill=blue_bg)

# Draw Redesigned iD Corp Vector Asset
idx, idy = 45, 34
draw_b.rectangle([idx + 16, idy, idx + 38, idy + 52], fill=blue_bg, outline=white, width=8)
draw_b.pieslice([idx + 14, idy, idx + 64, idy + 52], 270, 90, fill=blue_bg, outline=white, width=8)
draw_b.rectangle([idx + 18, idy + 7, idx + 36, idy + 45], fill=blue_bg)
draw_b.rectangle([idx, idy + 16, idx + 8, idy + 52], fill=white)
draw_b.rectangle([idx, idy, idx + 8, idy + 8], fill=cyan)

# Render Text
draw_b.text((140, 34), "企業", fill=white, font=font)
img_blue.save(os.path.join(output_dir, "blue_button_rounded.png"))

print("Successfully generated ultra-rounded buttons at 360x120px with alpha backgrounds!")

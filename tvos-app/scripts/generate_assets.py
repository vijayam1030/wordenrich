#!/usr/bin/env python3
"""Generates App Icon (layered) and Top Shelf assets for the tvOS app."""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = "WordEnrichTV/Assets.xcassets/AppIcon & Top Shelf Image.brandassets"
FONT_ROUNDED = "/System/Library/Fonts/SFNSRounded.ttf"

PURPLE = (102, 126, 234)   # #667eea
PURPLE_DARK = (90, 60, 180)
INDIGO = (76, 29, 149)     # deep indigo
INK = (30, 41, 59)         # #1e293b
WHITE = (255, 255, 255)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def diagonal_gradient(size, c1, c2):
    w, h = size
    img = Image.new("RGB", (w, h))
    px = img.load()
    diag = w + h
    for y in range(h):
        for x in range(0, w, 2):
            t = (x + y) / diag
            color = lerp(c1, c2, t)
            px[x, y] = color
            if x + 1 < w:
                px[x + 1, y] = color
    return img


def radial_glow(size, color, alpha=180):
    w, h = size
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    cx, cy = w / 2, h / 2
    maxr = math.hypot(cx, cy)
    px = img.load()
    for y in range(h):
        for x in range(0, w, 2):
            d = math.hypot(x - cx, y - cy) / maxr
            a = max(0, int(alpha * (1 - d) ** 2))
            px[x, y] = (*color, a)
            if x + 1 < w:
                px[x + 1, y] = (*color, a)
    return img


def draw_wordmark_glyph(size, scale=1.0):
    """An open-book + sparkle glyph rendered as transparent PNG."""
    w, h = size
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = w / 2, h / 2

    book_w = w * 0.46 * scale
    book_h = h * 0.30 * scale
    spine_x = cx
    top = cy - book_h * 0.15
    bottom = cy + book_h * 0.55

    left_pts = [
        (spine_x - book_w, top + book_h * 0.12),
        (spine_x - book_w * 0.06, top),
        (spine_x - book_w * 0.06, bottom),
        (spine_x - book_w, bottom + book_h * 0.12),
    ]
    right_pts = [
        (spine_x + book_w, top + book_h * 0.12),
        (spine_x + book_w * 0.06, top),
        (spine_x + book_w * 0.06, bottom),
        (spine_x + book_w, bottom + book_h * 0.12),
    ]
    d.polygon(left_pts, fill=(255, 255, 255, 235))
    d.polygon(right_pts, fill=(255, 255, 255, 235))

    line_gap = book_h * 0.16
    for i in range(3):
        ly = top + book_h * 0.32 + i * line_gap
        d.line([(spine_x - book_w * 0.75, ly), (spine_x - book_w * 0.18, ly)],
               fill=(90, 60, 180, 200), width=max(2, int(h * 0.012 * scale)))
        d.line([(spine_x + book_w * 0.18, ly), (spine_x + book_w * 0.75, ly)],
               fill=(90, 60, 180, 200), width=max(2, int(h * 0.012 * scale)))

    star_cx = cx + book_w * 0.62
    star_cy = cy - book_h * 0.95
    star_r = h * 0.09 * scale
    draw_star(d, (star_cx, star_cy), star_r, (255, 214, 102, 255))

    star2_r = h * 0.045 * scale
    draw_star(d, (cx - book_w * 0.95, cy - book_h * 0.55), star2_r, (255, 255, 255, 200))

    return img


def draw_star(d, center, r, color):
    cx, cy = center
    pts = []
    for i in range(4):
        ang = math.pi / 2 * i
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
        ang2 = ang + math.pi / 4
        pts.append((cx + r * 0.35 * math.cos(ang2), cy + r * 0.35 * math.sin(ang2)))
    d.polygon(pts, fill=color)


def save(img, path):
    img.save(path, "PNG")
    print("wrote", path, img.size)


def make_icon_layers():
    sizes = {
        "Back": [(400, 240), (800, 480), (1280, 768), (2560, 1536)],
        "Middle": [(400, 240), (800, 480), (1280, 768), (2560, 1536)],
        "Front": [(400, 240), (800, 480), (1280, 768), (2560, 1536)],
    }
    for layer, dims in sizes.items():
        for (w, h) in dims:
            if layer == "Back":
                img = diagonal_gradient((w, h), PURPLE, INDIGO)
            elif layer == "Middle":
                base = Image.new("RGBA", (w, h), (0, 0, 0, 0))
                glow = radial_glow((w, h), (255, 255, 255), alpha=90)
                base.alpha_composite(glow)
                img = base
            else:
                img = draw_wordmark_glyph((w, h), scale=1.0)
            fname = f"{layer.lower()}-{w}x{h}.png"
            save(img, f"{ROOT}/App Icon.imagestack/{layer}.imagestacklayer/Content.imageset/{fname}")


def make_top_shelf():
    combos = [
        ("Top Shelf Image", [(1920, 720), (3840, 1440)]),
        ("Top Shelf Image Wide", [(2320, 720), (4640, 1440)]),
    ]
    for name, dims in combos:
        for (w, h) in dims:
            img = diagonal_gradient((w, h), PURPLE, INDIGO).convert("RGBA")
            glow = radial_glow((w, h), (255, 255, 255), alpha=60)
            img.alpha_composite(glow)
            d = ImageDraw.Draw(img)

            glyph_h = int(h * 0.62)
            glyph = draw_wordmark_glyph((glyph_h, glyph_h), scale=1.15)
            gx = int(w * 0.08)
            gy = (h - glyph_h) // 2
            img.alpha_composite(glyph, (gx, gy))

            font_size = int(h * 0.20)
            try:
                font = ImageFont.truetype(FONT_ROUNDED, font_size)
            except Exception:
                font = ImageFont.load_default()
            text = "Word Enrich"
            tx = gx + glyph_h + int(w * 0.03)
            ty = h // 2 - font_size // 2 - int(h * 0.02)
            d.text((tx, ty), text, font=font, fill=(255, 255, 255, 255))

            sub_font_size = int(h * 0.085)
            try:
                sub_font = ImageFont.truetype(FONT_ROUNDED, sub_font_size)
            except Exception:
                sub_font = ImageFont.load_default()
            d.text((tx, ty + font_size + int(h * 0.02)), "Vocabulary Games",
                    font=sub_font, fill=(230, 230, 255, 220))

            img = img.convert("RGB")
            fname = f"{name.lower().replace(' ', '-')}-{w}x{h}.png"
            save(img, f"{ROOT}/{name}.imageset/{fname}")


def make_launch_and_accent():
    accent = "WordEnrichTV/Assets.xcassets/AccentColor.colorset"
    import os
    os.makedirs(accent, exist_ok=True)


if __name__ == "__main__":
    make_icon_layers()
    make_top_shelf()
    make_launch_and_accent()

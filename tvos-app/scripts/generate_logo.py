#!/usr/bin/env python3
"""Generates a redesigned layered App Icon + Top Shelf logo for the tvOS app.

Design: two fanned "letter tiles" (A / Z, evoking word-game tiles and
full vocabulary range) on the app's signature periwinkle -> indigo
gradient, with a small gold spark accent, and a soft glow layer for
tvOS parallax depth.
"""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = "WordEnrichTV/Assets.xcassets/AppIcon.brandassets"
FONT_BOLD_ROUNDED = "/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf"
FONT_ROUNDED = "/System/Library/Fonts/SFNSRounded.ttf"

PERIWINKLE = (102, 126, 234)   # #667eea
INDIGO = (76, 29, 149)
INK = (10, 8, 24)
WHITE = (255, 255, 255)
GOLD = (255, 214, 102)
TILE_TEXT = (58, 46, 122)      # deep indigo letter on white tile


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


def radial_glow(size, color, alpha=180, center=None):
    w, h = size
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    cx, cy = center if center else (w / 2, h / 2)
    maxr = math.hypot(max(cx, w - cx), max(cy, h - cy))
    px = img.load()
    for y in range(h):
        for x in range(0, w, 2):
            d = math.hypot(x - cx, y - cy) / maxr
            a = max(0, int(alpha * (1 - d) ** 2))
            px[x, y] = (*color, a)
            if x + 1 < w:
                px[x + 1, y] = (*color, a)
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


def make_tile(size, letter, corner_dot=True):
    """A single rounded-square letter tile, drawn on a transparent square
    canvas larger than the tile so it can be freely rotated without clipping."""
    canvas = int(size * 1.6)
    img = Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    off = (canvas - size) / 2
    rect = [off, off, off + size, off + size]
    radius = size * 0.16

    d.rounded_rectangle(rect, radius=radius, fill=(*WHITE, 255))

    font = ImageFont.truetype(FONT_BOLD_ROUNDED, int(size * 0.56))
    bbox = d.textbbox((0, 0), letter, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = off + (size - tw) / 2 - bbox[0]
    ty = off + (size - th) / 2 - bbox[1] - size * 0.03
    d.text((tx, ty), letter, font=font, fill=(*TILE_TEXT, 255))

    if corner_dot:
        dot_r = size * 0.045
        dot_cx = off + size * 0.82
        dot_cy = off + size * 0.82
        d.ellipse(
            [dot_cx - dot_r, dot_cy - dot_r, dot_cx + dot_r, dot_cy + dot_r],
            fill=(*GOLD, 255),
        )

    return img


def draw_tiles_glyph(size, scale=1.0):
    w, h = size
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    tile_size = h * 0.5 * scale

    # drop shadow pass first (both tiles), then the tiles themselves on top
    def place(letter, angle, dx, dy, shadow=False):
        tile = make_tile(tile_size, letter)
        tile = tile.rotate(angle, resample=Image.BICUBIC, expand=True)
        if shadow:
            alpha = tile.split()[3].point(lambda a: int(a * 0.35))
            shadow_img = Image.new("RGBA", tile.size, (0, 0, 0, 0))
            shadow_img.paste((0, 0, 0, 255), (0, 0), alpha)
            shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(radius=h * 0.015))
            px = int(w / 2 - tile.width / 2 + dx)
            py = int(h / 2 - tile.height / 2 + dy + h * 0.02)
            img.alpha_composite(shadow_img, (px, py))
        else:
            px = int(w / 2 - tile.width / 2 + dx)
            py = int(h / 2 - tile.height / 2 + dy)
            img.alpha_composite(tile, (px, py))

    back_dx, back_dy = -w * 0.155, 0.0
    front_dx, front_dy = w * 0.155, h * 0.02

    place("W", -6, back_dx, back_dy, shadow=True)
    place("E", 6, front_dx, front_dy, shadow=True)
    place("W", -6, back_dx, back_dy)
    place("E", 6, front_dx, front_dy)

    d = ImageDraw.Draw(img)
    star_cx = w * 0.80
    star_cy = h * 0.16
    draw_star(d, (star_cx, star_cy), h * 0.07 * scale, (*GOLD, 255))

    return img


def save(img, path):
    img.save(path, "PNG")
    print("wrote", path, img.size)


def make_icon_layers():
    dims = [(400, 240), (800, 480)]
    for (w, h) in dims:
        back = diagonal_gradient((w, h), PERIWINKLE, INDIGO)
        save(back, f"{ROOT}/App Icon.imagestack/Back.imagestacklayer/Content.imageset/back-{w}x{h}.png")

        middle = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        glow = radial_glow((w, h), WHITE, alpha=65, center=(w * 0.5, h * 0.4))
        middle.alpha_composite(glow)
        save(middle, f"{ROOT}/App Icon.imagestack/Middle.imagestacklayer/Content.imageset/middle-{w}x{h}.png")

        front = draw_tiles_glyph((w, h), scale=1.0)
        save(front, f"{ROOT}/App Icon.imagestack/Front.imagestacklayer/Content.imageset/front-{w}x{h}.png")


def make_app_store_icon_layers():
    w, h = 1280, 768
    store_root = f"{ROOT}/App Icon - App Store.imagestack"

    back = diagonal_gradient((w, h), PERIWINKLE, INDIGO)
    save(back, f"{store_root}/Back.imagestacklayer/Content.imageset/icon-store-back-{w}x{h}.png")

    middle = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    glow = radial_glow((w, h), WHITE, alpha=65, center=(w * 0.5, h * 0.4))
    middle.alpha_composite(glow)
    save(middle, f"{store_root}/Middle.imagestacklayer/Content.imageset/icon-store-middle-{w}x{h}.png")

    front = draw_tiles_glyph((w, h), scale=1.0)
    save(front, f"{store_root}/Front.imagestacklayer/Content.imageset/icon-store-front-{w}x{h}.png")


def make_top_shelf():
    combos = [
        ("Top Shelf Image", [(1920, 720), (3840, 1440)]),
        ("Top Shelf Image Wide", [(2320, 720), (4640, 1440)]),
    ]
    for name, dims in combos:
        for (w, h) in dims:
            img = diagonal_gradient((w, h), PERIWINKLE, INDIGO).convert("RGBA")
            glow = radial_glow((w, h), WHITE, alpha=50, center=(w * 0.16, h * 0.5))
            img.alpha_composite(glow)
            d = ImageDraw.Draw(img)

            glyph_h = int(h * 0.7)
            glyph_w = int(glyph_h * (800 / 480))
            glyph = draw_tiles_glyph((glyph_w, glyph_h), scale=1.0)
            gx = int(w * 0.05)
            gy = (h - glyph_h) // 2
            img.alpha_composite(glyph, (gx, gy))

            font_size = int(h * 0.195)
            font = ImageFont.truetype(FONT_ROUNDED, font_size)
            text = "Word Enrich"
            tx = gx + glyph_w + int(w * 0.02)
            ty = h // 2 - font_size // 2 - int(h * 0.03)
            d.text((tx, ty), text, font=font, fill=(255, 255, 255, 255))

            sub_font_size = int(h * 0.085)
            sub_font = ImageFont.truetype(FONT_ROUNDED, sub_font_size)
            d.text((tx, ty + font_size + int(h * 0.02)), "Vocabulary Games",
                    font=sub_font, fill=(230, 230, 255, 210))

            img = img.convert("RGB")
            fname = f"{name.lower().replace(' ', '-')}-{w}x{h}.png"
            save(img, f"{ROOT}/{name}.imageset/{fname}")


if __name__ == "__main__":
    make_icon_layers()
    make_app_store_icon_layers()
    make_top_shelf()

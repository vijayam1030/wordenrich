#!/usr/bin/env python3
"""Writes Contents.json for the tvOS brand-assets catalog structure."""
import json, os

ROOT = "WordEnrichTV/Assets.xcassets"
BRAND = f"{ROOT}/AppIcon.brandassets"


def write(path, obj):
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)
    print("wrote", path)


def image_layer_contents(dirpath, prefix, w, h):
    write(f"{dirpath}/Contents.json", {
        "images": [
            {"idiom": "tv", "filename": f"{prefix}-{w}x{h}.png", "scale": "1x"},
            {"idiom": "tv", "filename": f"{prefix}-{w*2}x{h*2}.png", "scale": "2x"},
        ],
        "info": {"version": 1, "author": "xcode"}
    })


def main():
    os.makedirs(ROOT, exist_ok=True)

    write(f"{ROOT}/Contents.json", {
        "info": {"version": 1, "author": "xcode"}
    })

    os.makedirs(BRAND, exist_ok=True)
    write(f"{BRAND}/Contents.json", {
        "assets": [
            {"filename": "App Icon.imagestack", "role": "primary-app-icon", "size": "400x240"},
            {"filename": "Top Shelf Image.imageset", "role": "top-shelf-image", "size": "1920x720"},
            {"filename": "Top Shelf Image Wide.imageset", "role": "top-shelf-image-wide", "size": "2320x720"},
        ],
        "info": {"version": 1, "author": "xcode"},
        "properties": {"provides-namespace": True}
    })

    imagestack = f"{BRAND}/App Icon.imagestack"
    write(f"{imagestack}/Contents.json", {
        "layers": [
            {"filename": "Front.imagestacklayer"},
            {"filename": "Middle.imagestacklayer"},
            {"filename": "Back.imagestacklayer"},
        ],
        "info": {"version": 1, "author": "xcode"}
    })

    for layer, prefix in [("Front", "front"), ("Middle", "middle"), ("Back", "back")]:
        layerdir = f"{imagestack}/{layer}.imagestacklayer"
        write(f"{layerdir}/Contents.json", {
            "info": {"version": 1, "author": "xcode"}
        })
        image_layer_contents(f"{layerdir}/Content.imageset", prefix, 400, 240)

    ts = f"{BRAND}/Top Shelf Image.imageset"
    image_layer_contents(ts, "top-shelf-image", 1920, 720)

    tsw = f"{BRAND}/Top Shelf Image Wide.imageset"
    image_layer_contents(tsw, "top-shelf-image-wide", 2320, 720)

    accent = f"{ROOT}/AccentColor.colorset"
    os.makedirs(accent, exist_ok=True)
    write(f"{accent}/Contents.json", {
        "colors": [
            {
                "idiom": "universal",
                "color": {
                    "color-space": "srgb",
                    "components": {"red": "0.400", "green": "0.494", "blue": "0.918", "alpha": "1.000"}
                }
            }
        ],
        "info": {"version": 1, "author": "xcode"}
    })


if __name__ == "__main__":
    main()

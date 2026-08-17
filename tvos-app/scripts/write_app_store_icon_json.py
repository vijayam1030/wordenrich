#!/usr/bin/env python3
"""Writes Contents.json for the App Icon - App Store.imagestack (1280x768,
required for App Store submission in addition to the 400x240 Home Screen icon)."""
import json

ROOT = "WordEnrichTV/Assets.xcassets/AppIcon.brandassets"
STORE = f"{ROOT}/App Icon - App Store.imagestack"


def write(path, obj):
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)
    print("wrote", path)


def main():
    write(f"{STORE}/Contents.json", {
        "layers": [
            {"filename": "Front.imagestacklayer"},
            {"filename": "Middle.imagestacklayer"},
            {"filename": "Back.imagestacklayer"},
        ],
        "info": {"version": 1, "author": "xcode"}
    })

    for layer, prefix in [("Front", "front"), ("Middle", "middle"), ("Back", "back")]:
        layerdir = f"{STORE}/{layer}.imagestacklayer"
        write(f"{layerdir}/Contents.json", {
            "info": {"version": 1, "author": "xcode"}
        })
        write(f"{layerdir}/Content.imageset/Contents.json", {
            "images": [
                {"idiom": "tv", "filename": f"icon-store-{prefix}-1280x768.png", "scale": "1x"},
            ],
            "info": {"version": 1, "author": "xcode"}
        })


if __name__ == "__main__":
    main()

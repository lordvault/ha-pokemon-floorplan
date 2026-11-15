#!/usr/bin/env python3
"""
Generate Home Assistant floorplan assets in www/ from references/drafts/mapita_rendered.png:
- floorplan_day.png
- floorplan_night.png
- light_*.png (per-room lighting overlays with wall-boundary clipping)
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

ROOT_DIR = Path(__file__).resolve().parent.parent
RENDERED_PATH = ROOT_DIR / "references" / "drafts" / "mapita_rendered.png"
OUT_DIR = ROOT_DIR / "www"


def main():
    base = Image.open(RENDERED_PATH).convert("RGBA")
    w, h = base.size
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Daytime Base Map
    base.save(OUT_DIR / "floorplan_day.png")

    # 2. Nighttime Base Map (when lights are OFF)
    night = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    px_b = base.load()
    px_n = night.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = px_b[x, y]
            if r == 152 and g == 208 and b == 248:
                px_n[x, y] = (18, 24, 48, 255)
            else:
                nr = int(r * 0.34)
                ng = int(g * 0.37)
                nb = min(255, int(b * 0.52) + 12)
                px_n[x, y] = (nr, ng, nb, a)

    night.save(OUT_DIR / "floorplan_night.png")

    # 3. Warm-lit full map used to cut out room light overlays
    lit_full = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    px_l = lit_full.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = px_b[x, y]
            if r == 152 and g == 208 and b == 248:
                px_l[x, y] = (18, 24, 48, 255)
            else:
                nr = min(255, int(r * 1.06 + 10))
                ng = min(255, int(g * 1.01 + 4))
                nb = max(0, int(b * 0.90))
                px_l[x, y] = (nr, ng, nb, a)

    def make_room_light_overlay(name, rects, feather=8, exclude_rects=None):
        mask = Image.new("L", (w, h), 0)
        draw = ImageDraw.Draw(mask)
        for (c0, r0, c1, r1) in rects:
            draw.rectangle([int(c0 * 32), int(r0 * 32), int(c1 * 32), int(r1 * 32)], fill=255)
        mask_blur = mask.filter(ImageFilter.GaussianBlur(radius=feather))
        if exclude_rects:
            ex_draw = ImageDraw.Draw(mask_blur)
            for (ec0, er0, ec1, er1) in exclude_rects:
                ex_draw.rectangle([int(ec0 * 32), int(er0 * 32), int(ec1 * 32), int(er1 * 32)], fill=0)
            mask_blur = mask_blur.filter(ImageFilter.GaussianBlur(radius=2))
            ex_draw = ImageDraw.Draw(mask_blur)
            for (ec0, er0, ec1, er1) in exclude_rects:
                ex_draw.rectangle([int(ec0 * 32), int(er0 * 32), int(ec1 * 32), int(er1 * 32)], fill=0)
        overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        overlay.paste(lit_full, (0, 0), mask=mask_blur)
        out_file = OUT_DIR / f"light_{name}.png"
        overlay.save(out_file)
        print(f"Saved {out_file}")

    make_room_light_overlay("kitchen_1", [(9.8, 1.0, 14.0, 5.8)], feather=10)
    make_room_light_overlay(
        "kitchen_2",
        [(9.8, 5.5, 14.0, 11.0)],
        feather=10,
        exclude_rects=[(0, 11.0, 14.0, 22.0)],
    )
    make_room_light_overlay(
        "living_1",
        [(14.0, 4.0, 19.2, 9.2)],
        feather=10,
        exclude_rects=[(16.8, 9.2, 22.0, 22.0)],
    )
    make_room_light_overlay(
        "living_2",
        [
            (13.8, 8.2, 16.9, 11.4),
            (9.5, 9.5, 14.8, 10.9),
            (13.9, 10.9, 14.9, 15.8),
        ],
        feather=8,
        exclude_rects=[
            (16.9, 9.2, 22.0, 22.0),
            (15.0, 11.5, 22.0, 22.0),
            (8.5, 11.0, 13.9, 16.2),
        ],
    )
    make_room_light_overlay(
        "study",
        [
            (15.0, 11.8, 19.2, 18.2),
            (17.0, 9.6, 19.2, 12.0),
        ],
        feather=8,
        exclude_rects=[
            (13.5, 8.0, 17.0, 11.6),
            (0.0, 0.0, 14.9, 22.0),
        ],
    )
    make_room_light_overlay(
        "bedroom",
        [(9.0, 15.8, 14.9, 20.0)],
        feather=10,
        exclude_rects=[
            (8.5, 11.0, 14.0, 15.6),
            (15.0, 11.0, 22.0, 22.0),
        ],
    )
    make_room_light_overlay(
        "wardrobe",
        [(5.0, 16.2, 8.2, 20.0)],
        feather=8,
        exclude_rects=[(4.5, 11.0, 8.5, 16.0)],
    )
    make_room_light_overlay("bathroom_guest", [(9.0, 11.2, 13.8, 15.6)], feather=8)
    make_room_light_overlay("bathroom_master", [(5.0, 11.2, 8.2, 16.0)], feather=8)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Render mapita_pokemon.tmx into a composite RGBA PNG image (references/drafts/mapita_rendered.png).
Supports Tiled layer visibility, layer opacity, and horizontal/vertical/diagonal tile flip flags.
"""

from pathlib import Path
import xml.etree.ElementTree as ET
from PIL import Image

ROOT_DIR = Path(__file__).resolve().parent.parent
TMX_PATH = ROOT_DIR / "mapita_pokemon.tmx"
OUT_PATH = ROOT_DIR / "references" / "drafts" / "mapita_rendered.png"


def main():
    tree = ET.parse(TMX_PATH)
    root = tree.getroot()
    w = int(root.attrib["width"])
    h = int(root.attrib["height"])
    tw = int(root.attrib["tilewidth"])
    th = int(root.attrib["tileheight"])

    tilesets = []
    for ts_elem in root.findall("tileset"):
        firstgid = int(ts_elem.attrib["firstgid"])
        src = ts_elem.attrib["source"]
        ts_path = ROOT_DIR / src
        ts_tree = ET.parse(ts_path)
        img_src = ts_tree.getroot().find("image").attrib["source"]
        img_path = ts_path.parent / img_src
        img = Image.open(img_path).convert("RGBA")
        cols = img.width // tw
        tilesets.append((firstgid, cols, img))

    tilesets.sort(key=lambda x: x[0])

    def get_gid_tile(gid):
        FLIP_H = 0x80000000
        FLIP_V = 0x40000000
        FLIP_D = 0x20000000
        fh = bool(gid & FLIP_H)
        fv = bool(gid & FLIP_V)
        fd = bool(gid & FLIP_D)
        raw_gid = gid & ~(FLIP_H | FLIP_V | FLIP_D)
        if raw_gid == 0:
            return None
        chosen = None
        for fg, cols, img in tilesets:
            if raw_gid >= fg:
                chosen = (fg, cols, img)
            else:
                break
        if not chosen:
            return None
        fg, cols, img = chosen
        local_id = raw_gid - fg
        r = local_id // cols
        c = local_id % cols
        tile = img.crop((c * tw, r * th, (c + 1) * tw, (r + 1) * th))
        if fd:
            tile = tile.transpose(Image.TRANSPOSE)
        if fh:
            tile = tile.transpose(Image.FLIP_LEFT_RIGHT)
        if fv:
            tile = tile.transpose(Image.FLIP_TOP_BOTTOM)
        return tile

    canvas = Image.new("RGBA", (w * tw, h * th), (0, 0, 0, 255))

    for layer in root.findall("layer"):
        if layer.attrib.get("visible", "1") == "0":
            continue
        opacity = float(layer.attrib.get("opacity", "1.0"))
        data_text = layer.find("data").text.strip()
        gids = [int(x) for x in data_text.replace("\n", ",").split(",") if x.strip() != ""]
        layer_img = Image.new("RGBA", (w * tw, h * th), (0, 0, 0, 0))
        for idx, gid in enumerate(gids):
            if gid == 0:
                continue
            t = get_gid_tile(gid)
            if t:
                r = idx // w
                c = idx % w
                layer_img.alpha_composite(t, (c * tw, r * th))
        if opacity < 1.0:
            r_ch, g_ch, b_ch, a_ch = layer_img.split()
            a_ch = a_ch.point(lambda p: int(p * opacity))
            layer_img = Image.merge("RGBA", (r_ch, g_ch, b_ch, a_ch))
        canvas.alpha_composite(layer_img)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUT_PATH)
    print(f"Rendered {OUT_PATH} ({canvas.size[0]}x{canvas.size[1]})")


if __name__ == "__main__":
    main()

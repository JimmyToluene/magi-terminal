#!/usr/bin/env python3
"""
make-nerv-screens.py — render the NERV console screens from scratch.

Usage:
    python3 tools/make-nerv-screens.py -o images/

These are clean-room recreations, not screencaps. Every pixel is drawn here
from the palette in magi.sh and set in the PC-9800 font this repository
builds, so they ship as original assets and double as a demonstration of what
the NERV Console palette does with a real layout.

The canvas is 640x400 — the native resolution of the NEC PC-9801, the machine
NERV's displays were modeled on — then scaled by an integer factor with
nearest-neighbour so the 8x16 cell stays sharp.

Requires the font from the README's font section, installed or on --font:
    ~/.local/share/fonts/pc-9800-regular.ttf
"""

import argparse
import os
import sys

from PIL import Image, ImageDraw, ImageFont

# NERV Console palette — see magi.sh
BG        = "#000000"   # title-card black
FG        = "#FF9900"   # console body text
RED       = "#E81900"   # 警告 alert red
GREEN     = "#41BB42"   # Unit-01 stripes; the hexagonal screen grid
YELLOW    = "#F6E201"   # official EVA yellow
BLUE      = "#54A2D4"   # Pattern Blue — Angel confirmed
BR_BLUE   = "#7FC8F0"   # Pattern Blue at peak
BR_RED    = "#FF2D0E"   # the alert flashing
BR_YELLOW = "#F9CC38"   # caution striping
CHROME    = "#856640"   # inactive frame lines
WHITE     = "#FFFFFF"   # Matisse EB title-card white
GRID      = "#0E2A0E"   # the hex grid, backed off to sit under text

W, H = 640, 400

FONT_CANDIDATES = [
    os.path.expanduser("~/.local/share/fonts/pc-9800-regular.ttf"),
    os.path.expanduser("~/.fonts/pc-9800-regular.ttf"),
    "/usr/local/share/fonts/pc-9800-regular.ttf",
    "dist/pc-9800-regular.ttf",
]


def load_font(path, size):
    return ImageFont.truetype(path, size)


def hex_grid(d, color=GRID, r=22):
    """The repeating hexagonal grid on NERV's screen ground."""
    import math
    pts = [(math.cos(math.radians(60 * i)) * r,
            math.sin(math.radians(60 * i)) * r) for i in range(6)]
    dx = r * 1.5
    dy = r * math.sqrt(3)
    col = 0
    x = -r
    while x < W + r * 2:
        y = -r if col % 2 == 0 else -r + dy / 2
        while y < H + r * 2:
            d.polygon([(x + px, y + py) for px, py in pts], outline=color)
            y += dy
        x += dx
        col += 1


def frame(d, box, color=CHROME, tick=10):
    """Bracketed corner frame — NERV never draws a plain rectangle."""
    x0, y0, x1, y1 = box
    for (cx, cy, sx, sy) in ((x0, y0, 1, 1), (x1, y0, -1, 1),
                             (x0, y1, 1, -1), (x1, y1, -1, -1)):
        d.line([(cx, cy), (cx + tick * sx, cy)], fill=color)
        d.line([(cx, cy), (cx, cy + tick * sy)], fill=color)


def text(d, xy, s, font, fill, anchor="la"):
    d.text(xy, s, font=font, fill=fill, anchor=anchor)


# ---------------------------------------------------------------- screens

def screen_magi(fp):
    """The three-system verdict display. Two approve, one dissents."""
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    hex_grid(d)

    f10 = load_font(fp, 16)
    f16 = load_font(fp, 16)
    f32 = load_font(fp, 32)

    text(d, (16, 14), "MAGI", f32, FG)
    text(d, (108, 26), "SYSTEM", f16, CHROME)
    text(d, (W - 16, 20), "決議", f16, FG, anchor="ra")
    d.line([(16, 56), (W - 16, 56)], fill=CHROME)

    # Canon layout: BALTHASAR and CASPER below, MELCHIOR at the apex.
    units = [
        ("MELCHIOR", "1", "可決", GREEN,  (232, 78)),
        ("BALTHASAR", "2", "可決", GREEN, (74, 216)),
        ("CASPER", "3", "否決", RED,      (390, 216)),
    ]
    for name, num, verdict, col, (bx, by) in units:
        box = (bx, by, bx + 176, by + 104)
        d.rectangle(box, outline=col)
        frame(d, (bx - 5, by - 5, bx + 181, by + 109), color=CHROME, tick=8)
        text(d, (bx + 88, by + 12), f"{name}・{num}", f16, col, anchor="ma")
        text(d, (bx + 88, by + 52), verdict, f32, col, anchor="ma")

    d.line([(320, 182), (162, 216)], fill=CHROME)
    d.line([(320, 182), (478, 216)], fill=CHROME)

    text(d, (16, H - 30), "審議終了", f16, FG)
    text(d, (W - 16, H - 30), "2 / 3  可決", f16, YELLOW, anchor="ra")
    return im


def screen_pattern_blue(fp):
    """Sensor readout at the moment a target is classified as an Angel."""
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    hex_grid(d)

    f16 = load_font(fp, 16)
    f32 = load_font(fp, 32)

    text(d, (16, 14), "解析", f16, CHROME)
    text(d, (16, 40), "パターン青", f32, BR_BLUE)
    text(d, (W - 16, 46), "使徒 確認", f16, BR_BLUE, anchor="ra")
    d.line([(16, 84), (W - 16, 84)], fill=BLUE)

    # Waveform: the readout is the only blue thing on a NERV screen that means
    # something. Bars are deterministic so the image is reproducible.
    bx, by, bw, bh = 16, 108, W - 32, 132
    frame(d, (bx, by, bx + bw, by + bh), color=CHROME)
    seed = [3, 7, 12, 26, 41, 63, 88, 104, 121, 108, 93, 71, 55, 78, 96, 118,
            127, 112, 84, 61, 44, 52, 68, 81, 66, 49, 33, 22, 14, 8, 5, 2]
    step = bw // len(seed)
    for i, v in enumerate(seed):
        x = bx + 4 + i * step
        h = int(v / 127 * (bh - 16))
        d.rectangle([x, by + bh - 8 - h, x + step - 3, by + bh - 8],
                    fill=BLUE if v < 100 else BR_BLUE)
    d.line([(bx, by + bh - 8), (bx + bw, by + bh - 8)], fill=CHROME)

    rows = [
        ("目標", "第五使徒", FG),
        ("パターン", "青", BR_BLUE),
        ("信頼度", "99.8%", FG),
        ("A.T.フィールド", "展開中", YELLOW),
    ]
    y = 262
    for k, v, col in rows:
        text(d, (16, y), k, f16, CHROME)
        text(d, (240, y), v, f16, col)
        y += 26

    text(d, (W - 16, H - 30), "NERV", f16, FG, anchor="ra")
    return im


def screen_alert(fp):
    """緊急事態 — the emergency card, caution striping and all."""
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)

    f16 = load_font(fp, 16)
    f32 = load_font(fp, 32)

    def stripes(y0, y1):
        for x in range(-H, W + H, 32):
            d.polygon([(x, y1), (x + 16, y1), (x + 16 + (y1 - y0), y0),
                       (x + (y1 - y0), y0)], fill=BR_YELLOW)

    stripes(0, 28)
    stripes(H - 28, H)

    text(d, (W // 2, 96), "緊急事態", f32, BR_RED, anchor="ma")
    d.line([(120, 148), (W - 120, 148)], fill=RED)
    text(d, (W // 2, 168), "第三新東京市", f16, FG, anchor="ma")
    text(d, (W // 2, 196), "特別非常事態宣言", f16, WHITE, anchor="ma")

    box = (120, 232, W - 120, 300)
    frame(d, box, color=RED, tick=12)
    text(d, (W // 2, 248), "全員退避", f16, RED, anchor="ma")
    text(d, (W // 2, 274), "シェルターへ", f16, FG, anchor="ma")
    return im


SCREENS = {
    "nerv-magi": screen_magi,
    "nerv-pattern-blue": screen_pattern_blue,
    "nerv-alert": screen_alert,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--outdir", default="images")
    ap.add_argument("--font", default=None, help="path to pc-9800-regular.ttf")
    ap.add_argument("--scale", type=int, default=2,
                    help="integer upscale, nearest-neighbour (default: 2)")
    ap.add_argument("--only", choices=sorted(SCREENS), help="render one screen")
    args = ap.parse_args()

    fp = args.font
    if not fp:
        fp = next((p for p in FONT_CANDIDATES if os.path.exists(p)), None)
    if not fp or not os.path.exists(fp):
        sys.exit("pc-9800-regular.ttf not found — build it (see README) or pass --font")

    os.makedirs(args.outdir, exist_ok=True)
    todo = [args.only] if args.only else sorted(SCREENS)
    for name in todo:
        im = SCREENS[name](fp)
        if args.scale > 1:
            im = im.resize((W * args.scale, H * args.scale), Image.NEAREST)
        out = os.path.join(args.outdir, f"{name}.png")
        im.save(out)
        print(f"wrote {out} {im.size}")


if __name__ == "__main__":
    main()

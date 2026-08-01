#!/usr/bin/env python3
#
# MAGI Terminal, Copyright (C) 2026 JimmyToluene
# Licensed under the GNU General Public License v3.0. See LICENSE.
"""
make-cover.py: stack two terminal screenshots into the README cover.

Usage:
    python3 tools/make-cover.py images/shot-nvidia.png images/shot-htop.png \
        -o images/cover.png

Normalizes both shots to the same width by scaling the wider one down, which
keeps every pixel sharp, then stacks them vertically with a thin amber rule
between and pads with title-card black.
"""

import argparse

from PIL import Image

RULE = "#3A2A14"   # bright-black from the palette
BG = "#000000"     # title-card black
GAP = 3
PAD = 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("top")
    ap.add_argument("bottom")
    ap.add_argument("-o", "--output", default="images/cover.png")
    ap.add_argument("--max-width", type=int, default=0,
                    help="cap output width (default: narrower of the two inputs)")
    args = ap.parse_args()

    a = Image.open(args.top).convert("RGB")
    b = Image.open(args.bottom).convert("RGB")

    w = args.max_width or min(a.width, b.width)
    def fit(im):
        if im.width == w:
            return im
        return im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)

    a, b = fit(a), fit(b)
    H = a.height + GAP + b.height + PAD * 2
    cov = Image.new("RGB", (w + PAD * 2, H), BG)
    cov.paste(a, (PAD, PAD))
    cov.paste(Image.new("RGB", (w, GAP), RULE), (PAD, PAD + a.height))
    cov.paste(b, (PAD, PAD + a.height + GAP))
    cov.save(args.output)
    print(f"wrote {args.output} {cov.size}")


if __name__ == "__main__":
    main()

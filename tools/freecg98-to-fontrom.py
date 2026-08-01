#!/usr/bin/env python3
#
# MAGI Terminal — Copyright (C) 2026 JimmyToluene
# Licensed under the GNU General Public License v3.0. See LICENSE.
"""
freecg98-to-fontrom.py — synthesize a PC-9800 FONT.ROM from FREECG98.BMP.

hikaen2/ttf-pc9800 builds a TrueType font from a NEC PC-9801 FONT.ROM dump.
The FONT.ROM shipped in that repository is a placeholder: 288,768 bytes of
0xFF. It is the correct size, so `make` runs to completion — and every glyph
in the resulting font is a solid block.

Rather than source NEC's copyrighted firmware, this reads FREECG98.BMP, the
free clean-room Anex86-compatible PC-98 font distributed with DOSBox-X, and
writes a FONT.ROM in the byte layout that ttf-pc9800's parser expects.

Layout produced (matches bin/fontrom2bdf):

    0x0000..0x07FF   header, unused by the parser
    0x0800 + n*16    256 single-byte ANK glyphs, 8x16, one byte per row
    then             8832 double-byte glyphs, 32 bytes each

Only the ANK range is filled. The parser skips all-zero glyphs, and kanji
coverage comes from the Shinonome 16 BDF that ttf-pc9800 already bundles.

Usage:
    python3 freecg98-to-fontrom.py FREECG98.BMP > FONT.ROM
    # or
    python3 freecg98-to-fontrom.py FREECG98.BMP -o path/to/data/FONT.ROM

FREECG98.BMP source:
    https://github.com/joncampbell123/dosbox-x/raw/master/contrib/fonts/FREECG98.BMP
"""

import argparse
import sys

from PIL import Image

HEADER = 0x800
ANK_COUNT, ANK_BYTES = 256, 16
DBCS_COUNT, DBCS_BYTES = 8832, 32
ROM_SIZE = HEADER + ANK_COUNT * ANK_BYTES + DBCS_COUNT * DBCS_BYTES  # 288768

INK = 0  # a black pixel is ink; the sheet is black-on-white


def build(bmp_path):
    im = Image.open(bmp_path).convert("L")
    if im.size != (2048, 2048):
        print(f"warning: expected a 2048x2048 sheet, got {im.size}", file=sys.stderr)
    px = im.load()

    # The SBCS 8x16 font occupies the top row of the sheet: byte value `code`
    # lives at x = code*8, y = 0..15. 256 codes * 8px spans the full width.
    rom = bytearray(ROM_SIZE)
    for code in range(ANK_COUNT):
        for row in range(16):
            bits = 0
            for bit in range(8):
                if px[code * 8 + bit, row] == INK:
                    bits |= 0x80 >> bit
            rom[HEADER + code * ANK_BYTES + row] = bits
    return bytes(rom)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("bmp", help="path to FREECG98.BMP")
    ap.add_argument("-o", "--output", help="output path (default: stdout)")
    args = ap.parse_args()

    rom = build(args.bmp)
    if args.output:
        with open(args.output, "wb") as fh:
            fh.write(rom)
        print(f"wrote {args.output} ({len(rom)} bytes)", file=sys.stderr)
    else:
        sys.stdout.buffer.write(rom)


if __name__ == "__main__":
    main()

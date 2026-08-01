<div align="center">

# MAGI Terminal

**English** · [简体中文](README.zh-CN.md) · [日本語](README.ja.md)

**An amber-on-black terminal palette derived from the NERV console screens in *Neon Genesis Evangelion* — plus a clean-room build of the PC-98 font those screens were drawn from.**

![MAGI Monochrome and NERV Console shell sessions side by side](images/cover.png)

</div>

---

## What this is

Two terminal palettes and a font toolchain.

The palettes are not "orange theme, vaguely anime." Every value traces to something on screen or to one of the four official series colors, and every slot was contrast-tested rather than eyeballed. The font is the actual NEC PC-9801 ROM face that Anno's team modeled NERV's displays on, built from a free clean-room source so no copyrighted firmware is involved.

Applied by escape sequence from the machine you SSH *into*, so the look follows the workstation rather than living in one client's settings.

## The palettes

### MAGI Monochrome — the default

The amber-on-black MAGI text screens. All sixteen ANSI slots are stops on a single ramp interpolated between the two official series colors: NERV orange `#F66E25` and EVA yellow `#F6E201`. Nothing is not-amber.

![MAGI Monochrome palette](images/palette-magi.png)

### NERV Console

Amber still carries the screen, but hue survives where *Evangelion* assigns it meaning. Use this one if you read `git diff` or `pytest` output all day — red-versus-green is the most load-bearing color pair in development work, and monochrome flattens it.

![NERV Console palette](images/palette-nerv.png)

## Install

```bash
git clone https://github.com/JimmyToluene/magi-terminal.git ~/magi-terminal
cp ~/magi-terminal/magi.sh ~/.config/magi.sh
```

Then append to `~/.zshrc` (or `~/.bashrc`) **on the machine you SSH into**:

```bash
if [[ -o interactive && -t 1 && $TERM != dumb && $TERM != linux ]]; then
  source ~/.config/magi.sh
fi
```

The guards matter. Without the `-t 1` test the escape sequences get emitted into non-TTY streams and corrupt `scp`, `rsync`, and `git` over SSH.

```bash
source ~/.config/magi.sh                # MAGI Monochrome (default)
EVA_ACCENT=1 source ~/.config/magi.sh   # NERV Console
```

Or enter the hex values by hand in your terminal's own theme editor — see [What the server can and cannot control](#what-the-server-can-and-cannot-control).

## Why these colors

There is no official hex spec for NERV's screens. They are cel and early digital animation, not a brand system. Three things *are* authoritative, and everything here is built from them:

- **The four official series colors**, unchanged since 1995 — orange `#F66E25`, yellow `#F6E201`, black, white.
- **The licensed Gaia Notes EVA paint line** (EV-01 Eva Purple, EV-02 Eva Green, EV-06 Eva Red, EV-11 Eva Proto Yellow), which fixes which color belongs to which unit.
- **Canon color semantics**, which matter most: **Pattern Blue means a target is confirmed as an Angel; Pattern Orange means the MAGI cannot classify it.** NERV's screen ground is black with a repeating *green* hexagonal grid.

That last point drives the whole design. In *Evangelion*, screen color is information, not decoration. So in NERV Console each slot earns its hue:

| Slot | Hex | On screen |
|---|---|---|
| Background | `#000000` | Title-card black — pure, never near-black |
| Foreground | `#FF9900` | NERV console body text |
| Cursor | `#F66E25` | Official NERV logo orange |
| Red | `#E81900` | 警告 alert red; Unit-02 |
| Green | `#41BB42` | Unit-01's stripes; the hexagonal screen grid |
| Yellow | `#F6E201` | Official EVA yellow; Unit-00 proto |
| Blue | `#54A2D4` | **Pattern Blue** — Angel confirmed |
| Magenta | `#9B78C4` | Unit-01 armor purple |
| Bright White | `#FFFFFF` | Matisse EB title-card white — the only pure white |

The background is `#000000` and not a softened near-black. The title cards and MAGI screens are pure black, and the whole look collapses without it.

## Legibility

Brightness is assigned by **terminal role**, not by how often a color appears in the series.

This is worth stating because getting it backwards produces a beautiful palette you cannot read. Blue is rare in *Evangelion*, which argues for making slot 4 dim — but slot 4 is what `ls` uses for directories (`DIR=01;34`), the most-read colored text on a working screen. An early version of this palette put slot 4 at **2.8:1** against black. Unusable.

Every slot is now measured. In MAGI Monochrome, only Black and Bright Black are permitted to recede:

| | Contrast vs `#000000` |
|---|---|
| Directories (slot 4) | **8.9:1** |
| Lowest non-recessive slot | 5.9:1 |
| Highest | 19:1 |
| Bright Black (chrome, comments) | 4.0:1 — recessive by design |

Check any palette yourself with the WCAG relative-luminance formula; anything under 4.5:1 against the background should be a deliberate choice.

## The PC-9800 font

The `Jet Alone` boot screen in Episode 07 is not generic DOS set dressing. It is modeled on the **NEC PC-9800 series**, Japan's dominant PC platform of the era — the opening lines match a real PC-9801 BIOS memory test, and the `addr PSP blks size` table is output from `VMAP.COM`, an obscure Japanese memory diagnostic. The letterforms are the PC-9801's built-in 8×16 ANK bitmap font, burned into ROM. Its slab serifs are why the screen never reads as a Western DOS box; IBM's VGA CP437 font is essentially sans.

[`hikaen2/ttf-pc9800`](https://github.com/hikaen2/ttf-pc9800) converts a PC-9801 `FONT.ROM` dump into TrueType. **The `FONT.ROM` bundled in that repository is a placeholder** — 288,768 bytes of nothing but `0xFF`. It is exactly the right size, so `make` runs to completion and produces a font in which every glyph is a solid filled block.

`tools/freecg98-to-fontrom.py` removes the need for NEC's firmware entirely. It reads `FREECG98.BMP` — the free clean-room Anex86-compatible PC-98 font distributed with DOSBox-X — and writes a `FONT.ROM` in the byte layout ttf-pc9800's parser expects:

```bash
sudo apt install -y git make ruby fontforge-nox potrace bdfresize
git clone https://github.com/hikaen2/ttf-pc9800.git && cd ttf-pc9800
curl -sLO https://github.com/joncampbell123/dosbox-x/raw/master/contrib/fonts/FREECG98.BMP
python3 ../tools/freecg98-to-fontrom.py FREECG98.BMP -o data/FONT.ROM
make
```

Output lands in `dist/` as `pc-9800-regular.ttf` and `pc-9800-bold.ttf`.

The Jet Alone boot screen, rebuilt in the resulting font at 32px and 16px:

![Boot screen at 32px](images/boot-32px.png)

![Boot screen at 16px](images/boot-16px.png)

Two notes:

- **Set `post.isFixedPitch = 1`** on the output. All Latin advances are a uniform 512 and PANOSE already reports monospaced, but FontForge leaves that flag clear, and it is what most applications check when filtering their font menu to monospace fonts. Without it, the font may not appear at all.
- `FREECG98.BMP` is a **recreation**, not NEC's ROM. It carries the PC-98 character and the correct 8×16 metrics, but glyph shapes are close rather than identical. Drop in a real dump from hardware and rerun `make` if you need exactness.

The font renders sharpest at exact multiples of its 16px cell. If it looks soft, try 16 / 32 rather than adjusting by one.

## What the server can and cannot control

Terminal appearance is negotiated between two machines, and clients honor wildly different subsets of it. In practice there are three tiers:

| | ANSI colors (`OSC 4`) | Background (`OSC 11`) | Font |
|---|---|---|---|
| xterm, kitty, Alacritty, iTerm2, GNOME Terminal, Windows Terminal | ✅ automatic | ✅ automatic | client-side |
| Termius | ✅ automatic | ❌ set in theme editor (syncs across devices) | client-side |
| MobaXterm (PuTTY-derived) | ❌ | ❌ | client-side |

**The font is always client-side.** The server sends bytes; the client renders glyphs. No escape sequence changes that — install the TTF on every device.

For clients that ignore `OSC 4` entirely, paste the hex values into their own color settings. Confirm which tier a client is in:

```bash
printf '\033]4;1;#00FF00\007'; printf '\033[31mIf this text is GREEN, OSC 4 works\033[0m\n'
```

## Credits

- [EvaGeeks — Jet Alone's boot screen](https://wiki.evageeks.org/FGC:Supplemental_Jet_Alone's_boot_screen) — identification of the PC-9800 basis and `VMAP.COM`
- [Fonts In Use — Neon Genesis Evangelion](https://fontsinuse.com/uses/28760/neon-genesis-evangelion) — Matisse EB title cards
- [hikaen2/ttf-pc9800](https://github.com/hikaen2/ttf-pc9800) — the ROM-to-TrueType pipeline
- [DOSBox-X](https://dosbox-x.com/) — `FREECG98.BMP`, the clean-room PC-98 font
- Shinonome 16 — kanji coverage, bundled by ttf-pc9800

*Neon Genesis Evangelion* is © khara. This project is unaffiliated fan work; it ships no copyrighted assets.

## License

MIT — see [LICENSE](LICENSE).

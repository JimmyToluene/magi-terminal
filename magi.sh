#!/usr/bin/env bash
#
#  MAGI Terminal — Copyright (C) 2026 JimmyToluene
#  Licensed under the GNU General Public License v3.0. See LICENSE.
#
# ============================================================================
#  NERV CONSOLE — terminal palette derived from Neon Genesis Evangelion
# ============================================================================
#  Applied via OSC escape sequences; works in Termius and any xterm-compatible
#  emulator without touching application settings.
#
#    source ~/.config/magi.sh                # MAGI Monochrome (default)
#    EVA_ACCENT=1 source ~/.config/magi.sh   # NERV Console (canon accents)
#
#  Add to ~/.zshrc to persist. See README for the required guards.
#
#  Sourcing notes are per-slot below. Two rules govern both variants:
#    - Background is #000000. Not near-black. The title cards and the MAGI
#      text screens are pure black, and the whole look depends on that.
#    - Nothing is desaturated for comfort. EVA's UI palette is blunt.
# ============================================================================

_eva_set()  { printf '\033]%s;%s\007' "$1" "$2"; }
_eva_ansi() { printf '\033]4;%d;%s\007' "$1" "$2"; }

if [ -z "${EVA_ACCENT:-}" ]; then
  # ------------------------------------------------------------------------
  #  MAGI MONOCHROME — the amber-on-black text screens. Every slot is a stop
  #  on a ramp between the two official series colors: NERV orange #F66E25
  #  and EVA yellow #F6E201. Nothing is not-amber.
  #
  #  Brightness is assigned by TERMINAL ROLE, not by how often a color shows
  #  up in the series. Slot 4 is directories (ls DIR=01;34) and is read more
  #  than anything else on screen, so it is bright regardless of the fact
  #  that blue is rare in EVA. Only 0 and 8 are allowed to recede.
  # ------------------------------------------------------------------------
  bg=#000000    # title-card black
  fg=#FF9900    # NERV console body text
  cur=#F6E201   # EVA yellow, the brightest thing on the ramp
  sel=#5C2A08   # LCL, backlit

  set -- \
    "#1A0C04" \
    "#E85A1A" \
    "#FFA02E" \
    "#F6C21F" \
    "#FF8A2B" \
    "#FFB347" \
    "#FFC65C" \
    "#FFD9A0" \
    "#7A4A1E" \
    "#FF7038" \
    "#FFB43D" \
    "#F6E201" \
    "#FFA347" \
    "#FFC46B" \
    "#FFD98C" \
    "#FFF3D6"
    #  0  black    the void; only ever a background
    #  1  red      errors, hottest orange on the ramp
    #  2  green    executables (ls EXEC=01;32)
    #  3  yellow   warnings, device files
    #  4  blue     DIRECTORIES (ls DIR=01;34) — must carry the screen
    #  5  magenta  archives, images
    #  6  cyan     SYMLINKS (ls LINK=01;36)
    #  7  white    default text
    #  8  br black dim chrome, comments — the only recessive slot
    #  9-15       bright variants; 11 is official EVA yellow, the peak
else
  # ------------------------------------------------------------------------
  #  NERV CONSOLE — amber carries the screen; accents appear only where the
  #  series assigns them meaning. Blue is Pattern Blue, red is 警告, green is
  #  the hex grid, purple is Unit-01. They are semantic, not decoration.
  # ------------------------------------------------------------------------
  bg=#000000    # title card / MAGI screen ground
  fg=#FF9900    # NERV console body text
  cur=#F66E25   # NERV logo orange (official series color)
  sel=#5C2A08   # LCL, backlit

  set -- \
    "#100A00" \
    "#E81900" \
    "#41BB42" \
    "#F6E201" \
    "#54A2D4" \
    "#9B78C4" \
    "#20BFA6" \
    "#E8E1D4" \
    "#856640" \
    "#FF2D0E" \
    "#58F2A5" \
    "#F9CC38" \
    "#7FC8F0" \
    "#B797DB" \
    "#3CFFD0" \
    "#FFFFFF"
    #  0  black    the void behind the grid, lifted just off bg
    #  1  red      警告 / alert red, also Unit-02
    #  2  green    Unit-01's stripes; the NERV hexagonal screen grid
    #  3  yellow   official EVA yellow; Unit-00 proto
    #  4  blue     PATTERN BLUE — canon: target confirmed as Angel
    #  5  magenta  Unit-01 armor purple
    #  6  cyan     holographic readout, derived from slot 14
    #  7  white    bone / plugsuit off-white
    #  8  br black UI chrome, inactive frame lines
    #  9  br red   the alert flashing
    # 10  br green readout glow at full intensity
    # 11  br yellow caution striping
    # 12  br blue  pattern blue at peak
    # 13  br mag   Unit-01 highlight
    # 14  br cyan  holo readout at peak
    # 15  br white Matisse EB title-card white — the only pure white
fi

i=0
for c in "$@"; do _eva_ansi "$i" "$c"; i=$((i + 1)); done
_eva_set 10 "$fg"   # foreground
_eva_set 11 "$bg"   # background
_eva_set 12 "$cur"  # cursor
_eva_set 17 "$sel"  # selection background (ignored by some emulators)

unset -f _eva_set _eva_ansi
unset bg fg cur sel i c

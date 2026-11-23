#!/usr/bin/env python3
"""Build entry.png for news-image-20261122: a one-page newspaper front page
summing up the world news of Sunday 22 November 2026.

Layout (1024 x 1024, deterministic): masthead with the date, a three-panel
hero illustration (climate summit / burning tanker / Mercury probe), six
labelled story boxes, and an "also today" ticker. All text is drawn with
PIL from DejaVu fonts, so every label is crisp and legible; the hero art
carries no text of its own.

Run: python3 draw.py  -> writes entry.png beside this file.
"""
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
W, H = 1024, 1024

PAPER = (247, 243, 232)
INK = (20, 24, 30)
NAVY = (20, 38, 62)
NAVY2 = (28, 52, 82)
GOLD = (198, 148, 52)
RUST = (166, 52, 32)
GREY = (92, 96, 104)
RULE = (196, 188, 172)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


STORIES = [
    ("CLIMATE  ·  ANTALYA, TURKEY", "COP31 ends with no deal",
     "After 17 days of talks, the climate summit collapses over fossil "
     "fuels. The EU rejects a final text that never names them."),
    ("CONFLICT  ·  BENGHAZI, LIBYA", "Russian warship hit at port",
     "A suspected Ukrainian sea drone strikes a corvette docked at "
     "Benghazi. A second ship is reported targeted."),
    ("CONFLICT  ·  DYMER, UKRAINE", "Kyiv apartment block hit",
     "A Russian drone partly destroys a five-storey block north of Kyiv. "
     "Three people are killed and 14 are missing."),
    ("CONFLICT  ·  STRAIT OF HORMUZ", "Iran strikes tankers",
     "Tankers are hit near Hormuz and a site in Bahrain is struck, two "
     "wounded, as a US naval blockade standoff deepens."),
    ("POLITICS  ·  WASHINGTON, USA", "Democrats take the House",
     "Democrats win at least 258 seats — their largest House majority "
     "since 1992."),
    ("MARKETS  ·  NEW YORK", "Stocks slide in AI sell-off",
     "The S&P 500 falls 3.7% and Japan's Nikkei 5.1% as investors dump "
     "AI shares."),
]

TICKER = ("ALSO TODAY:  BepiColombo enters orbit around Mercury  •  Mexico "
          "captures cartel boss 'El Chapo Isidro'  •  Banten candy factory "
          "fire: 3 dead, 34 missing  •  Gukesh–Sindarov world chess title "
          "match begins  •  UN court: Myanmar committed genocide against "
          "the Rohingya")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 96], fill=NAVY)
    d.rectangle([0, 96, W, 100], fill=GOLD)
    f_title = font(SERIF_B, 34)
    f_date = font(SANS_B, 22)
    d.text((24, 30), "THE WORLD IN ONE PAGE", font=f_title, fill=PAPER)
    date = "SUNDAY 22 NOVEMBER 2026"
    d.text((W - 24 - d.textlength(date, font=f_date), 36), date,
           font=f_date, fill=(232, 196, 110))

    # --- Hero illustration ----------------------------------------------
    hero = Image.open(HERE / "hero.png").convert("RGB")
    # Centre-crop to the 1024x296 strip ratio, then resize.
    tw, th = 1024, 296
    scale = max(tw / hero.width, th / hero.height)
    hero = hero.resize((round(hero.width * scale), round(hero.height * scale)),
                       Image.LANCZOS)
    x0 = (hero.width - tw) // 2
    y0 = (hero.height - th) // 2
    hero = hero.crop((x0, y0, x0 + tw, y0 + th))
    img.paste(hero, (0, 100))
    d.rectangle([0, 396, W, 400], fill=GOLD)

    # --- Deck line --------------------------------------------------------
    f_deck = font(SERIF, 21)
    deck = ("Climate talks collapse, tankers burn in the Strait of Hormuz, "
            "and a probe reaches Mercury.")
    d.text(((W - d.textlength(deck, font=f_deck)) / 2, 414), deck,
           font=f_deck, fill=INK)

    # --- Story grid: 2 columns x 3 rows ----------------------------------
    gx, gy = 24, 452
    bw, bh = 476, 148
    gapx, gapy = 24, 14
    f_kick = font(SANS_B, 15)
    f_body = font(SANS, 17)
    for i, (kicker, head, body) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = gx + col * (bw + gapx)
        y = gy + row * (bh + gapy)
        d.rectangle([x, y, x + bw, y + bh], outline=RULE, width=1)
        d.rectangle([x, y, x + 6, y + bh], fill=RUST if i % 2 == 0 else NAVY2)
        tx = x + 20
        d.text((tx, y + 12), kicker, font=f_kick, fill=RUST)
        # Headline: shrink to fit one line, else wrap to two lines.
        size = 25
        f_head = font(SERIF_B, size)
        while size > 18 and d.textlength(head, font=f_head) > bw - 40:
            size -= 1
            f_head = font(SERIF_B, size)
        head_lines = [head] if d.textlength(head, font=f_head) <= bw - 40 \
            else wrap(d, head, f_head, bw - 40)
        hy = y + 36
        for hl in head_lines[:2]:
            d.text((tx, hy), hl, font=f_head, fill=INK)
            hy += size + 5
        lines = wrap(d, body, f_body, bw - 40)
        ly = hy + 6
        for line in lines[:3]:
            d.text((tx, ly), line, font=f_body, fill=(52, 56, 64))
            ly += 23

    # --- Ticker -----------------------------------------------------------
    ty = 452 + 3 * bh + 2 * gapy + 16  # 940
    d.rectangle([0, ty, W, H], fill=NAVY)
    d.rectangle([0, ty, W, ty + 4], fill=GOLD)
    f_tick = font(SANS, 18)
    lines = wrap(d, TICKER, f_tick, W - 48)
    ly = ty + 14
    for line in lines:
        d.text((24, ly), line, font=f_tick, fill=PAPER)
        ly += 25

    out = HERE / "entry.png"
    img.save(out, "PNG", optimize=True)
    print("wrote", out, img.size, out.stat().st_size, "bytes")


if __name__ == "__main__":
    main()

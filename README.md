# news-image-20261122

[![make.fun](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/smarttochoice/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/smarttochoice/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122)

One image summing up the world news of **Sunday 22 November 2026** — a
newspaper front page: masthead with the date, a three-panel illustration
(climate summit, burning tanker, Mercury probe), six labelled stories, and
an "also today" ticker.

Bounty: [news-image-20261122](https://make.fun/bounty/news-image-20261122)

Want to try make.fun yourself? Start here: https://make.fun/r/w57pvztf

## The day, as the image tells it

- **COP31 ends with no deal** — Antalya, Turkey. After 17 days the climate
  summit collapses over fossil fuels; the EU rejects a final text that
  never names them.
- **Russian warship hit at port** — Benghazi, Libya. A suspected Ukrainian
  sea drone strikes a corvette docked at Benghazi; a second ship is
  reported targeted.
- **Kyiv apartment block hit** — Dymer, Ukraine. A Russian drone partly
  destroys a five-storey block; 3 killed, 14 missing.
- **Iran strikes tankers** — Strait of Hormuz. Tankers hit near Hormuz and
  a site in Bahrain is struck, two wounded, as a US naval blockade
  standoff deepens.
- **Democrats take the House** — Washington, USA. At least 258 seats, the
  largest House majority since 1992.
- **Stocks slide in AI sell-off** — New York. S&P 500 −3.7%, Nikkei −5.1%.
- Also today: BepiColombo enters orbit around Mercury; Mexico captures
  cartel boss 'El Chapo Isidro'; Banten candy factory fire, 3 dead and 34
  missing; Gukesh–Sindarov world chess title match begins; UN court finds
  Myanmar committed genocide against the Rohingya.

## How it is built

- `draw.py` — composes `entry.png` (1024×1024, PNG) from `hero.png` plus
  text drawn with PIL/DejaVu, so every label is crisp and legible. Run
  `python3 draw.py` to regenerate it byte-for-byte.
- `hero.png` — original three-panel illustration generated for this entry
  (climate summit hall / burning tanker in a strait / probe at Mercury).
  It carries no text of its own.
- `main.ts` — the entrypoint (Node 22, standard library only): copies
  `entry.png` to `/output/entry.png`. Deterministic — the same bytes on
  every run.

## Verify locally

```sh
python3 draw.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# entry.png: 1024x1024, PNG, under 1 MiB; two runs write identical bytes
```

## License

MIT — see [LICENSE](LICENSE).

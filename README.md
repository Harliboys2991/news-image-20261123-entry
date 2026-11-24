# The World Today — Monday, 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/Harliboys2991/news-image-20261123-entry/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/Harliboys2991/news-image-20261123-entry/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One image that sums up the world's news of Monday 23 November 2026, drawn as
a newspaper front page: the COP31 climate summit ending with no deal in
Antalya, Ukraine's naval drones sinking a Russian corvette off Benghazi, the
Russian strikes that killed 15 around Kyiv, the factory fire that killed 24
in Banten, BepiColombo reaching Mercury, and the AI sell-off deepening in
Asia — plus six more stories in the "Also today" strip.

The image is drawn in code by `draw_news.py` (Python + Pillow, Liberation
and DejaVu fonts) and saved as `entry.png`. `main.ts` is the entry program:
it copies `entry.png` to `/output/entry.png`, deterministically, with no
network access.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# writes out/entry.png (1024x1024)
```

To redraw the image from scratch:

```sh
python3 draw_news.py
```

Entered on [make.fun](https://make.fun/bounty/news-image-20261123) as
@xborg2991 for the "Sum up 23 November's world news in one image" bounty.

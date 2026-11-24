#!/usr/bin/env python3
"""Draw the 23 November 2026 world-news front page (1024x1024 PNG).

Run once, locally, to produce entry.png. The entry program itself is
main.ts, which only copies entry.png to /output/entry.png, so the grader
never needs PIL or fonts. All text is rendered here, from real reporting
of Monday 23 November 2026 (wire coverage as carried by the day's news
digests: COP31 outcome, Benghazi warship, Kyiv-region strikes, Banten
factory fire, BepiColombo, Asian markets).
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (18, 18, 18)
NAVY = (14, 34, 56)
NAVY2 = (22, 48, 79)
RED = (178, 34, 34)
GOLD = (201, 162, 39)
GRAY = (90, 86, 76)
CARD = (255, 253, 247)
BORDER = (206, 198, 178)
CREAM = (238, 230, 210)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def star(d, cx, cy, r_out, r_in, points, fill, rot=-90):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180 / points)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill)


def wrap(d, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = f"{cur} {w}".strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, text, fnt, max_w, fill, leading=1.18):
    lines = wrap(d, text, fnt, max_w)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


# ---------------------------------------------------------------- canvas
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- masthead -----------------------------------------------------------
d.rectangle([0, 0, W, 96], fill=NAVY)
d.rectangle([0, 96, W, 100], fill=GOLD)
title = "THE WORLD TODAY"
tf = font(SERIF_B, 58)
d.text(((W - d.textlength(title, font=tf)) / 2, 14), title, font=tf, fill=(255, 255, 255))
tag = "ONE DAY  •  EVERY CONTINENT  •  IN ONE PICTURE"
tg = font(SANS_B, 15)
d.text(((W - d.textlength(tag, font=tg)) / 2, 74), tag, font=tg, fill=GOLD)

# ---- date bar -----------------------------------------------------------
date = "MONDAY, 23 NOVEMBER 2026"
df = font(SERIF_B, 46)
dw = d.textlength(date, font=df)
d.text(((W - dw) / 2, 112), date, font=df, fill=INK)
d.line([26, 136, (W - dw) / 2 - 18, 136], fill=RED, width=3)
d.line([(W + dw) / 2 + 18, 136, W - 26, 136], fill=RED, width=3)
sub = "The day's world news, as reported on Monday 23 November 2026"
sf = font(SANS, 19)
d.text(((W - d.textlength(sub, font=sf)) / 2, 164), sub, font=sf, fill=GRAY)

# ---- lead card: COP31 ---------------------------------------------------
LX, LY, LW, LH = 26, 196, 972, 272
d.rectangle([LX, LY, LX + LW, LY + LH], fill=CARD, outline=BORDER, width=2)
# illustration: cracked globe, left half
IX, IY, IW, IH = LX + 2, LY + 2, 452, LH - 4
d.rectangle([IX, IY, IX + IW, IY + IH], fill=NAVY2)
# stars
for sx, sy, sr in ((30, 26, 2), (70, 60, 2), (400, 30, 2), (420, 90, 3),
                   (36, 200, 2), (410, 210, 2), (90, 230, 2)):
    d.ellipse([IX + sx - sr, IY + sy - sr, IX + sx + sr, IY + sy + sr],
              fill=(255, 255, 255))
# globe
cx, cy, cr = IX + IW // 2, IY + IH // 2 - 8, 92
d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(38, 120, 150),
          outline=(180, 220, 235), width=3)
# continents
d.ellipse([cx - 62, cy - 58, cx - 8, cy - 18], fill=(96, 168, 96))
d.ellipse([cx + 6, cy + 6, cx + 58, cy + 52], fill=(96, 168, 96))
d.ellipse([cx - 30, cy + 28, cx + 12, cy + 62], fill=(110, 180, 110))
d.ellipse([cx + 30, cy - 62, cx + 66, cy - 28], fill=(96, 168, 96))
# crack: red zigzag down the globe
crack = [(cx - 18, cy - 88), (cx + 6, cy - 52), (cx - 14, cy - 18),
         (cx + 10, cy + 16), (cx - 8, cy + 50), (cx + 12, cy + 86)]
d.line(crack, fill=RED, width=6, joint="curve")
d.line(crack, fill=(255, 90, 60), width=2, joint="curve")
# NO DEAL ribbon across the bottom of the art
ry = IY + IH - 44
d.rectangle([IX + 34, ry, IX + IW - 34, ry + 32], fill=RED)
rb = "NO DEAL"
rf = font(SANS_B, 22)
d.text(((IW - d.textlength(rb, font=rf)) / 2 + IX, ry + 3), rb, font=rf,
       fill=(255, 255, 255))
# lead text, right half
TX = IX + IW + 24
TW = LX + LW - TX - 22
d.text((TX, LY + 22), "CLIMATE  •  ANTALYA", font=font(SANS_B, 21), fill=RED)
y = text_block(d, TX, LY + 52, "CLIMATE SUMMIT ENDS WITH NO DEAL",
               font(SERIF_B, 38), TW, INK, 1.12)
y += 8
d.line([TX, y, TX + 120, y], fill=RED, width=3)
y += 12
text_block(d, TX, y, "COP31 collapses after record-long talks \u2014 split "
           "over fossil fuels and finance.",
           font(SANS, 20), TW, GRAY, 1.25)

# ---- middle row ---------------------------------------------------------
MY, MH = 482, 224
MW = (972 - 14) // 2


def mid_card(x, kicker, headline, subline, draw_art):
    d.rectangle([x, MY, x + MW, MY + MH], fill=CARD, outline=BORDER, width=2)
    ax, ay, aw, ah = x + 2, MY + 2, MW - 4, 104
    draw_art(ax, ay, aw, ah)
    tx, tw = x + 18, MW - 36
    d.text((tx, MY + 116), kicker, font=font(SANS_B, 19), fill=RED)
    y = text_block(d, tx, MY + 140, headline, font(SERIF_B, 26), tw, INK, 1.1)
    text_block(d, tx, y + 4, subline, font(SANS, 18), tw, GRAY, 1.2)


def art_benghazi(ax, ay, aw, ah):
    # dusk sea, listing warship, drone strike
    d.rectangle([ax, ay, ax + aw, ay + ah], fill=(16, 42, 66))
    d.rectangle([ax, ay + 58, ax + aw, ay + ah], fill=(10, 30, 50))
    # horizon glow
    d.ellipse([ax + aw // 2 - 90, ay + 8, ax + aw // 2 + 90, ay + 72],
              fill=(214, 130, 60))
    d.ellipse([ax + aw // 2 - 60, ay + 22, ax + aw // 2 + 60, ay + 66],
              fill=(240, 180, 90))
    # warship silhouette, listing to starboard
    hx, hy = ax + 120, ay + 62
    hull = [(hx, hy), (hx + 220, hy), (hx + 238, hy + 16),
            (hx + 10, hy + 16)]
    d.polygon(hull, fill=(30, 34, 40))
    d.rectangle([hx + 60, hy - 22, hx + 130, hy], fill=(30, 34, 40))
    d.rectangle([hx + 90, hy - 40, hx + 100, hy - 22], fill=(30, 34, 40))
    d.rectangle([hx + 150, hy - 14, hx + 190, hy], fill=(30, 34, 40))
    # bow explosion + smoke
    star(d, hx + 232, hy - 6, 20, 8, 8, (255, 160, 40))
    star(d, hx + 232, hy - 6, 11, 4, 8, (255, 230, 150))
    d.ellipse([hx + 196, hy - 52, hx + 236, hy - 22], fill=(90, 88, 84))
    d.ellipse([hx + 214, hy - 66, hx + 250, hy - 38], fill=(120, 116, 110))
    # naval drone skimming in from the left
    d.line([ax + 18, ay + 44, hx - 26, hy - 2], fill=(255, 220, 120), width=3)
    d.ellipse([ax + 10, ay + 38, ax + 30, ay + 50], fill=(20, 20, 20))
    d.line([ax + 8, ay + 36, ax + 32, ay + 36], fill=(200, 200, 200), width=2)
    d.line([ax + 8, ay + 52, ax + 32, ay + 52], fill=(200, 200, 200), width=2)
    # waves
    for wx in range(ax + 8, ax + aw - 20, 46):
        d.arc([wx, ay + ah - 16, wx + 34, ay + ah + 2], 180, 360,
              fill=(120, 180, 210), width=2)


def art_kyiv2(ax, ay, aw, ah):
    # night city, one collapsed block, searchlight and dust
    d.rectangle([ax, ay, ax + aw, ay + ah], fill=(10, 22, 38))
    import random
    rnd = random.Random(23)
    bx = ax + 6
    while bx < ax + aw - 30:
        bw = rnd.randint(26, 44)
        bh = rnd.randint(30, 58)
        d.rectangle([bx, ay + ah - 22 - bh, bx + bw, ay + ah - 22],
                    fill=(4, 10, 20))
        for wy in range(ay + ah - 20 - bh, ay + ah - 26, 10):
            for wx in range(bx + 4, bx + bw - 4, 9):
                if rnd.random() < 0.5:
                    d.rectangle([wx, wy, wx + 4, wy + 5],
                                fill=(255, 200, 80))
        bx += bw + 5
    # collapsed block: tilted slab + rubble
    d.polygon([(ax + 150, ay + ah - 22), (ax + 240, ay + ah - 22),
               (ax + 222, ay + 34), (ax + 196, ay + 30)],
              fill=(52, 48, 44))
    d.polygon([(ax + 150, ay + ah - 22), (ax + 196, ay + 30),
               (ax + 178, ay + 26), (ax + 138, ay + ah - 30)],
              fill=(34, 32, 30))
    for rx, ry, rr in ((160, 78, 6), (185, 84, 5), (210, 80, 7),
                       (232, 86, 4), (170, 90, 4)):
        d.ellipse([ax + rx - rr, ay + ry - rr, ax + rx + rr, ay + ry + rr],
                  fill=(90, 86, 80))
    # dust cloud over the rubble
    d.ellipse([ax + 150, ay + 14, ax + 210, ay + 40], fill=(130, 124, 114))
    d.ellipse([ax + 185, ay + 6, ax + 240, ay + 32], fill=(150, 144, 132))
    # searchlight beam from the right
    d.polygon([(ax + aw - 20, ay + ah - 22), (ax + 250, ay + 10),
               (ax + 300, ay + 22)], fill=(255, 240, 180))
    d.ellipse([ax + aw - 28, ay + ah - 30, ax + aw - 12, ay + ah - 14],
              fill=(255, 220, 120))
    # ground
    d.rectangle([ax, ay + ah - 22, ax + aw, ay + ah], fill=(6, 10, 16))


mid_card(26, "WAR  •  MEDITERRANEAN",
         "UKRAINE SINKS RUSSIAN WARSHIP OFF LIBYA",
         "Naval drones hit corvette Merkury at Benghazi.", art_benghazi)
mid_card(26 + MW + 14, "WAR  •  KYIV REGION",
         "RUSSIAN STRIKES KILL 15 AROUND KYIV",
         "11 die in Dymer; boy, 7, pulled alive.",
         art_kyiv2)

# ---- bottom row ---------------------------------------------------------
BY, BH = 720, 184
BW = (972 - 28) // 3


def small_card(x, kicker, headline, subline, draw_art):
    d.rectangle([x, BY, x + BW, BY + BH], fill=CARD, outline=BORDER, width=2)
    ax, ay, aw, ah = x + 2, BY + 2, BW - 4, 74
    draw_art(ax, ay, aw, ah)
    tx, tw = x + 14, BW - 28
    d.text((tx, BY + 86), kicker, font=font(SANS_B, 16), fill=RED)
    y = text_block(d, tx, BY + 106, headline, font(SERIF_B, 23), tw, INK, 1.08)
    text_block(d, tx, y + 3, subline, font(SANS, 17), tw, GRAY, 1.18)


def art_fire(ax, ay, aw, ah):
    # burning factory: sawtooth roof, chimney, flames, smoke
    d.rectangle([ax, ay, ax + aw, ay + ah], fill=(46, 14, 10))
    # factory block
    d.rectangle([ax + 30, ay + 34, ax + aw - 30, ay + ah], fill=(24, 20, 20))
    for i in range(3):
        x0 = ax + 30 + i * 84
        d.polygon([(x0, ay + 34), (x0 + 42, ay + 14), (x0 + 84, ay + 34)],
                  fill=(24, 20, 20))
    # chimney
    d.rectangle([ax + aw - 52, ay + 6, ax + aw - 38, ay + 40],
                fill=(60, 54, 50))
    # flames
    for fx, fh in ((60, 26), (110, 34), (160, 28), (205, 32)):
        d.polygon([(ax + fx - 14, ay + 44), (ax + fx, ay + 44 - fh),
                   (ax + fx + 14, ay + 44)], fill=(255, 140, 30))
        d.polygon([(ax + fx - 7, ay + 44), (ax + fx, ay + 44 - fh + 12),
                   (ax + fx + 7, ay + 44)], fill=(255, 220, 90))
    # smoke
    d.ellipse([ax + 200, ay + 2, ax + 244, ay + 22], fill=(110, 105, 100))
    d.ellipse([ax + 226, ay - 4, ax + 264, ay + 14], fill=(140, 134, 128))
    # lit windows
    for wx in range(ax + 44, ax + aw - 60, 26):
        d.rectangle([wx, ay + 52, wx + 12, ay + 62], fill=(255, 170, 60))


def art_mercury(ax, ay, aw, ah):
    # cratered Mercury + small probe on approach
    d.rectangle([ax, ay, ax + aw, ay + ah], fill=(8, 10, 18))
    for sx, sy in ((20, 12), (60, 30), (260, 14), (290, 44), (150, 8),
                   (40, 58), (230, 60)):
        d.ellipse([ax + sx - 1, ay + sy - 1, ax + sx + 1, ay + sy + 1],
                  fill=(255, 255, 255))
    # planet
    px, py, pr = ax + 92, ay + 40, 30
    d.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(168, 158, 148))
    for cx, cy, cr in ((-12, -8, 6), (8, 4, 8), (-2, 14, 5), (14, -12, 4)):
        d.ellipse([px + cx - cr, py + cy - cr, px + cx + cr, py + cy + cr],
                  fill=(128, 118, 108))
    # trajectory + probe
    d.arc([px + 10, py - 44, px + 190, py + 40], 270, 90,
          fill=(120, 200, 230), width=2)
    qx, qy = ax + 230, ay + 24
    d.rectangle([qx - 8, qy - 6, qx + 8, qy + 6], fill=(220, 220, 220))
    d.rectangle([qx - 26, qy - 3, qx - 8, qy + 3], fill=(60, 110, 200))
    d.rectangle([qx + 8, qy - 3, qx + 26, qy + 3], fill=(60, 110, 200))
    d.line([qx, qy + 6, qx, qy + 14], fill=(220, 220, 220), width=2)


def art_selloff(ax, ay, aw, ah):
    # falling chart, no invented numbers
    d.rectangle([ax, ay, ax + aw, ay + ah], fill=(66, 16, 24))
    pts = [(ax + 12, ay + 14), (ax + 60, ay + 26), (ax + 110, ay + 22),
           (ax + 160, ay + 42), (ax + 210, ay + 50), (ax + 258, ay + 62)]
    d.line(pts, fill=(255, 110, 110), width=5, joint="curve")
    d.polygon([(ax + 258, ay + 62), (ax + 240, ay + 62), (ax + 256, ay + 46)],
              fill=(255, 110, 110))
    d.text((ax + 14, ay + 40), "AI", font=font(SANS_B, 26),
           fill=(255, 200, 90))
    d.text((ax + 196, ay + 6), "TECH", font=font(SANS_B, 20),
           fill=(255, 255, 255))


small_card(26, "DISASTER  •  BANTEN", "FACTORY FIRE KILLS 24",
           "30 missing after sweets-plant blaze.", art_fire)
small_card(26 + BW + 14, "SPACE  •  MERCURY",
           "BEPICOLOMBO REACHES MERCURY",
           "Eight-year trip ends in orbit.", art_mercury)
small_card(26 + 2 * (BW + 14), "MARKETS", "AI SELL-OFF DEEPENS IN ASIA",
           "Tech shares fall again.", art_selloff)

# ---- also-today ticker --------------------------------------------------
TY = 918
d.rectangle([26, TY, 998, TY + 66], fill=NAVY)
d.text((42, TY + 8), "ALSO TODAY", font=font(SANS_B, 19), fill=GOLD)
t1 = ("EU unveils 22nd Russia sanctions  •  Poland: Kh-101 debris at 3 sites"
      "  •  Nigeria boat sinks, 24 dead")
t2 = ("Eurozone inflation hits 4.0%  •  Mexico captures 'El Chapo Isidro'"
      "  •  Skubal signs $450m Mets deal")
tf2 = font(SANS, 17)
assert d.textlength(t1, font=tf2) <= 940, d.textlength(t1, font=tf2)
assert d.textlength(t2, font=tf2) <= 940, d.textlength(t2, font=tf2)
d.text((42, TY + 30), t1, font=tf2, fill=(255, 255, 255))
d.text((42, TY + 50), t2, font=tf2, fill=(255, 255, 255))

# ---- footer -------------------------------------------------------------
ft = "Drawn from reporting of Monday 23 November 2026  •  make.fun news-image-20261123"
ff = font(SANS, 14)
d.text(((W - d.textlength(ft, font=ff)) / 2, 994), ft, font=ff, fill=GRAY)

img.save("entry.png", optimize=True)
print("saved entry.png")

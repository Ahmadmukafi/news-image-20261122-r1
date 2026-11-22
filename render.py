#!/usr/bin/env python3
"""Render THE WORLD TODAY — broadsheet front page for Sunday 22 November 2026.
Build-time only: main.ts never calls this. Run: python3 render.py"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (20, 20, 20)
RED = (179, 39, 30)
SEA = (24, 58, 92)
SEA_LT = (46, 96, 140)
LAND = (217, 201, 163)
LAND2 = (203, 184, 141)
GOLD = (176, 141, 58)
GREY = (107, 101, 88)
WHITE = (255, 255, 255)
DRONE = (230, 230, 225)

FONT_DIRS = ["/usr/share/fonts/truetype/dejavu", "/usr/share/fonts/dejavu"]


def font(name, size):
    for d in FONT_DIRS:
        p = os.path.join(d, name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    raise SystemExit("missing font: " + name)


def serif_b(s):
    return font("DejaVuSerif-Bold.ttf", s)


def serif(s):
    return font("DejaVuSerif.ttf", s)


def sans(s):
    return font("DejaVuSans.ttf", s)


def sans_b(s):
    return font("DejaVuSans-Bold.ttf", s)


def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def rule(draw, x, y, w, weight=2, color=INK):
    draw.rectangle([x, y, x + w, y + weight - 1], fill=color)


def fit_font(draw, text, fname, start, max_w):
    size = start
    while size > 10:
        f = font(fname, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 2
    return font(fname, 10)


def drone(draw, cx, cy, s, color=DRONE):
    # simple delta-wing drone silhouette, nose pointing right
    draw.polygon([(cx - s, cy), (cx + s, cy - s * 0.55), (cx + s * 0.4, cy),
                  (cx + s, cy + s * 0.55)], fill=color)
    draw.line([cx - s, cy, cx - s - s * 0.5, cy], fill=color, width=max(2, s // 4))


def red_x(draw, cx, cy, r):
    w = 4
    draw.line([cx - r, cy - r, cx + r, cy + r], fill=RED, width=w)
    draw.line([cx - r, cy + r, cx + r, cy - r], fill=RED, width=w)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 40  # margin
    CW = W - 2 * MX  # content width 944

    # ---- masthead ----
    rule(d, MX, 16, CW, 3)
    rule(d, MX, 22, CW, 1)
    mast = fit_font(d, "THE WORLD TODAY", "DejaVuSerif-Bold.ttf", 96, CW)
    tw = d.textlength("THE WORLD TODAY", font=mast)
    d.text(((W - tw) / 2, 30), "THE WORLD TODAY", font=mast, fill=INK)
    rule(d, MX, 132, CW, 1)
    meta = sans_b(19)
    d.text((MX, 142), "SUNDAY, 22 NOVEMBER 2026", font=meta, fill=INK)
    ce = "WORLD EDITION"
    d.text(((W - d.textlength(ce, font=meta)) / 2, 142), ce, font=meta, fill=GREY)
    ri = "SIX STORIES"
    d.text((W - MX - d.textlength(ri, font=meta), 142), ri, font=meta, fill=GREY)
    rule(d, MX, 168, CW, 2)

    # ---- lead kicker + headline ----
    kick = sans_b(21)
    d.text((MX, 182), "THE GULF  ·  LEAD STORY", font=kick, fill=RED)
    lh = serif_b(54)
    d.text((MX, 210), "IRAN SAYS IT DOWNED", font=lh, fill=INK)
    d.text((MX, 268), "TWO U.S. DRONES", font=lh, fill=INK)
    rule(d, MX, 332, 120, 4, RED)
    deck = sans(20)
    deck_lines = wrap(d, "Guards say a new air-defence system brought down an MQ-9 over the "
                         "Strait of Hormuz and an MQ-1 over Qeshm Island. Washington had no "
                         "immediate comment.", deck, CW)
    y = 346
    for ln in deck_lines:
        d.text((MX, y), ln, font=deck, fill=INK)
        y += 26

    # ---- lead art panel: stylised Strait of Hormuz ----
    px0, py0, px1, py1 = MX, 408, W - MX, 568
    d.rectangle([px0, py0, px1, py1], fill=SEA)
    # Iran landmass (top)
    d.polygon([(px0, py0), (px1, py0), (px1, py0 + 30), (700, py0 + 54),
               (480, py0 + 40), (300, py0 + 58), (px0, py0 + 46)], fill=LAND)
    d.text((px0 + 18, py0 + 8), "IRAN", font=sans_b(20), fill=(90, 74, 44))
    # Oman / Arabian peninsula (bottom right)
    d.polygon([(px1, py1), (px1, py1 - 58), (800, py1 - 44), (620, py1 - 70),
               (560, py1 - 26), (620, py1)], fill=LAND2)
    # strait channel highlight
    d.line([(px0 + 120, py0 + 78), (px1 - 60, py1 - 70)], fill=SEA_LT, width=26)
    # tanker
    d.rectangle([px0 + 520, py0 + 108, px0 + 620, py0 + 128], fill=(205, 205, 200))
    d.rectangle([px0 + 528, py0 + 94, px0 + 560, py0 + 108], fill=(205, 205, 200))
    # drones + red X marks
    drone(d, px0 + 300, py0 + 88, 28)
    red_x(d, px0 + 300, py0 + 88, 17)
    d.text((px0 + 338, py0 + 74), "MQ-9", font=sans_b(20), fill=WHITE)
    drone(d, px0 + 700, py0 + 60, 24)
    red_x(d, px0 + 700, py0 + 60, 15)
    d.text((px0 + 732, py0 + 46), "MQ-1", font=sans_b(20), fill=WHITE)
    # panel caption strip
    d.rectangle([px0, py1 - 30, px1, py1], fill=(12, 30, 48))
    cap = sans_b(17)
    d.text((px0 + 12, py1 - 25), "THE STRAIT OF HORMUZ  —  TRAFFIC 65% BELOW PRE-WAR LEVELS",
           font=cap, fill=WHITE)

    # ---- section divider + header ----
    rule(d, MX, 584, CW, 2)
    sec = sans_b(19)
    d.text((MX, 596), "MORE FROM THE DAY", font=sec, fill=INK)
    rule(d, MX, 622, CW, 1)

    # ---- story blocks ----
    def story(x, y, w, kicker, headline, body, glyph):
        d.text((x, y), kicker, font=sans_b(16), fill=RED)
        glyph(x + w - 34, y + 2)
        hf = serif_b(25)
        lines = wrap(d, headline, hf, w - 44)
        yy = y + 24
        for ln in lines[:2]:
            d.text((x, yy), ln, font=hf, fill=INK)
            yy += 30
        bf = sans(16)
        blines = wrap(d, body, bf, w)
        yy += 4
        for ln in blines[:3]:
            d.text((x, yy), ln, font=bf, fill=INK)
            yy += 21
        return yy

    def g_burst(cx, cy):
        for a in range(8):
            import math
            x2 = cx + 15 * math.cos(a * math.pi / 4)
            y2 = cy + 15 * math.sin(a * math.pi / 4)
            d.line([cx, cy, x2, y2], fill=GOLD, width=3)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED)

    def g_globe(cx, cy):
        d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], outline=SEA, width=3)
        d.line([cx - 14, cy, cx + 14, cy], fill=SEA, width=2)
        d.arc([cx - 7, cy - 14, cx + 7, cy + 14], 270, 90, fill=SEA, width=2)

    def g_star(cx, cy):
        import math
        pts = []
        for i in range(10):
            r = 16 if i % 2 == 0 else 7
            a = -math.pi / 2 + i * math.pi / 5
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        d.polygon(pts, fill=GOLD)

    def g_quake(cx, cy):
        pts = [(cx - 16, cy + 6), (cx - 8, cy - 8), (cx, cy + 6),
               (cx + 8, cy - 8), (cx + 16, cy + 6)]
        d.line(pts, fill=RED, width=3, joint="curve")

    col_w = (CW - 32) // 2
    x2 = MX + col_w + 32
    story(MX, 636, col_w, "UKRAINE", "RUSSIA'S BIGGEST ATTACK OF THE YEAR",
          "110 missiles and 400+ drones hit Ukraine; at least 9 killed. Zelensky calls "
          "Putin a \u2018killer\u2019 after Trump calls him a friend.", g_burst)
    story(x2, 636, col_w, "CLIMATE", "COP31 DEADLOCKED OVER FOSSIL FUELS",
          "Talks run into overtime with no final deal as nations split on phasing out "
          "oil, gas and coal.", g_globe)
    rule(d, MX, 796, CW, 1)
    story(MX, 808, col_w, "MEXICO", "\u2018EL CHAPO ISIDRO\u2019 CAPTURED",
          "FBI most-wanted cartel boss seized in Sinaloa; 11 killed as gunmen fought "
          "troops.", g_star)
    story(x2, 808, col_w, "PERU", "6.9 QUAKE SHAKES THE ANDES",
          "Strong tremor felt in Lima; no casualties immediately reported.", g_quake)

    # ---- Shenzhen strip ----
    rule(d, MX, 946, CW, 1)
    sh_kick = sans_b(20)
    kick_txt = "SHENZHEN  \u2014  "
    d.text((MX, 960), kick_txt, font=sh_kick, fill=RED)
    sh = serif_b(24)
    d.text((MX + d.textlength(kick_txt, font=sh_kick), 959),
           "TRUMP, XI AND PUTIN SIGN FOUR-POINT PACT", font=sh, fill=INK)
    foot = sans(13)
    ft = "Sources: Al Jazeera \u00b7 BBC \u00b7 AP \u00b7 Reuters \u00b7 USGS \u00b7 SBS"
    d.text((MX, 994), ft, font=foot, fill=GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()

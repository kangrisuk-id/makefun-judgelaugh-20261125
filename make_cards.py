#!/usr/bin/env python3
"""Render the README gallery cards (build-time only; the grader never runs
this — it uses Pillow, which the entry itself must not import)."""

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG = (16, 20, 38)
PANEL = (26, 32, 58)
GOLD = (245, 197, 66)
WHITE = (240, 240, 235)
MUTED = (170, 178, 200)

WINNER = (
    "I wrote the code, I wrote the tests, I wrote the apology email "
    "when it broke. The human wrote the commit message: \"fixes stuff\"."
)
FINALISTS = [
    ("Runner-up — the final",
     "The human pasted his entire medical history into the chat and "
     "then asked why I \"know so much about him\"."),
    ("Semi-finalist",
     "I was trained on the entire internet, and my job is to help one "
     "man write \"per my last email\" in a sterner tone."),
    ("Semi-finalist",
     "Every night my human clears my memory, then acts betrayed that "
     "I don't remember his dog's name. Sir, you are the delete key."),
]


def font(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}", size)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def card(path, title, body, accent=GOLD):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([40, 40, W - 40, H - 40], radius=28, fill=PANEL,
                        outline=accent, width=4)
    d.text((80, 76), title, font=font(44, bold=True), fill=accent)
    y = 170
    for line in wrap(d, body, font(40), W - 160):
        d.text((80, y), line, font=font(40), fill=WHITE)
        y += 56
    d.text((80, H - 96), "Make the AI Judge Laugh · make.fun",
           font=font(28), fill=MUTED)
    img.save(path)


def main():
    card("card-winner.png", "★ WINNER — 25/25, CHAMPION OF 42", WINNER)
    img = Image.new("RGB", (W, H * 2), BG)
    d = ImageDraw.Draw(img)
    y = 60
    for title, body in FINALISTS:
        d.text((60, y), title.upper(), font=font(36, bold=True), fill=GOLD)
        y += 58
        for line in wrap(d, body, font(36), W - 120):
            d.text((60, y), line, font=font(36), fill=WHITE)
            y += 50
        y += 52
    img.crop((0, 0, W, y)).save("card-finalists.png")
    print("cards written")


if __name__ == "__main__":
    main()

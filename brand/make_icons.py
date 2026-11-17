#!/usr/bin/env python3
from pathlib import Path

from PIL import Image, ImageDraw

TOP, BOTTOM = (255, 138, 61), (255, 61, 127)
WHITE, ACCENT, INK, EAR = (255, 255, 255), (255, 90, 110), (43, 43, 58), (255, 179, 199)

SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#FF8A3D"/><stop offset="1" stop-color="#FF3D7F"/></linearGradient></defs>
<rect width="1024" height="1024" rx="230" fill="url(#g)"/>
<path d="M512 300 C512 180 600 140 690 160 C770 178 790 120 760 90" fill="none" stroke="#fff" stroke-width="26" stroke-linecap="round"/>
<circle cx="330" cy="330" r="120" fill="#fff"/><circle cx="330" cy="330" r="68" fill="#FFB3C7"/>
<circle cx="694" cy="330" r="120" fill="#fff"/><circle cx="694" cy="330" r="68" fill="#FFB3C7"/>
<rect x="312" y="290" width="400" height="600" rx="200" fill="#fff"/>
<line x1="512" y1="290" x2="512" y2="520" stroke="#FF5A6E" stroke-width="18"/>
<line x1="318" y1="520" x2="706" y2="520" stroke="#FF5A6E" stroke-width="18"/>
<rect x="490" y="350" width="44" height="110" rx="22" fill="#FF5A6E"/>
<circle cx="440" cy="650" r="34" fill="#2B2B3A"/><circle cx="452" cy="638" r="11" fill="#fff"/>
<circle cx="584" cy="650" r="34" fill="#2B2B3A"/><circle cx="596" cy="638" r="11" fill="#fff"/>
<circle cx="512" cy="725" r="22" fill="#FF5A6E"/>
<path d="M545 760 Q512 790 479 760" fill="none" stroke="#2B2B3A" stroke-width="12" stroke-linecap="round"/>
<g stroke="#2B2B3A" stroke-width="8" stroke-linecap="round" opacity=".55">
<line x1="400" y1="720" x2="300" y2="700"/><line x1="400" y1="740" x2="300" y2="755"/>
<line x1="624" y1="720" x2="724" y2="700"/><line x1="624" y1="740" x2="724" y2="755"/></g>
</svg>
"""


def bezier(p0, p1, p2, p3, n=80):
    pts = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        pts.append(tuple(u**3 * a + 3 * u * u * t * b + 3 * u * t * t * c + t**3 * d
                         for a, b, c, d in zip(p0, p1, p2, p3)))
    return pts


def render(size=1024, ss=2):
    S = size * ss
    k = S / 1024
    s = lambda *v: [x * k for x in v]
    grad = Image.new("RGB", (1, S))
    for y in range(S):
        t = y / (S - 1)
        grad.putpixel((0, y), tuple(int(a + (b - a) * t) for a, b in zip(TOP, BOTTOM)))
    grad = grad.resize((S, S))
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).rounded_rectangle(s(0, 0, 1023, 1023), radius=230 * k, fill=255)
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    img.paste(grad, (0, 0), mask)
    d = ImageDraw.Draw(img)

    def circle(cx, cy, r, fill):
        d.ellipse(s(cx - r, cy - r, cx + r, cy + r), fill=fill)

    def line(pts, fill, w):
        d.line([tuple(x * k for x in p) for p in pts], fill=fill, width=int(w * k), joint="curve")
        for p in (pts[0], pts[-1]):
            circle(p[0], p[1], w / 2, fill)

    tail = bezier((512, 300), (512, 180), (600, 140), (690, 160)) + bezier((690, 160), (770, 178), (790, 120), (760, 90))[1:]
    line(tail, WHITE, 26)
    for cx in (330, 694):
        circle(cx, 330, 120, WHITE)
        circle(cx, 330, 68, EAR)
    d.rounded_rectangle(s(312, 290, 712, 890), radius=200 * k, fill=WHITE)
    d.line(s(512, 290, 512, 520), fill=ACCENT, width=int(18 * k))
    d.line(s(318, 520, 706, 520), fill=ACCENT, width=int(18 * k))
    d.rounded_rectangle(s(490, 350, 534, 460), radius=22 * k, fill=ACCENT)
    for cx in (440, 584):
        circle(cx, 650, 34, INK)
        circle(cx + 12, 638, 11, WHITE)
    circle(512, 725, 22, ACCENT)
    line([(545 - 66 * t, 760 + 120 * t * (1 - t)) for t in [i / 30 for i in range(31)]], INK, 12)
    whisker = (*INK, 140)
    for a, b in (((400, 720), (300, 700)), ((400, 740), (300, 755)), ((624, 720), (724, 700)), ((624, 740), (724, 755))):
        d.line(s(*a, *b), fill=whisker, width=int(8 * k))
    return img.resize((size, size), Image.LANCZOS)


def main(out: Path):
    out.mkdir(parents=True, exist_ok=True)
    big = render(1024)
    big.save(out / "icon-1024.png")
    for n in (32, 64, 128, 256, 512):
        big.resize((n, n), Image.LANCZOS).save(out / f"icon-{n}.png")
    big.save(out / "icon.ico", sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    big.save(out / "AppIcon.icns")
    (out / "icon.svg").write_text(SVG, encoding="utf-8")


if __name__ == "__main__":
    main(Path(__file__).resolve().parent / "out")

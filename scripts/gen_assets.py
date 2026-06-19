#!/usr/bin/env python3
"""Genera los assets binarios del sitio Marz Labs.

Salidas (en la raíz del proyecto):
  - favicon.ico           (16/32/48 px, esquinas redondeadas)
  - apple-touch-icon.png  (180x180, sangre completa)
  - assets/og-image.png   (1200x630, tarjeta social)

`favicon.svg` se edita a mano. Requiere Pillow (`pip install Pillow`).
Ejecutar:  python3 scripts/gen_assets.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

# Raíz del proyecto = carpeta padre de este script.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# --- Tokens de marca (deben coincidir con assets/styles.css) ---
ACCENT    = (30, 58, 138, 255)   # #1e3a8a
WHITE     = (255, 255, 255, 255)
BG        = (250, 250, 250, 255) # #fafafa
INK       = (10, 10, 10, 255)    # #0a0a0a
INK_SOFT  = (64, 64, 64, 255)    # #404040
INK_MUTED = (82, 82, 82, 255)    # #525252
SS = 8  # supersampling para bordes nítidos


def m_points(size):
    """Vértices de la 'M' del monograma, escalados a `size` (viewBox base 32)."""
    s = size / 32.0
    pts = [(9, 23), (9, 9), (16, 17), (23, 9), (23, 23)]
    return [(x * s, y * s) for x, y in pts]


def draw_icon(size, rounded=True, transparent=True):
    big = size * SS
    base = (0, 0, 0, 0) if transparent else ACCENT
    img = Image.new("RGBA", (big, big), base)
    d = ImageDraw.Draw(img)
    if rounded:
        radius = int(7 * (big / 32))
        d.rounded_rectangle([0, 0, big - 1, big - 1], radius=radius, fill=ACCENT)
    elif transparent:
        d.rectangle([0, 0, big, big], fill=ACCENT)
    pts = m_points(big)
    w = max(2, int(round(2.6 * (big / 32))))
    d.line(pts, fill=WHITE, width=w, joint="curve")
    r = w / 2.0
    for (x, y) in pts:  # tapas/uniones redondeadas
        d.ellipse([x - r, y - r, x + r, y + r], fill=WHITE)
    return img.resize((size, size), Image.LANCZOS)


def sf(size, weight):
    """San Francisco variable (eje de peso); cae a Arial si no está disponible."""
    try:
        f = ImageFont.truetype("/System/Library/Fonts/SFNS.ttf", size)
        try:
            axes = f.get_variation_axes()
            vals = []
            for a in axes:
                nm = a.get("name", b"")
                nm = nm.decode() if isinstance(nm, bytes) else nm
                vals.append(weight if nm.lower() in ("weight", "wght")
                            else a.get("default", a.get("minimum", 0)))
            f.set_variation_by_axes(vals)
        except Exception:
            pass
        return f
    except Exception:
        fp = ("/System/Library/Fonts/Supplemental/Arial Bold.ttf" if weight >= 600
              else "/System/Library/Fonts/Supplemental/Arial.ttf")
        return ImageFont.truetype(fp, size)


def main():
    draw_icon(256, rounded=True, transparent=True).save(
        "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    draw_icon(180, rounded=False, transparent=False).convert("RGB").save(
        "apple-touch-icon.png")

    W, H, M = 1200, 630, 96
    og = Image.new("RGBA", (W, H), BG)
    d = ImageDraw.Draw(og)

    logo_y = 224
    og.alpha_composite(draw_icon(104, rounded=True, transparent=True), (M, logo_y))
    d.text((M + 104 + 36, logo_y + 52), "Marz Labs",
           font=sf(96, 640), fill=INK, anchor="lm")
    d.text((M, 392), "Software empresarial para Centroamérica",
           font=sf(42, 430), fill=INK_SOFT, anchor="lt")
    d.rectangle([M, 486, M + 64, 491], fill=ACCENT)
    d.text((M, 512), "marzlabs.tech", font=sf(30, 500), fill=INK_MUTED, anchor="lt")

    os.makedirs("assets", exist_ok=True)
    og.convert("RGB").save("assets/og-image.png")
    print("Assets generados: favicon.ico, apple-touch-icon.png, assets/og-image.png")


if __name__ == "__main__":
    main()

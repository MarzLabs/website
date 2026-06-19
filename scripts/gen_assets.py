#!/usr/bin/env python3
"""Genera los assets binarios del sitio Marz Labs a partir del logo de marca.

Fuente: assets/logo.png (lockup horizontal: marca circular + "MARZ LABS").
Salidas (en la raíz del proyecto):
  - favicon.ico           (16/32/48 px, a partir de la marca circular)
  - apple-touch-icon.png  (180x180, marca sobre fondo blanco)
  - assets/og-image.png   (1200x630, logo + tagline)

Requiere Pillow (`pip install Pillow`).  Ejecutar:  python3 scripts/gen_assets.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# --- Tokens de marca (deben coincidir con assets/styles.css) ---
ACCENT    = (219, 120, 81, 255)  # #db7851 terracota
BG        = (250, 250, 250, 255) # #fafafa
INK_SOFT  = (64, 64, 64, 255)    # #404040
INK_MUTED = (82, 82, 82, 255)    # #525252

logo = Image.open("assets/logo.png").convert("RGBA")

# La marca circular ocupa la región cuadrada izquierda del lockup.
mark = logo.crop((0, 0, logo.height, logo.height))
mark = mark.crop(mark.getbbox())          # recorta al contenido
w, h = mark.size
side = max(w, h)
square = Image.new("RGBA", (side, side), (0, 0, 0, 0))
square.paste(mark, ((side - w) // 2, (side - h) // 2), mark)


def icon_from_mark(size, bg=None, pad=0.04):
    inner = round(size * (1 - 2 * pad))
    m = square.resize((inner, inner), Image.LANCZOS)
    canvas = Image.new("RGBA", (size, size), bg if bg else (0, 0, 0, 0))
    off = (size - inner) // 2
    canvas.alpha_composite(m, (off, off))
    return canvas


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
    icon_from_mark(256, bg=None, pad=0.04).save(
        "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    icon_from_mark(180, bg=(255, 255, 255, 255), pad=0.14).convert("RGB").save(
        "apple-touch-icon.png")

    # OG image con el logo real
    W, H, M = 1200, 630, 96
    og = Image.new("RGBA", (W, H), BG)
    d = ImageDraw.Draw(og)

    target_w = 500
    logo_r = logo.resize((target_w, round(logo.height * target_w / logo.width)),
                         Image.LANCZOS)
    ly = 156
    og.alpha_composite(logo_r, (M, ly))

    ty = ly + logo_r.height + 52
    d.text((M, ty), "Software empresarial para Centroamérica",
           font=sf(40, 440), fill=INK_SOFT, anchor="lt")
    d.rectangle([M, ty + 76, M + 64, ty + 81], fill=ACCENT)
    d.text((M, ty + 104), "marzlabs.tech", font=sf(30, 500), fill=INK_MUTED, anchor="lt")

    os.makedirs("assets", exist_ok=True)
    og.convert("RGB").save("assets/og-image.png")
    print("Assets generados: favicon.ico, apple-touch-icon.png, assets/og-image.png")


if __name__ == "__main__":
    main()

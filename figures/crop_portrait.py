#!/usr/bin/env python3
"""Recadre le portrait de l'accueil depuis la photo brute d'appareil.

Sortie : assets/portrait.jpg (600 × 600, sRGB, JPEG 85).
Les bornes sont des fractions de la largeur (W) et de la hauteur (H) de
l'original, pour rester lisibles si la source change de définition.

Usage : python3 figures/crop_portrait.py [chemin/vers/source.JPG]
"""

import sys
from pathlib import Path

from PIL import Image, ImageOps

SOURCE = Path.home() / "Downloads" / "DSC_6242.JPG"
TARGET = Path(__file__).resolve().parent.parent / "assets" / "portrait.jpg"

# Fenêtre de recadrage, en fractions de W et H.
#
# Contrainte géométrique de cette photo : la tête va de 0.20 W à 0.72 W et de
# 0.055 H à 0.68 H, soit 1849 px de haut pour 1324 px de large. Une fenêtre
# carrée contenant toute la tête fait donc ~1900 px de côté, et son bord
# gauche ne peut pas dépasser 0.20 W sans rogner les cheveux et la monture des
# lunettes. Les bornes ci-dessous sont le meilleur compromis trouvé.
LEFT = 0.185  # bord gauche : au ras des cheveux
TOP = 0.045   # juste au-dessus du sommet du crâne
SIDE = 1900   # côté de la fenêtre carrée, en pixels de l'original
SIZE = 600
QUALITY = 85


def main() -> None:
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else SOURCE
    im = ImageOps.exif_transpose(Image.open(source)).convert("RGB")
    w, h = im.size
    print(f"source : {source}")
    print(f"dimensions : {w} × {h} px")

    left, top, side = round(LEFT * w), round(TOP * h), SIDE
    # Fenêtre carrée ; si elle déborde, on rétrécit plutôt que de remonter le
    # haut (le sommet du crâne doit rester dans le cadre).
    side = min(side, w - left, h - top)
    right, bottom = left + side, top + side

    print(f"fenêtre : x {left}–{right}, y {top}–{bottom} ({side} × {side} px)")
    out = im.crop((left, top, right, bottom)).resize(
        (SIZE, SIZE), Image.LANCZOS
    )
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    out.save(TARGET, "JPEG", quality=QUALITY, optimize=True, subsampling=0)
    print(f"écrit : {TARGET} ({TARGET.stat().st_size // 1024} Ko)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate the placeholder assets (portrait, research figures, CV pdf).

Run once; the outputs are committed. Re-run only if a placeholder needs
different dimensions. Every file it writes is meant to be replaced by the
real asset later, at the same path and with the same dimensions.

    python3 scripts/make_placeholders.py
"""

import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"

ACCENT = "#2a5d78"

# name, width, height, label, label font size (the portrait is displayed small,
# so its label needs to be proportionally bigger to stay readable)
PLACEHOLDERS = [
    ("portrait.svg", 600, 750, "Portrait", 46),
    ("coexistence.svg", 1200, 675, "Coexistence, feasibility & structural stability", 40),
    ("bef.svg", 1200, 675, "Biodiversity & ecosystem functioning", 40),
    ("food-webs.svg", 1200, 675, "Food-web structure and dynamics", 40),
]

SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"
     viewBox="0 0 {w} {h}" role="img" aria-label="{label} placeholder">
  <rect width="{w}" height="{h}" fill="#eef1f3"/>
  <rect x="0.5" y="0.5" width="{w1}" height="{h1}" fill="none"
        stroke="#c9d2d8" stroke-width="1"/>
  <line x1="0" y1="0" x2="{w}" y2="{h}" stroke="#dde3e7" stroke-width="1"/>
  <line x1="{w}" y1="0" x2="0" y2="{h}" stroke="#dde3e7" stroke-width="1"/>
  <text x="{cx}" y="{ty}" text-anchor="middle"
        font-family="system-ui, sans-serif" font-size="{fs}" fill="{accent}">{label}</text>
  <text x="{cx}" y="{sy}" text-anchor="middle"
        font-family="system-ui, sans-serif" font-size="{fs2}" fill="#7b8792">{w} &#215; {h} placeholder</text>
</svg>
"""


def write_svgs():
    IMG.mkdir(parents=True, exist_ok=True)
    for name, w, h, label, fs in PLACEHOLDERS:
        (IMG / name).write_text(
            SVG.format(
                w=w, h=h, w1=w - 1, h1=h - 1, cx=w // 2,
                ty=h // 2 - fs // 2, sy=h // 2 + fs, fs=fs, fs2=int(fs * 0.7),
                label=html.escape(label, quote=True), accent=ACCENT,
            ),
            encoding="utf-8",
        )
        print("wrote", (IMG / name).relative_to(ROOT))


PDF_LINES = [
    (56, "Mario Desallais - Curriculum Vitae"),
    (30, "PLACEHOLDER"),
    (18, ""),
    (18, "This file is a placeholder. Replace assets/cv.pdf with the real CV;"),
    (18, "the download link on the CV page points here and needs no edit."),
]


def write_pdf():
    """Write a minimal one-page PDF without any third-party dependency."""
    y = 700
    content = ["BT"]
    for size, text in PDF_LINES:
        if text:
            escaped = text.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")
            content.append(f"/F1 {size} Tf 1 0 0 1 60 {y} Tm ({escaped}) Tj")
        y -= int(size * 1.8)
    content.append("ET")
    stream = "\n".join(content).encode("latin-1")

    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
        b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream",
    ]

    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for i, obj in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n".encode() + obj + b"\nendobj\n"

    xref_at = len(out)
    out += f"xref\n0 {len(objects) + 1}\n".encode()
    out += b"0000000000 65535 f \n"
    for off in offsets:
        out += f"{off:010d} 00000 n \n".encode()
    out += f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_at}\n%%EOF\n".encode()

    path = ROOT / "assets" / "cv.pdf"
    path.write_bytes(bytes(out))
    print("wrote", path.relative_to(ROOT))


if __name__ == "__main__":
    write_svgs()
    write_pdf()

from __future__ import annotations

from pathlib import Path

import cairosvg
from PIL import Image


BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "dados_produtividade" / "static" / "dados_produtividade"
SVG_PATH = STATIC_DIR / "favicon.svg"

SIZES = [16, 32, 180, 192, 512]


def generate_pngs() -> None:
    for size in SIZES:
        output = STATIC_DIR / f"favicon-{size}x{size}.png"
        cairosvg.svg2png(
            url=str(SVG_PATH),
            write_to=str(output),
            output_width=size,
            output_height=size,
        )


def generate_ico() -> None:
    png_32 = STATIC_DIR / "favicon-32x32.png"
    png_16 = STATIC_DIR / "favicon-16x16.png"
    if not png_32.exists() or not png_16.exists():
        raise FileNotFoundError("PNG base não encontrado. Rode generate_pngs primeiro.")

    img_32 = Image.open(png_32)
    img_16 = Image.open(png_16)
    ico_path = STATIC_DIR / "favicon.ico"
    img_32.save(ico_path, format="ICO", sizes=[(32, 32), (16, 16)])
    img_16.close()
    img_32.close()


def main() -> None:
    if not SVG_PATH.exists():
        raise FileNotFoundError(f"SVG não encontrado: {SVG_PATH}")

    generate_pngs()
    generate_ico()
    print("Favicons gerados em:", STATIC_DIR)


if __name__ == "__main__":
    main()

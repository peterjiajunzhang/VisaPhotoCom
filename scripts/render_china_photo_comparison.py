#!/usr/bin/env python3
"""Render the bilingual comparison cards with Pillow and macOS system fonts."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONTS = Path("/System/Library/Fonts")
PINGFANG = next(
    iter(sorted(Path("/System/Library/AssetsV2").glob("com_apple_MobileAsset_Font8/*.asset/AssetData/PingFang.ttc"))),
    FONTS / "PingFang.ttc",
)

LABELS = {
    "en": (
        "U.S. vs. China visa photo sizes", "Paper prints shown at the same scale",
        "U.S. print", "China print", "China upload",
        "2 × 2 in", "33 × 48 mm", "3:4 JPEG",
        "Square", "Portrait", "354 × 472 to 420 × 560 px",
    ),
    "zh-hans": (
        "美签与中国签证照片尺寸对比", "两种纸质照片按同一比例绘制",
        "美国纸质照片", "中国纸质照片", "中国网上上传",
        "2 × 2 英寸", "33 × 48 毫米", "3:4 JPEG",
        "正方形", "竖幅", "354×472 至 420×560 像素",
    ),
}

INK = "#102a43"
MUTED = "#465f76"
BLUE = "#1959a5"
TEAL = "#176951"
PRINT_SCALE = 3.6
SUPERSAMPLE = 2


def render(locale, labels):
    title, subtitle, *labels = labels
    image = Image.new("RGB", (1200 * SUPERSAMPLE, 630 * SUPERSAMPLE), "#f4f8fc")
    draw = ImageDraw.Draw(image)
    font_path = FONTS / "HelveticaNeue.ttc" if locale == "en" else PINGFANG
    regular, bold = (0, 1) if locale == "en" else (3, 11)

    def text(x, y, value, size, color=INK, strong=False, anchor="lt"):
        font = ImageFont.truetype(str(font_path), size * SUPERSAMPLE, index=bold if strong else regular)
        draw.text((x * SUPERSAMPLE, y * SUPERSAMPLE), value, font=font, fill=color, anchor=anchor)

    def box(coords, fill, radius, stroke=None, width=1):
        draw.rounded_rectangle(
            [round(value * SUPERSAMPLE) for value in coords],
            fill=fill, radius=radius * SUPERSAMPLE, outline=stroke, width=width * SUPERSAMPLE,
        )

    text(52, 48, title, 57, strong=True)
    text(54, 124, subtitle, 34, color=MUTED)
    box((48, 196, 761, 580), "white", 22, "#dce6ef", 2)
    box((781, 196, 1152, 580), "#e7f4ef", 22, "#b4d5ca", 2)

    physical_sizes = ((50.8, 50.8), (33, 48))
    sizes = [(width * PRINT_SCALE, height * PRINT_SCALE) for width, height in physical_sizes]
    # The digital example shares an illustrative height. Pixels have no physical scale.
    sizes.append((183 * 3 / 4, 183))
    names, dimensions, descriptions = labels[:3], labels[3:6], labels[6:]
    for center, (width, height), name, dimension, description, color, fill in zip(
        (225, 584, 966), sizes, names, dimensions, descriptions,
        (BLUE, BLUE, TEAL), ("#eaf2fb", "#eaf2fb", "white"),
    ):
        text(center, 223, name, 36, color=color, strong=True, anchor="mt")
        box((center - width / 2, 463 - height, center + width / 2, 463), fill, 0, color, 4)
        text(center, 483, dimension, 38, strong=True, anchor="mt")
        text(center, 536, description, 28, color=MUTED, anchor="mt")

    output = ROOT / "assets" / "guides" / f"china-us-photo-comparison-{locale}.png"
    card = image.resize((1200, 630), Image.Resampling.LANCZOS)
    card.quantize(colors=192).save(output, optimize=True)


if __name__ == "__main__":
    for locale, labels in LABELS.items():
        render(locale, labels)

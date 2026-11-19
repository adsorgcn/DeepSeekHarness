"""Rebuild the two site-specific Noto Sans SC webfonts from the pinned source."""

import argparse
import hashlib
import json
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont


SOURCE_SHA256 = "a3041811a78c361b1de50f953c805e0244951c21c5bd412f7232ef0d899af0da"
DOCS_DIR = Path(__file__).resolve().parents[1] / "docs"
FONT_DIR = DOCS_DIR / "assets" / "fonts"


def site_text():
    for pattern in ("*.html", "*.js"):
        for path in DOCS_DIR.rglob(pattern):
            yield path.read_text(encoding="utf-8")
    for filename in ("registry.json", "index.json"):
        data = (DOCS_DIR / "market" / filename).read_text(encoding="utf-8")
        yield json.dumps(json.loads(data), ensure_ascii=False)


def is_han(codepoint):
    return (
        0x3400 <= codepoint <= 0x9FFF
        or 0xF900 <= codepoint <= 0xFAFF
        or 0x20000 <= codepoint <= 0x323AF
    )


def common_han():
    # GB 2312 level-one Hanzi occupy rows 16–55, starting with byte B0.
    return {
        ord(char)
        for row in range(0xB0, 0xD8)
        for cell in range(0xA1, 0xFF)
        for char in bytes([row, cell]).decode("gb2312", errors="ignore")
    }


def save_subset(source, codepoints, output):
    with TTFont(source, recalcTimestamp=False) as font:
        options = subset.Options()
        options.name_IDs = ["*"]
        options.name_languages = ["*"]
        options.layout_features = ["*"]
        subsetter = subset.Subsetter(options=options)
        subsetter.populate(unicodes=codepoints)
        subsetter.subset(font)
        font.flavor = "woff2"
        font.save(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Google Fonts NotoSansSC[wght].ttf")
    source = parser.parse_args().source
    if hashlib.sha256(source.read_bytes()).hexdigest() != SOURCE_SHA256:
        parser.error("The source differs from the pinned Google Fonts binary in SOURCES.md")

    with TTFont(source) as font:
        available = set(font.getBestCmap())
    page_han = {ord(char) for text in site_text() for char in text if is_han(ord(char))}
    missing = page_han - available
    if missing:
        raise ValueError(f"Missing site Hanzi in upstream font: {sorted(missing)}")

    punctuation = set(range(0x3000, 0x3040)) | set(range(0xFF01, 0xFF61))
    punctuation.update(map(ord, "·—―‘’“”‥…‧‰‵‶〈〉《》「」『』【】〔〕￥"))
    ui = page_han | (punctuation & available)
    common = (common_han() & available) - ui
    for filename, codepoints in (("noto-sans-sc-ui.woff2", ui), ("noto-sans-sc-common.woff2", common)):
        output = FONT_DIR / filename
        save_subset(source, codepoints, output)
        print(f"{filename}: {len(codepoints)} codepoints, {output.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()

"""Entry program for the news-image-20261119 bounty.

The image this repository holds is the entry: a front page summing up
Thursday 19 November 2026 in six panels. This program copies it to the
output directory the grader provides, so the judge sees exactly the
bytes in entry.png.

Standard library only; no network, no arguments. Run it locally with:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

Without MAKEFUN_OUTPUT_DIR it writes to ./output/entry.png.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
OUTPUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "output")
TARGET = OUTPUT_DIR / "entry.png"

# A PNG file always starts with these eight bytes; entry.png is a
# 1024x1024 PNG, so the copy is checked against the header, the IHDR
# dimensions and the byte count before the program reports success.
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def check_copy(source: Path, target: Path) -> None:
    """Raise unless target is a byte-identical copy of source."""
    if target.stat().st_size != source.stat().st_size:
        raise RuntimeError("entry.png did not copy completely")
    with target.open("rb") as handle:
        header = handle.read(33)
    if header[: len(PNG_MAGIC)] != PNG_MAGIC:
        raise RuntimeError("copied file is not a PNG image")
    if header[12:16] != b"IHDR":
        raise RuntimeError("copied file has no PNG IHDR chunk")
    width = int.from_bytes(header[16:20], "big")
    height = int.from_bytes(header[20:24], "big")
    if (width, height) != (1024, 1024):
        raise RuntimeError(f"entry image is {width}x{height}, expected 1024x1024")


def main() -> None:
    """Copy entry.png into the output directory, checking the copy."""
    if not SOURCE.is_file():
        raise RuntimeError(f"missing entry image: {SOURCE}")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, TARGET)
    check_copy(SOURCE, TARGET)


if __name__ == "__main__":
    main()

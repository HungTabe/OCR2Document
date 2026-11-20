#!/usr/bin/env python3
"""List images in a folder in natural order. Converts HEIC/WEBP/TIFF to JPG and
downsizes very large images (sips on macOS, Pillow elsewhere) into <folder>/.ocr_cache/."""
import re, subprocess, sys, shutil
from pathlib import Path

EXT = {".jpg", ".jpeg", ".png", ".heic", ".heif", ".webp", ".tif", ".tiff", ".bmp"}
MAX_SIDE = 2000

def nat(p):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", p.name)]

def prepare(src: Path, cache: Path) -> Path:
    needs_convert = src.suffix.lower() in {".heic", ".heif", ".webp", ".tif", ".tiff", ".bmp"}
    out = cache / (src.stem + ".jpg")
    if out.exists():
        return out
    if shutil.which("sips"):
        r = subprocess.run(["sips", "-s", "format", "jpeg", "-Z", str(MAX_SIDE), str(src), "--out", str(out)],
                           capture_output=True)
        if r.returncode == 0:
            return out
    try:
        from PIL import Image
        im = Image.open(src).convert("RGB")
        im.thumbnail((MAX_SIDE, MAX_SIDE))
        im.save(out, "JPEG", quality=90)
        return out
    except Exception:
        return src if not needs_convert else src

def main():
    folder = Path(sys.argv[1] if len(sys.argv) > 1 else ".").expanduser().resolve()
    if not folder.is_dir():
        sys.exit(f"Not a folder: {folder}")
    cache = folder / ".ocr_cache"
    cache.mkdir(exist_ok=True)
    imgs = sorted((p for p in folder.iterdir() if p.suffix.lower() in EXT and not p.name.startswith(".")), key=nat)
    if not imgs:
        sys.exit(f"No images found in {folder}")
    for p in imgs:
        print(prepare(p, cache))

if __name__ == "__main__":
    main()

from pathlib import Path
from typing import Any, Generator

import natsort

from app.utils.dirs import IMAGE_DIR


IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}

def is_image_path(path: Path) -> bool:
    return path.suffix.lower() in IMAGE_EXTS


def iter_item_dirs() -> Generator[Path, Any, None]:
    yield from (p for p in IMAGE_DIR.iterdir() if p.is_dir())


def iter_item_dir_image_paths(image_dir: Path):
    for f in natsort.natsorted(image_dir.iterdir()):
        if f.is_file() and is_image_path(f):
            yield f


if __name__ == "__main__":
    for item_dir in iter_item_dirs():
        for image in iter_item_dir_image_paths(item_dir):
            print(image)

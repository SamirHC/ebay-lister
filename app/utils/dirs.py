from pathlib import Path


IMAGE_DIR = Path("images").resolve()
OUT_DIR = Path("out").resolve()
LOG_DIR = OUT_DIR / "log"


def setup_directories():
    IMAGE_DIR.mkdir(exist_ok=True)
    OUT_DIR.mkdir(exist_ok=True)
    LOG_DIR.mkdir(exist_ok=True)


if __name__ == "__main__":
    print(IMAGE_DIR)
    setup_directories()

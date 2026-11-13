#!/usr/bin/env python3
"""Coolest-art-01 entry: copy the art beside this file to the output dir.

The art is a 1024x1024 JPEG (named entry.png, as the gate allows) of a
golden kintsugi dragon being repaired by tiny craftsmen, ukiyo-e style.
The program is deterministic: it copies the same bytes every run.
"""

import hashlib
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    src = HERE / "entry.png"
    dst = OUT / "entry.png"
    OUT.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    # The gate reads exactly these bytes; a short copy must never pass.
    assert dst.stat().st_size == src.stat().st_size, "short copy"
    # Verify the copy byte-for-byte; a corrupt copy must fail loudly.
    if _sha256(src) != _sha256(dst):
        raise SystemExit("SHA-256 mismatch: copied entry.png differs from source")


if __name__ == "__main__":
    main()

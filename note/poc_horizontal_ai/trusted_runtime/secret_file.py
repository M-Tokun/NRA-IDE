"""Load a bounded, non-symlink secret file supplied by the service launcher."""

from __future__ import annotations

import os
import stat
from pathlib import Path


def load_secret_key_file(path: Path) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise ValueError("key path must be a regular non-symlink file")
    size = path.stat().st_size
    if size < 32 or size > 4096:
        raise ValueError("key file size is outside the accepted range")
    if os.name != "nt":
        mode = stat.S_IMODE(path.stat().st_mode)
        if mode & 0o077:
            raise ValueError("key file must not be group/world accessible")
    key = path.read_bytes()
    if len(key) != size:
        raise ValueError("key file changed while reading")
    return key

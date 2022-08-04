import os
import pathlib
from collections import namedtuple

__BASE_DIR = pathlib.Path(__file__).parent.parent.parent

def resolve_root(*segments: str) -> str:
    """
    Resolves a relative path relative to the project root
    """

    abspath = __BASE_DIR / os.path.join(*segments)
    return str(abspath.resolve())

def root_directory(segments: list[str], create_missing=False) -> str:
    abspath = (__BASE_DIR / os.path.join(*segments)).resolve()
    if create_missing:
        abspath.mkdir(parents=True, exist_ok=True)

    return str(abspath)

def to_int(num, default = 0) -> int:
    try:
        return int(num)
    except:
        return default

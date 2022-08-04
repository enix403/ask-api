import pathlib
from collections import namedtuple

__BASE_DIR = pathlib.Path(__file__).parent.parent.parent

def resolve_root(relpath: str='.') -> str:
    """
    Resolves a relative path relative to the project root
    """
    abspath = __BASE_DIR / relpath
    return str(abspath.resolve())

def root_directory(rel_directory_path: str, create_missing=False) -> str:
    abspath = (__BASE_DIR / rel_directory_path).resolve()
    if create_missing:
        abspath.mkdir(parents=True, exist_ok=True)

    return str(abspath)

def to_int(num, default = 0) -> int:
    try:
        return int(num)
    except:
        return default

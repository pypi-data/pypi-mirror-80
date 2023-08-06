from pathlib import Path
from os import scandir, DirEntry, PathLike
from typing import Iterator, Union, AnyStr

# Return all file or symlink Path obj in `path`
def scan_dir(path: Union[AnyStr, PathLike]) -> Iterator[Path]:
    for entry in scan_dir_raw(path):
        yield Path(entry.path)


# Return all file or symlink os.DirEntry obj in `path`
def scan_dir_raw(path: Union[AnyStr, PathLike]) -> Iterator[DirEntry]:
    with scandir(path) as it:
        for entry in it:
            if entry.is_dir():
                for e in scan_dir_raw(Path(entry.path)):
                    yield e
            else:
                yield entry

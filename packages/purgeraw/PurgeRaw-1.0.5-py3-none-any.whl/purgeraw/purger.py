import os
from itertools import chain, filterfalse
from typing import List, Callable, Tuple

from toolz import curry, unique  # type: ignore


@curry
def __is_raw(raw_exts: List[str], path: str) -> bool:
    path_ext = os.path.splitext(path)[1].strip(".")
    return any((path_ext.lower() == ext.lower() for ext in raw_exts))


@curry
def purge(raw_exts: List[str],
          indexes: Callable[[str], List[Tuple[str, str]]],
          files: List[str]
          ) -> List[str]:
    print(f"There are {len(files)} files to process")

    raw_files: List[str] = list(filter(__is_raw(raw_exts), files))
    proc_files: List[str] = list(filterfalse(__is_raw(raw_exts), files))
    print(f"There are {len(raw_files)} raw files and {len(proc_files)} processed files")

    raw_indexes: List[Tuple[str, str]] = list(chain.from_iterable([indexes(raw_file) for raw_file in raw_files]))
    proc_indexes: List[str] = list(unique(
        map(lambda x: x[0], list(chain.from_iterable([indexes(proc_file) for proc_file in proc_files])))
    ))

    to_remove: List[str] = list([item[1] for item in raw_indexes if item[0] not in proc_indexes])
    to_remove.sort()

    print(f"Found {len(to_remove)} files to remove: {to_remove}")

    return to_remove

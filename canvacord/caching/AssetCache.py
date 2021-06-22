import pathlib
from contextlib import AbstractContextManager
from typing import Dict, MutableMapping

from canvacord.caching.types import PathType


class AssetCache(MutableMapping):
    def __init__(
        self, *, cache_dict: Dict, basepath: PathType, lock: AbstractContextManager
    ):
        self.cache_dict = cache_dict

        if isinstance(basepath, pathlib.Path):
            self.basepath = basepath
        else:
            self.basepath = pathlib.Path(basepath)

    def __setitem__(self, key: str, value) -> None:
        self.cache_dict[key] = value

    def __delitem__(self, key: str) -> None:
        del self.cache_dict[key]

    def __iter__(self):
        return self.cache_dict.__iter__()

    def __len__(self):
        return len(self.cache_dict)

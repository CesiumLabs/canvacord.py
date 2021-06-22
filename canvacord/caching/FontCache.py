import io
from contextlib import AbstractContextManager
from typing import Tuple

from PIL import ImageFont

from canvacord.caching.AssetCache import AssetCache
from canvacord.caching.types import FontCacheDict, PathType


class FontCache(AssetCache):
    def __init__(
        self,
        *,
        cache_dict: FontCacheDict = {},
        basepath: PathType,
    ):
        super().__init__(cache_dict=cache_dict, basepath=basepath)

    def __getitem__(self, key: Tuple[str, int]) -> ImageFont.FreeTypeFont:
        filename, size = key

        if filename in self.cache_dict:
            return ImageFont.truetype(io.BytesIO(self.cache_dict[filename]), size=size)

        with open(self.basepath / filename, "rb") as f:
            fontbytes = f.read()

        font = ImageFont.truetype(io.BytesIO(fontbytes), size=size)
        self.cache_dict[filename] = fontbytes

        return font

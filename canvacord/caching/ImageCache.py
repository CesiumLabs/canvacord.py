from contextlib import AbstractContextManager

from PIL import Image

from canvacord.caching.types import AssetCache, ImageCacheDict, PathType


class ImageCache(AssetCache):
    def __init__(
        self,
        *,
        cache_dict: ImageCacheDict = {},
        basepath: PathType,
    ):
        super().__init__(cache_dict=cache_dict, basepath=basepath)

    def __getitem__(self, key: str) -> Image.Image:
        if key in self.cache_dict:
            return self.cache_dict[key].copy()

        img = Image.open(self.basepath / key)
        self[key] = img

        return img.copy()

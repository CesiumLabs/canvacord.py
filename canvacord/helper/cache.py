"""Classes for caching purposes (images, fonts as of now)."""
import io
import os
from pathlib import Path
from typing import Optional

from PIL import Image, ImageFont

from canvacord.types import FontCacheDict, ImageCacheDict

IMAGE_ASSET_DIRECTORY = Path(os.path.abspath(__file__)).parent.parent / "assets/images/"
FONT_ASSET_DIRECTORY = Path(os.path.abspath(__file__)).parent.parent / "assets/fonts/"


class ImageCache:
    __slots__ = ("directory", "images_cache")
    
    def __init__(
        self,
        directory: Optional[str] = None,
        cache_dict: Optional[ImageCacheDict] = None,
    ) -> None:
        """
        Initialize class variables as well as load images from provided directory.

        :param directory: directory to load images from
        :rtype directory: Optional[str]
        :param cache_dict: premade dict of images
        :rtype cache_dict: Optional[ImageCacheDict]
        """
        self.directory = directory or IMAGE_ASSET_DIRECTORY
        self.images_cache = cache_dict or {}

        self.load_images(self.directory)

    def load_images(self, directory: str) -> ImageCacheDict:
        """
        Load images from provided directory.

        :param directory: dir to load images from
        :rtype: str
        :return: ImageCacheDict
        """
        images_cache: ImageCacheDict = {
            item: Image.open(directory / item).convert("RGBA")
            for item in os.listdir(directory)
            if item.endswith(".png")
        }

        self.images_cache = self.images_cache | images_cache

        return self.images_cache


    def __getitem__(self, key: str) -> Image.Image:
        return self.images_cache[key]

    def __setitem__(self, key: str, value: Image.Image) -> Image.Image:
        self.images_cache[key] = value

class FontCache:
    __slots__ = ("directory", "filelike")
    
    def __init__(
        self,
        directory: Optional[str] = None,
        cache_dict: Optional[FontCacheDict] = None,
    ) -> None:
        """
        Initialize class variables as well load fonts.

        Class to be used in the following way: FontCache[(font, size)]

        :param directory: directory to load fonts from
        :rtype directory: Optional[str]
        :param cache_dict: a premade fontcache dict
        :rtype cache_dict: Optional[dict]
        """
        self.directory = directory or FONT_ASSET_DIRECTORY
        self.filelike = cache_dict or {}

        self.load_fonts(self.directory)

    def load_fonts(self, directory: str) -> FontCacheDict:
        """
        Load fonts and cache them in BytesIO.

        :param directory: directory to load from
        :rtype directory: str
        :return: FontCacheDict
        """
        filelike: FontCacheDict = {}

        for item in os.listdir(directory):
            if item.endswith(".ttf"):
                f = open(directory / item, "rb")
                filelike[item] = io.BytesIO(f.read())
                f.close()

        self.filelike = self.filelike | filelike

        return self.filelike

    def __getitem__(self, key: tuple[str, int]) -> ImageFont.FreeTypeFont:
        return ImageFont.truetype(self.filelike[key[0]], size=key[1])

    def __setitem__(self, key, value):
        self.filelike[key] = value

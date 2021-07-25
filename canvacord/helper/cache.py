import os
from typing import Optional

from PIL import Image, ImageFont

from canvacord.types import ImageCacheDict, FontCacheDict

IMAGE_ASSET_DIRECTORY = r'C:\Users\scorz\Desktop\canvacord-py\canvacord\assets\images'
FONT_ASSET_DIRECTORY = r'C:\Users\scorz\Desktop\canvacord-py\canvacord\assets\fonts'

class ImageCache:
    def __init__(self, directory: Optional[str] = None) -> None:
        self.directory = directory or IMAGE_ASSET_DIRECTORY
        self.images_cache = {}

        self.load_images(self.directory)

    def load_images(self, directory: str) -> ImageCacheDict:
        images_cache: ImageCacheDict = {
            item: Image.open(directory + '/' + item).convert("RGBA")
            for item in os.listdir(directory)
            if item.endswith('.png')
        }

        self.images_cache = self.images_cache | images_cache

        return self.images_cache

class FontCache:
    def __init__(self, directory: Optional[str] = None) -> None:
        self.directory = directory or FONT_ASSET_DIRECTORY
        self.font_cache = {}

        self.load_fonts(self.directory)

    def load_fonts(self, directory: str, size: int = 10) -> FontCacheDict:
        font_cache: ImageCacheDict = {
            item: ImageFont.truetype(directory + '/' + item, size=size)
            for item in os.listdir(directory)
            if item.endswith('.ttf')
        }

        self.font_cache = self.font_cache | font_cache

        return self.font_cache

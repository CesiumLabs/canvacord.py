import os
from pathlib import Path
from typing import Optional

from PIL import Image

from canvacord.types import ImageCacheDict

IMAGE_ASSET_DIRECTORY = Path("canvacord/assets/images")


class ImageCache:
    def __init__(self, directory: Optional[Path] = None) -> None:
        self.directory = directory or IMAGE_ASSET_DIRECTORY
        self.images_cache = {}

        self.load_images(self.directory)

    def load_images(self, directory: Path) -> ImageCacheDict:
        images_cache: ImageCacheDict = {
            path: Image.open(directory / path).convert("RGBA")
            for path in os.listdir(directory)
            if path
        }

        self.images_cache.update(images_cache)

        return self.images_cache

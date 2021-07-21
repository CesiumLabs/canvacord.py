import os
import pathlib
from pathlib import Path
from typing import Optional

from PIL import Image

from canvacord.types import ImageCacheDict

IMAGE_ASSET_DIRECTORY = Path("canvacord/assets/images")


class ImageCache:
    def __init__(self, directory: Optional[Path] = None) -> None:
        self.directory = directory or IMAGE_ASSET_DIRECTORY

        # Loads all the images from the provided directory
        self.load_images(self.directory)

    def load_images(self, directory: Path) -> ImageCacheDict:
        images_cache: ImageCacheDict = {
            path: Image.open(directory / path).convert("RGBA")
            for path in os.listdir(directory)
            if path
        }

        try:
            self.images_cache = images_cache | self.images_cache
        except AttributeError:
            self.images_cache = images_cache

        return self.images_cache

    def load_image(self, image: Path) -> ImageCacheDict:
        file_name = "".join(str(image).split(".").pop(-1))
        self.images_cache[file_name] = Image.open(image)

import os
import pathlib
from pathlib import Path
from typing import Optional

from PIL import Image

IMAGE_ASSET_DIRECTORY = Path("canvacord/assets/images")


class ImageCache:
    def __init__(self, directory: Optional[Path] = None) -> None:
        self.directory = directory or IMAGE_ASSET_DIRECTORY

        # Loads all the images from the provided directory
        self.images: dict[str, Image.Image] = {
            path: Image.open(self.directory / path).convert("RGBA")
            for path in os.listdir(self.directory)
            if path
        }
        print(self.images)

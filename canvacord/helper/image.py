from pathlib import Path
from typing import Optional, Union
import asyncio

from PIL import Image

from .cache import ImageCache


class ImageHelper:
    def __init__(
        self,
        image_asset_directory: Optional[Path] = None,
        images_cache: Optional[ImageCache] = None,
    ) -> None:
        self._image_asset_directory = image_asset_directory

        # User can pass custom ImageClass object

        self._assets = (
            images_cache if images_cache else ImageCache(self._image_asset_directory)
        )

        self.images_cache = self._assets.images_cache

    @classmethod
    def resize(
        cls, img: Image.Image, size: Union[float, tuple[int, int]]
    ) -> Image.Image:
        if isinstance(size, float):
            return img.resize([int(size * s) for s in img.size])
        elif isinstance(size, tuple):
            return img.resize(size)

    @classmethod
    def _manipulate_image(
        cls,
        cords: tuple[int, int],
        background: Image.Image,
        foreground: Image.Image,
        back_size: Union[float, tuple[int, int]] = 1,
        back_transparency: int = 255,
        fore_size: Union[float, tuple[int, int]] = 1,
        fore_transparency: int = 255,
    ) -> Image.Image:
        if back_size != 1:
            background = cls.resize(background, back_size)
        if back_transparency != 255:
            background.putalpha(back_transparency)

        if fore_size != 1:
            foreground = cls.resize(foreground, fore_size)
        if fore_transparency != 255:
            foreground.putalpha(fore_transparency)

        background.paste(foreground, cords, mask=foreground)
        return background

    @classmethod
    async def manipulate_image(cls, *args, **kwargs) -> Image.Image:
        return await asyncio.to_thread(
            cls._manipulate_image,
            *args,
            **kwargs
        )

"""Image helpers for canvacord."""
import asyncio
from canvacord.types import FontCacheDict, ImageCacheDict
from typing import Optional, Union

from PIL import Image, ImageDraw, ImageFont

from .cache import ImageCache, FontCache


class ImageHelper:
    def __init__(
        self,
        image_asset_directory: Optional[str] = None,
        images_cache: Optional[ImageCache] = None,
        images_cache_dict: Optional[ImageCacheDict] = None,
        font_asset_directory: Optional[str] = None,
        fonts_cache: Optional[FontCache] = None,
        fonts_cache_dict: Optional[FontCacheDict] = None,
    ) -> None:
        """
        Initialize the ImageHelper class

        :param image_asset_directory: Path to cache images
        :type image_asset_directory: Optional[str]
        :param images_cache: Premade ImageCache object
        :type images_cache: Optional[ImageCache]
        :param images_cache_dict: Dictionary of the cached images
        :type images_cache_dict: Optional[ImageCacheDict]
        :param font_asset_directory: Path to cache fonts
        :type font_asset_directory: Optional[str]
        :param fonts_cache: Permade FontsCache object
        :type fonts_cache: Optional[FontCache]
        :param fonts_cache_dict: Dictonary of cached font bytes
        :type fonts_cache_dict: Optional[FontCacheDict]
        """
        # User can pass custom ImageClass object
        self.images_cache = (
            images_cache
            if images_cache
            else ImageCache(image_asset_directory, images_cache_dict)
        ).images_cache

        self.fonts_cache = (
            fonts_cache
            if fonts_cache
            else FontCache(font_asset_directory, fonts_cache_dict)
        )

    @classmethod
    def resize(
        cls, img: Image.Image, size: Union[float, tuple[int, int]]
    ) -> Image.Image:
        """Resize a image."""
        if isinstance(size, float):
            return img.resize([int(size * s) for s in img.size])
        elif isinstance(size, tuple):
            return img.resize(size)

    @classmethod
    def add_text(
        cls,
        img: Image.Image,
        text: str,
        cords: tuple[int, int, int],
        font: ImageFont.FreeTypeFont,
        fill: int = 255,
    ):
        """
        Add text onto an image.

        :param fill: fill for the text
        :rtype fill: int
        :param font: font of the text
        :rtype font: ImageFont.
        :param img: image for the text to be added onto
        :rtype img: Image.Image
        :param text: text to be added
        :rtype text: str
        :param cords: tuple[int, int, int]
        :rtype cords: Union[tuple, list]
        :return:
        """
        return ImageDraw.Draw(img).text(cords, text, fill, font)

    @classmethod
    async def manipulate_image(
        cls,
        cords: tuple[int, int],
        background: Image.Image,
        foreground: Image.Image,
        back_size: Union[float, tuple[int, int]] = 1,
        back_transparency: int = 255,
        fore_size: Union[float, tuple[int, int]] = 1,
        fore_transparency: int = 255,
    ) -> Image.Image:
        """
        A helper function to handle, manipulate images.

        :param cords: cords as to where to paste foreground onto background
        :rtype cords: tuple[int, int]
        :param background: background image
        :rtype cords: Image.Image
        :param foreground: foreground image
        :rtype cords: Image.Image
        :param back_size: size of background image
        :rtype cords: Union[float, tuple[int, int]]
        :param back_transparency: transparency of backgorund image
        :rtype cords: int
        :param fore_size: size of foreground image
        :rtype cords: Union[float, tuple[int, int]]
        :param fore_transparency: transparency of foreground image
        :rtype cords: int
        :return: Image.Image
        """

        def blocking_manipulate_image(**kwargs) -> Image.Image:
            if kwargs["back_size"] != 1:
                kwargs["background"] = cls.resize(
                    kwargs["background"], kwargs["back_size"]
                )
            if back_transparency != 255:
                kwargs["background"].putalpha(kwargs["back_transparency"])

            if kwargs["fore_size"] != 1:
                kwargs["foreground"] = cls.resize(
                    kwargs["foreground"], kwargs["fore_size"]
                )
            if fore_transparency != 255:
                kwargs["foreground"].putalpha(kwargs["fore_transparency"])

            kwargs["background"].paste(
                kwargs["foreground"], kwargs["cords"], mask=kwargs["foreground"]
            )
            return kwargs["background"]

        return await asyncio.to_thread(
            blocking_manipulate_image,
            cords=cords,
            background=background,
            foreground=foreground,
            back_size=back_size,
            back_transparency=back_transparency,
            fore_size=fore_size,
            fore_transparency=fore_transparency,
        )

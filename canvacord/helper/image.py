"""Image helpers for canvacord."""
from typing import Optional, Union

from PIL import Image, ImageDraw, ImageFont
from typing_extensions import ParamSpec, TypeVar

from canvacord.types import FontCacheDict, ImageCacheDict

from .cache import FontCache, ImageCache
from .utils import aioify

T = TypeVar("T")
P = ParamSpec("P")


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
        )

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
    @aioify
    def add_text(
        cls,
        img: Image.Image,
        text: str,
        cords: tuple[int, int, int],
        font: ImageFont.FreeTypeFont,
        fill: int = 255,
    ) -> Image.Image:
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
        """

        return ImageDraw.Draw(img).text(cords, text, fill, font)

    @classmethod
    @aioify
    def manipulate_image(
        cls,
        cords: tuple[int, int],
        background: Image.Image,
        foreground: Image.Image,
        back_size: Union[float, tuple[int, int]] = 1,
        back_transparency: int = 255,
        fore_size: Union[float, tuple[int, int]] = 1,
        fore_transparency: int = 255,
        rotate_back: int = 0,
        rotate_fore: int = 0,
    ) -> Image.Image:
        """
        A helper function to handle, manipulate images.

        :param rotate_back: how much background should be rotated in degrees
        :rtype rotate_back: int
        :param rotate_fore: how much foreground should be rotated in degrees
        :rtype rotate_fore: int
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
        if back_size != 1:
            background = cls.resize(background, back_size)
        if back_transparency != 255:
            background.putalpha(back_transparency)

        if fore_size != 1:
            foreground = cls.resize(foreground, fore_size)
        if fore_transparency != 255:
            foreground.putalpha(fore_transparency)

        if rotate_back:
            background.rotate(rotate_back)

        if rotate_fore:
            foreground.rotate(rotate_fore)

        background.paste(foreground, cords, mask=foreground)
        return background

import asyncio
import io
import pathlib
from typing import Any, Optional, Tuple, Type, Union

from PIL import Image, ImageDraw

from canvacord.base.Generator import Generator
from canvacord.caching import FontCache, ImageCache
from canvacord.caching.types import ImageType


DEFAULT_IMAGE_TYPE = "JPEG"


class BaseImageGenerator:
    def __new__(cls, *args, **kwargs) -> Any:
        self = super().__new__(cls)
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if getattr(attr, "__image_generator__", False):
                setattr(self, attr_name, Generator(attr, gen=self))

        return self

    def __init__(
        self,
        *,
        async_mode: bool = False,
        image_basepath: Union[str, pathlib.Path],
        font_basepath: Union[str, pathlib.Path],
        event_loop: Optional[asyncio.BaseEventLoop] = None,
        defualt_image_type: Optional[str] = DEFAULT_IMAGE_TYPE,
    ):
        self.event_loop = event_loop
        self.async_mode = async_mode
        self.default_image_type = defualt_image_type

        self.image_cache = ImageCache(
            basepath=image_basepath,
        )
        self.font_cache = FontCache(basepath=font_basepath)

        if async_mode and event_loop is None:
            self.event_loop = asyncio.get_event_loop()

    def image_converter(self, image: ImageType) -> Image.Image:
        # Convert to image
        if isinstance(image, str):
            image = Image.open(image)
        if isinstance(image, bytes):
            image = io.BytesIO(image)
        if isinstance(image, io.BytesIO):
            image = Image.open(image)
        if not isinstance(image, Image.Image):
            raise TypeError("Invalid image type provided")
        return image

    def image_to_bytesio(self, image: Image.Image, img_format: str = None):
        img_format = img_format or self.default_image_type
        b = io.BytesIO()
        image.save(b, format=img_format)
        b.seek(0)
        return b

    def paste(
        self,
        basename: str,
        image: ImageType,
        coords: Tuple[int, int],
        *,
        img_format: str = None,
        resize: Tuple[int, int] = None,
    ):
        img_format = img_format or self.default_image_type
        base = self.image_cache[basename]
        image = self.image_converter(image)

        if resize:
            image = image.resize(resize)
        base.paste(image, coords)

        return self.image_to_bytesio(base, img_format=img_format)

    def writetext(
        self,
        image: Union[Image.Image, str],
        *,
        fontname: str,
        size: int,
        center: Tuple[int, int],
        text: str,
        fill: Tuple[int, int, int] = (0, 0, 0),
        img_format: str = None,
        return_type: Type[Union[io.BytesIO, Image.Image, bytes]] = io.BytesIO,
    ) -> Union[io.BytesIO, Image.Image, bytes]:
        img_format = img_format or self.default_image_type

        if isinstance(image, str):
            image = self.image_cache[image]
        text = text.strip()

        font = self.font_cache[fontname, size]
        length = max([font.getlength(t) for t in text.split("\n")])
        height = size * len(text.split("\n"))
        xy = (center[0] - length // 2, center[1] - height // 2)

        draw = ImageDraw.Draw(image)
        draw.text(xy, text, fill=fill, font=font, align="center")

        if issubclass(return_type, Image.Image):
            return image

        if issubclass(return_type, io.BytesIO):
            return self.image_to_bytesio(image, img_format=img_format)

        if issubclass(return_type, bytes):
            return self.image_to_bytesio(image, img_format=img_format).read()

        raise RuntimeError(f"Unknown return_type {return_type.__name__}")

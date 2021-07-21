import asyncio

from PIL import Image

from canvacord.helper.image import ImageHelper
from canvacord.types import UserType
from canvacord.utils import _parse_user


class FunGenerator:
    def __init__(self) -> None:
        self.image_helper = ImageHelper()

    @_parse_user
    async def jail(self, user: UserType) -> Image.Image:
        avatar = await asyncio.to_thread(
            self.image_helper.manipulate_image,
            x=0,
            y=0,
            background=user,
            foreground=self.image_helper.images["jail.png"],
        )
        return avatar

    @_parse_user
    async def gay(self, user: UserType) -> Image.Image:
        avatar = await asyncio.to_thread(
            self.image_helper.manipulate_image,
            x=0,
            y=0,
            round=user,
            foreground=self.image_helper.images["gay.png"],
            fore_transparency=80,
        )
        return avatar

    @_parse_user
    async def jokeoverhead(self, user: UserType) -> Image.Image:
        avatar = await asyncio.to_thread(
            self.image_helper.manipulate_image,
            x=150,
            y=150,
            background=self.image_helper.images["jokeoverhead.png"],
            foreground=user,
            fore_size=0.35,
        )
        return avatar

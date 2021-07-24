import asyncio
import io

import aiohttp

from canvacord.helper.image import ImageHelper
from canvacord.helper.utils import args_parser, image_to_bytesio
from canvacord.types import UserType


class FunGenerator:
    def __init__(self, async_session: aiohttp.ClientSession) -> None:
        self.image_helper = ImageHelper()
        self.async_session = async_session

    @args_parser
    async def jail(self, user: UserType) -> io.BytesIO:
        avatar = await asyncio.to_thread(
            self.image_helper.manipulate_image,
            x=0,
            y=0,
            background=user,
            back_size=(512, 512),
            foreground=self.image_helper.images_cache["jail.png"],
            fore_size=(512, 512)
        )
        return image_to_bytesio(avatar)

    @args_parser
    async def gay(self, user: UserType) -> io.BytesIO:
        avatar = await asyncio.to_thread(
            self.image_helper.manipulate_image,
            x=0,
            y=0,
            background=user,
            back_size=(512, 512),
            foreground=self.image_helper.images_cache["gay.png"],
            fore_size=(512, 512),
            fore_transparency=80,
        )
        return image_to_bytesio(avatar)

    @args_parser
    async def jokeoverhead(self, user: UserType) -> io.BytesIO:
        avatar = await asyncio.to_thread(
            self.image_helper.manipulate_image,
            x=150,
            y=150,
            background=self.image_helper.images_cache["jokeoverhead.png"],
            foreground=user,
            fore_size=(95, 95),
        )
        return image_to_bytesio(avatar)

    @args_parser
    async def hitler(self, user: UserType) -> io.BytesIO:
        avatar = await asyncio.to_thread(
            self.image_helper.manipulate_image,
            x=40,
            y=28,
            background=self.image_helper.images_cache["hitler.png"],
            foreground=user,
            fore_size=(153, 153),
        )
        return image_to_bytesio(avatar)

    @args_parser
    async def spank(self, user1: UserType, user2: UserType) -> io.BytesIO:
        first_image = await asyncio.to_thread(
            self.image_helper.manipulate_image,
            x=460,
            y=100,
            background=self.image_helper.images_cache["spank.png"],
            foreground=user1,
            fore_size=(180, 180),
        )
        second_image = await asyncio.to_thread(
            self.image_helper.manipulate_image,
            x=710,
            y=480,
            background=first_image,
            foreground=user2,
            fore_size=(180, 180),
        )
        return image_to_bytesio(second_image)

    @args_parser
    async def wanted(self, user: UserType) -> io.BytesIO:
        avatar = await asyncio.to_thread(
            self.image_helper.manipulate_image,
            x=269,
            y=451,
            background=self.image_helper.images_cache["wanted.png"],
            foreground=user,
            fore_size=(395, 395),
        )
        return image_to_bytesio(avatar)

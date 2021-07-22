import asyncio
import io

import aiohttp

from canvacord.helper.image import ImageHelper
from canvacord.helper.utils import manipulation
from canvacord.types import UserType


class FunGenerator:
    def __init__(self, session: aiohttp.ClientSession) -> None:
        self.image_helper = ImageHelper()
        self._session = session

    @manipulation
    async def jail(self, user: UserType) -> io.BytesIO:
        avatar = await asyncio.to_thread(
            self.image_helper.manipulate_image,
            x=0,
            y=0,
            background=user,
            foreground=self.image_helper.images_cache["jail.png"],
        )
        return avatar

    @manipulation
    async def gay(self, user: UserType) -> io.BytesIO:
        avatar = await asyncio.to_thread(
            self.image_helper.manipulate_image,
            x=0,
            y=0,
            round=user,
            foreground=self.image_helper.images_cache["gay.png"],
            fore_transparency=80,
        )
        return avatar

    @manipulation
    async def jokeoverhead(self, user: UserType) -> io.BytesIO:
        avatar = await asyncio.to_thread(
            self.image_helper.manipulate_image,
            x=150,
            y=150,
            background=self.image_helper.images_cache["jokeoverhead.png"],
            foreground=user,
            fore_size=0.35,
        )
        return avatar

    @manipulation
    async def hitler(self, user: UserType) -> io.BytesIO:
        avatar = await asyncio.to_thread(
            self.image_helper.manipulate_image,
            x=40,
            y=28,
            background=self.image_helper.images_cache["hitler.png"],
            foreground=user,
            fore_size=0.6,
        )
        return avatar

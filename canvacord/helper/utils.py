import asyncio
import io
from functools import wraps
from typing import Callable, TypeVar

import aiohttp
import discord
from PIL import Image

from canvacord.types import UserType

_T = TypeVar("_T")


async def _user_parser(avatar: UserType, session: aiohttp.ClientSession) -> Image.Image:
    if isinstance(avatar, str):
        async with session.get(avatar) as response:
            new_avatar = Image.open(io.BytesIO(await response.read())).convert("RGBA")

    elif isinstance(avatar, (discord.Member, discord.User)):
        async with session.get(avatar.avatar_url) as response:
            new_avatar = Image.open(io.BytesIO(await response.read())).convert("RGBA")
    else:
        if not isinstance(avatar, Image.Image):
            raise Exception("User not found.")

    return new_avatar


def _image_to_bytesio(image: Image.Image, format: str = "PNG"):
    b = io.BytesIO()
    image.save(b, format=format)
    b.seek(0)
    return b


def manipulation(func: _T) -> _T:
    @wraps(func)
    async def wrapper(gen: type, avatar: UserType, *args, **kwargs):
        session = gen._session
        new_avatar = await _user_parser(avatar, session)

        image = await func(gen, new_avatar, *args, **kwargs)
        return _image_to_bytesio(image)

    return wrapper

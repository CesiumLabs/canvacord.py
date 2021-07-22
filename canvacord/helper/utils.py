import io
from functools import wraps
from typing import TypeVar

import httpx
import discord
from PIL import Image

from canvacord.types import UserType

_T = TypeVar("_T")


async def _user_parser(avatar: UserType, async_client: httpx.AsyncClient) -> Image.Image:
    if isinstance(avatar, str):
        avatar = Image.open(io.BytesIO((await async_client.get(avatar)).read()))

    elif isinstance(avatar, (discord.Member, discord.User)):
        async with async_client.get(avatar.avatar_url) as response:
            avatar = Image.open(io.BytesIO(await response.read())).convert("RGBA")

    elif not isinstance(avatar, Image.Image):
        raise Exception("User not found.")

    return avatar


def image_to_bytesio(image: Image.Image, format: str = "PNG"):
    b = io.BytesIO()
    image.save(b, format=format)
    b.seek(0)
    return b


def args_parser(func: _T) -> _T:
    @wraps(func)
    async def wrapper(gen: type, *args, **kwargs):
        async_client = gen.async_client
        args = list(args)

        for index, arg in enumerate(args):
            if isinstance(arg, UserType.__args__):
                args[index] = await _user_parser(arg, async_client)

        for key, value in kwargs.items():
            if isinstance(arg, UserType.__args__):
                kwargs[key] = await _user_parser(value, async_client)

        return await func(gen, *args, **kwargs)

    return wrapper

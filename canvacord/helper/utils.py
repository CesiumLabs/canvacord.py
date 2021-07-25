import io
import re
from typing import TYPE_CHECKING, TypeVar, Union

if TYPE_CHECKING:
    from canvacord.generator import FunGenerator, RankCard, WelcomeCard

from functools import wraps

import aiohttp
import discord
from PIL import Image

from canvacord.types import UserType

_T = TypeVar("_T")

URL_REGEX = re.compile(
    "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
)


async def _user_parser(
    avatar: UserType, async_session: aiohttp.ClientSession
) -> Image.Image:
    if isinstance(avatar, str):
        if URL_REGEX.findall(avatar):
            async with async_session.get(avatar) as resp:
                return Image.open(io.BytesIO(await resp.read()))
        return Image.open(avatar).convert("RGBA")

    elif isinstance(avatar, (discord.Member, discord.User)):
        return Image.open(io.BytesIO(await avatar.avatar_url.read()))

    elif isinstance(avatar, bytes):
        return Image.open(io.BytesIO(avatar))

    elif isinstance(avatar, io.BytesIO):
        return Image.open(avatar)

    elif not isinstance(avatar, Image.Image):
        raise TypeError("Not a valid UserType")

    return avatar


def image_to_bytesio(image: Image.Image, imgformat: str = "PNG") -> io.BytesIO:
    b = io.BytesIO()
    image.save(b, format=imgformat)
    b.seek(0)
    return b


def args_parser(func):
    @wraps(func)
    async def wrapper(
        gen: Union["FunGenerator", "RankCard", "WelcomeCard"], *args, **kwargs
    ):
        async_session = gen.async_session
        args = list(args)

        for index, arg in enumerate(args):
            if isinstance(arg, UserType.__args__):
                args[index] = await _user_parser(arg, async_session)

        for key, value in kwargs.items():
            if isinstance(arg, UserType.__args__):
                kwargs[key] = await _user_parser(value, async_session)

        return await func(gen, *args, **kwargs)

    return wrapper

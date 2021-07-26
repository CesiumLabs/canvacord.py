"""Helper functions for the image-method."""
import io
import re
from typing import TYPE_CHECKING, TypeVar
from typing_extensions import ParamSpec, Literal
from collections.abc import Callable, Awaitable

from canvacord.types import UserType
if TYPE_CHECKING:
    from canvacord.generator import FunGenerator, RankCard, WelcomeCard, BoostCard

from functools import wraps

import aiohttp
import discord
from PIL import Image

URL_REGEX = re.compile(
    "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
)

T = TypeVar("T")
P = ParamSpec("P")

async def _user_parser(
    avatar: UserType, async_session: aiohttp.ClientSession
) -> Image.Image:
    """
    Parse the input user provides for the avatar argument.

    :param avatar: avatar to parse
    :rtype avatar: UserType
    :param async_session: aiohttp session to be used
    :rtype async_session: aiohttp.ClientSession
    :return:
    """
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
    """
    Convert an image to bytesio.

    :param image: Image to convert to bytesio.
    :rtype image: Image.Image
    :param imgformat: Format for the image, default, PNG.
    :rtype imgformat: str
    :return: io.BytesIO
    """
    b = io.BytesIO()
    image.save(b, format=imgformat)
    b.seek(0)
    return b


def args_parser(func: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]:
    @wraps(func)
    async def wrapper(
        gen: Literal['FunGenerator', 'RankCard', 'WelcomeCard', 'BoostCard'], *args: P.args, **kwargs: P.kwargs
    ) -> T:
        """
        Call _user_parser() func on all arguments annotated with the UserType type.

        :param gen: gen which must include the async_session
        :rtype gen: Literal['FunGenerator', 'RankCard', 'WelcomeCard', 'BoostCard']
        :param args: arguments
        :param kwargs: keyword arguments
        :return: T
        """
        async_session = gen.async_session
        arguments = list(args)

        for index, arg in enumerate(arguments):
            if isinstance(arg, UserType.__args__):
                arguments[index] = await _user_parser(arg, async_session)

        for key, value in kwargs.items():
            if isinstance(arg, UserType.__args__):
                kwargs[key] = await _user_parser(value, async_session)

        return await func(gen, *arguments, **kwargs)
    return wrapper

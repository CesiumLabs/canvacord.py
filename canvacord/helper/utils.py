import io
from functools import wraps
from typing import TypeVar

import aiohttp
import discord
from PIL import Image

from canvacord.types import UserType

_T = TypeVar("_T")


def _parse_user(f: _T) -> _T:
    @wraps(f)
    async def wrapper(generator: type, avatar: UserType, *args, **kwargs):
        ses = aiohttp.ClientSession()

        if isinstance(avatar, str):
            async with ses.get(avatar) as response:
                avatar = Image.open(io.BytesIO(await response.read())).convert("RGBA")

        elif isinstance(avatar, (discord.Member, discord.User)):
            async with ses.get(avatar.avatar_url) as response:
                avatar = Image.open(io.BytesIO(await response.read())).convert("RGBA")
        else:
            if not isinstance(avatar, Image.Image):
                raise Exception("User not found.")

        await ses.close()
        return await f(generator, avatar, *args, **kwargs)

    return wrapper

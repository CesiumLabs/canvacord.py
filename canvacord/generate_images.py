from PIL import Image
import discord
import typing
import os
import aiohttp
import asyncio
import io

class _Assets:
    images: dict[str, Image.Image] = {path: Image.open(f'assets/{path}').convert('RGBA') for path in os.listdir('assets')}

    def resize(self, img: Image.Image, size: float) -> Image.Image:
        return img.resize([int(size * s) for s in img.size])

    def manipulate_image(
            self,
            x: int,
            y: int,
            background: Image.Image,
            foreground: Image.Image,
            back_size: float = 1,
            back_transparency: int = 255,
            fore_size: float = 1,
            fore_transparency: int = 255,
    ) -> Image.Image:
        if back_size != 1:
            background = self.resize(background, back_size)
        if back_transparency != 255:
            background.putalpha(back_transparency)

        if fore_size != 1:
            foreground = self.resize(foreground, fore_size)
        if fore_transparency != 255:
            foreground.putalpha(fore_transparency)

        background.paste(foreground, (x, y), mask=foreground)
        return background

assets = _Assets()
UserType = typing.Union[discord.Member, discord.User, str, Image.Image]

def _parse_user(f):
    async def wrapper(*args, **kwargs):
        ses = aiohttp.ClientSession()
        l_args = list(args)
        avatar = l_args[0]

        if isinstance(avatar, str):
            async with ses.get(avatar) as response:
                avatar = Image.open(io.BytesIO(await response.read())).convert('RGBA')

        elif isinstance(avatar, (discord.Member, discord.User)):
            async with ses.get(avatar.avatar_url) as response:
                avatar = Image.open(io.BytesIO(await response.read())).convert('RGBA')
        else:
            if not isinstance(avatar, Image.Image):
                raise Exception('User not found.')

        l_args[0] = avatar
        await ses.close()
        return await f(*l_args, **kwargs)
    return wrapper

@_parse_user
async def jail(user: UserType) -> Image.Image:
    avatar = await asyncio.to_thread(assets.manipulate_image, x=0, y=0, background=user, foreground=assets.images['jail.png'])
    return avatar

@_parse_user
async def gay(user: UserType) -> Image.Image:
    avatar = await asyncio.to_thread(
        assets.manipulate_image,
        x=0,
        y=0,
        background=user,
        foreground=assets.images['gay.png'],
        fore_transparency=80
    )
    return avatar

@_parse_user
async def jokeoverhead(user: UserType) -> Image.Image:
    avatar = await asyncio.to_thread(
        assets.manipulate_image,
        x=150,
        y=150,
        background=assets.images['jokeoverhead.png'],
        foreground=user,
        fore_size=.35
    )
    return avatar

loop = asyncio.get_event_loop()
loop.run_until_complete(jokeoverhead('https://cdn.discordapp.com/avatars/438741869107871775/d8383a718f0574e7dc6670e951a6ba4b.png?size=256')).save('./joke.png')

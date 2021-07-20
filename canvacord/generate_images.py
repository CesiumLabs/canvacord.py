from PIL import Image
import requests
import discord
import typing
import os

class _Assets:
    gay: Image.Image
    jail: Image.Image

    def __init__(self):
        vars(self).update({path.split('.')[0]: Image.open(f'assets/{path}').convert('RGBA') for path in os.listdir('assets')})

assets = _Assets()
UserType = typing.Union[discord.Member, discord.User, str, Image.Image]

def _parse_user(user: UserType):
    if isinstance(user, str):
        avatar_url = Image.open(requests.get(user, stream=True).raw).convert('RGBA')
    elif isinstance(user, (discord.Member, discord.User)):
        avatar_url = Image.open(requests.get(user.avatar_url, stream=True).raw).convert('RGBA')
    else:
        if not isinstance(user, Image.Image):
            raise Exception('User not found.')
    return avatar_url

def jail(user: UserType) -> Image.Image:
    avatar = _parse_user(user)
    avatar.paste(assets.jail, (0, 0), mask=assets.jail)
    return avatar

def gay(user: UserType, transparency: int = 80) -> Image.Image:
    avatar = _parse_user(user)
    assets.gay.putalpha(transparency)
    avatar.paste(assets.gay, (0, 0), mask=assets.gay)
    return avatar

gay('https://cdn.discordapp.com/avatars/438741869107871775/d8383a718f0574e7dc6670e951a6ba4b.png?size=256').save('./gay.png')
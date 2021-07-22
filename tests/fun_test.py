import pathlib
import sys
from typing import Callable

import aiohttp

sys.path.append(".")

import pytest
from PIL import Image

from canvacord import Canvacord

USER_AV = "https://cdn.discordapp.com/avatars/438741869107871775/d8383a718f0574e7dc6670e951a6ba4b.png?size=256"


async def fun_tester(method: Callable, image_path: pathlib.Path, *args):
    image = await method(*args)
    first_image = Image.open(image)
    second_image = Image.open(image_path)
    return first_image, second_image


@pytest.mark.asyncio
async def test_jail():
    async with aiohttp.ClientSession() as session:
        canvacord = Canvacord(session)
        first_image, second_image = await fun_tester(
            canvacord.fun.jail, "tests/assets/jail.png", USER_AV
        )
    assert first_image == second_image


@pytest.mark.asyncio
async def test_hitler():
    async with aiohttp.ClientSession() as session:
        canvacord = Canvacord(session)
        first_image, second_image = await fun_tester(
            canvacord.fun.hitler, "tests/assets/hitler.png", USER_AV
        )
    assert first_image == second_image


@pytest.mark.asyncio
async def test_spank():
    async with aiohttp.ClientSession() as session:
        canvacord = Canvacord(session)
        first_image, second_image = await fun_tester(
            canvacord.fun.spank, "tests/assets/spank.png", USER_AV, USER_AV
        )

    assert first_image == second_image

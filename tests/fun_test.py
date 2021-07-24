import io
import pathlib
import sys
from typing import Any, Callable

import aiohttp

sys.path.append(".")

import pytest
from PIL import Image

from canvacord import Canvacord

USER_AV = "canvacord/assets/images/user_av.png"


async def fun_tester(
    method: Callable[[Any], io.BytesIO], image_path: pathlib.Path, *args
):
    image = await method(*args)
    first_image = Image.open(image)
    second_image = Image.open(image_path)
    return first_image, second_image


@pytest.mark.asyncio
async def test_jail():
    async with aiohttp.ClientSession() as async_session:
        canvacord = Canvacord(async_session)
        first_image, second_image = await fun_tester(
            canvacord.fun.jail, "tests/assets/jail.png", USER_AV
        )
    assert first_image == second_image


@pytest.mark.asyncio
async def test_hitler():
    async with aiohttp.ClientSession() as async_session:
        canvacord = Canvacord(async_session)
        first_image, second_image = await fun_tester(
            canvacord.fun.hitler, "tests/assets/hitler.png", USER_AV
        )
    assert first_image == second_image


@pytest.mark.asyncio
async def test_spank():
    async with aiohttp.ClientSession() as async_session:
        canvacord = Canvacord(async_session)
        first_image, second_image = await fun_tester(
            canvacord.fun.spank, "tests/assets/spank.png", USER_AV, USER_AV
        )

    assert first_image == second_image


@pytest.mark.asyncio
async def test_wanted():
    async with aiohttp.ClientSession() as async_session:
        canvacord = Canvacord(async_session)
        first_image, second_image = await fun_tester(
            canvacord.fun.wanted, "tests/assets/wanted.png", USER_AV
        )

    assert first_image == second_image


@pytest.mark.asyncio
async def test_gay():
    async with aiohttp.ClientSession() as async_session:
        canvacord = Canvacord(async_session)
        first_image, second_image = await fun_tester(
            canvacord.fun.gay, "tests/assets/gay.png", USER_AV
        )

    assert first_image == second_image

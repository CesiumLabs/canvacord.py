import io
import pathlib
import sys
from typing import Any, Callable

import httpx

sys.path.append(".")

import pytest
from PIL import Image

from canvacord import Canvacord

USER_AV = "https://cdn.discordapp.com/avatars/438741869107871775/d8383a718f0574e7dc6670e951a6ba4b.png?size=256"


async def fun_tester(
    method: Callable[[Any], io.BytesIO], image_path: pathlib.Path, *args
):
    image = await method(*args)
    first_image = Image.open(image)
    second_image = Image.open(image_path)
    return first_image, second_image


@pytest.mark.asyncio
async def test_jail():
    async with httpx.AsyncClient() as async_client:
        canvacord = Canvacord(async_client)
        first_image, second_image = await fun_tester(
            canvacord.fun.jail, "tests/assets/jail.png", USER_AV
        )
    assert first_image == second_image


@pytest.mark.asyncio
async def test_hitler():
    async with httpx.AsyncClient() as async_client:
        canvacord = Canvacord(async_client)
        first_image, second_image = await fun_tester(
            canvacord.fun.hitler, "tests/assets/hitler.png", USER_AV
        )
    assert first_image == second_image


@pytest.mark.asyncio
async def test_spank():
    async with httpx.AsyncClient() as async_client:
        canvacord = Canvacord(async_client)
        first_image, second_image = await fun_tester(
            canvacord.fun.spank, "tests/assets/spank.png", USER_AV, USER_AV
        )

    assert first_image == second_image


@pytest.mark.asyncio
async def test_wanted():
    async with httpx.AsyncClient() as async_client:
        canvacord = Canvacord(async_client)
        first_image, second_image = await fun_tester(
            canvacord.fun.wanted, "tests/assets/wanted.png", USER_AV
        )

    assert first_image == second_image


@pytest.mark.asyncio
async def test_gay():
    async with httpx.AsyncClient() as async_client:
        canvacord = Canvacord(async_client)
        first_image, second_image = await fun_tester(
            canvacord.fun.gay, "tests/assets/gay.png", USER_AV
        )

    assert first_image == second_image

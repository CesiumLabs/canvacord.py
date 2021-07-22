import sys
import aiohttp

sys.path.append(".")

import pytest
from PIL import Image

from canvacord import Canvacord


@pytest.mark.asyncio
async def test_jail():
    async with aiohttp.ClientSession() as session:
        canvacord = Canvacord(session)
        image = await canvacord.fun.jail(
            "https://cdn.discordapp.com/avatars/438741869107871775/d8383a718f0574e7dc6670e951a6ba4b.png?size=256"
        )
        frist_image = Image.open(image)
        second_image = Image.open("tests/assets/jail.png")

        assert frist_image == second_image
        
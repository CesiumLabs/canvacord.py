from typing import Optional

import aiohttp

from canvacord.generator import FunGenerator


class Canvacord:
    def __init__(self, async_client: Optional[aiohttp.ClientSession] = None) -> None:
        self._async_client = async_client or aiohttp.ClientSession()
        self._fun_client = FunGenerator(self._async_client)

    @property
    def fun(self) -> FunGenerator:
        return self._fun_client

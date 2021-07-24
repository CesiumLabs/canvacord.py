from typing import Optional

import aiohttp

from canvacord.generator import FunGenerator


class Canvacord:
    def __init__(self, async_session: Optional[aiohttp.ClientSession] = None) -> None:
        self.async_session = async_session or aiohttp.ClientSession()
        self._fun_client = FunGenerator(self.async_session)

    @property
    def fun(self) -> FunGenerator:
        return self._fun_client

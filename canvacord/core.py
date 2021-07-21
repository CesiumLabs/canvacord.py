from typing import Optional

import aiohttp

from canvacord.generator.fun import FunGenerator


class Canvacord:
    def __init__(self, session: Optional[aiohttp.ClientSession] = None) -> None:
        self._session = session or aiohttp.ClientSession()
        self._fun_client = FunGenerator(self._session)

    @property
    def fun(self) -> FunGenerator:
        return self._fun_client

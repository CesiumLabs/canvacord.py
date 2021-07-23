from typing import Optional

import httpx

from canvacord.generator import FunGenerator


class Canvacord:
    def __init__(self, async_client: Optional[httpx.AsyncClient] = None) -> None:
        self._async_client = async_client or httpx.AsyncClient()
        self._fun_client = FunGenerator(self._async_client)

    @property
    def fun(self) -> FunGenerator:
        return self._fun_client

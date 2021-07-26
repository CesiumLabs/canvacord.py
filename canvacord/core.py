"""The main file with all methods for the user to use."""
from typing import Optional

import aiohttp

from canvacord.generator import FunGenerator


class Canvacord:
    def __init__(self, async_session: Optional[aiohttp.ClientSession] = None) -> None:
        """
        The brains of the operation. Initialize class variables.

        :param async_session: aiohttp session, if none, create one which must be closed.
        :rtype async_session: Optional[aiohttp.ClientSession]
        """
        self.async_session = async_session or aiohttp.ClientSession()
        self._fun_client = FunGenerator(self.async_session)

    @property
    def fun(self) -> FunGenerator:
        return self._fun_client

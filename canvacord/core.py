"""The main file with all methods for the user to use."""
from typing import Optional

import aiohttp

from canvacord.generator import FunGenerator, BoostCard
from canvacord.helper.image import ImageHelper


class Canvacord:
    def __init__(
        self,
        async_session: Optional[aiohttp.ClientSession] = None,
        image_helper: Optional[ImageHelper] = None,
    ) -> None:
        """
        The brains of the operation. Initialize class variables.

        :param async_session: aiohttp session, if `None`, one is cretaed which must be closed
        :type async_session: Optional[aiohttp.ClientSession]
        :param image_helper: Permade ImageHelper object, defaults to None
        :type image_helper: Optional[ImageHelper]
        """
        self.async_session = async_session or aiohttp.ClientSession()

        self.image_helper = image_helper if image_helper else ImageHelper()

        self._fun_client = FunGenerator(self.async_session, self.image_helper)

    @property
    def fun(self) -> FunGenerator:
        return self._fun_client

    def boost_card(self, boosts: int, booster_name: str) -> BoostCard:
        return BoostCard(self.async_session, self.image_helper, boosts=boosts, booster_name=booster_name)

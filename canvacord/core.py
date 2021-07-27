"""The main file with all methods for the user to use."""
from canvacord.helper.cache import FontCache, ImageCache
from canvacord.helper.image import ImageHelper
from typing import Optional

import aiohttp

from canvacord.generator import FunGenerator


class Canvacord:
    def __init__(
        self,
        async_session: Optional[aiohttp.ClientSession] = None,
        image_helper: Optional[ImageHelper] = None,
    ) -> None:
        """
        The brains of the opeartion. Initialize class variables

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

import abc
import io
from re import A
from typing import Optional

import aiohttp

from canvacord.helper.image import ImageHelper
from canvacord.helper.utils import aioify


class BaseGenerator(abc.ABC):
    def __init__(
        self,
        async_session: Optional[aiohttp.ClientSession],
        image_helper: Optional[ImageHelper] = None,
    ):
        """
        Initialize class variables.

        :param async_session: async session to be used
        :rtype async_session: aiohttp.ClientSession
        :param image_helper: image helper
        :rtype image_helper: ImageHelper
        """
        self.async_session = async_session or aiohttp.ClientSession()
        self.image_helper = image_helper or ImageHelper()


class CardGenerator(BaseGenerator):
    @abc.abstractmethod
    @aioify
    def create(self) -> io.BytesIO:
        pass

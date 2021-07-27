import aiohttp

from canvacord.helper.image import ImageHelper


class BoostCard:
    def __init__(
        self, async_session: aiohttp.ClientSession, image_helper: ImageHelper, boosts: int, booster_name: str
    ) -> None:
        """
        Initialize class variables.

        :param async_session: async session to be used
        :rtype async_session: aiohttp.ClientSession
        :param image_helper: image helper
        :rtype image_helper: ImageHelper
        :param boosts: number of boosts a server has
        :rtype boosts: int
        :param booster_name: name of the booster including discriminator
        :rtype booster_name: str
        """
        self.image_helper = image_helper
        self.async_session = async_session
        self.boosts = boosts
        self.booster_name = booster_name

        self.create()

    def create(self):
        """TODO: Create the image."""

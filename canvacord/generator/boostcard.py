from canvacord.generator.base import CardGenerator
from canvacord.helper.utils import aioify


class BoostCard(CardGenerator):
    @aioify
    def create(self, boosts: int, booster_name: str):
        """TODO: Create the image."""

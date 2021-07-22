import io
from typing import Union

import discord
from PIL import Image

UserType = Union[discord.Member, discord.User, str, Image.Image, bytes, io.BytesIO]
ImageCacheDict = dict[str, Image.Image]

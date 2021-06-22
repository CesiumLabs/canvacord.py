import io
import pathlib
from typing import Dict, Union

from PIL import Image

ImageCacheDict = Dict[str, Image.Image]
FontCacheDict = Dict[str, bytes]
ImageType = Union[Image.Image, bytes, io.BytesIO, str]
PathType = Union[str, pathlib.Path]

# Canvacord.py

A Python implementation of the [canvacord](https://github.com/DevSnowflake/canvacord)
library.

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Usage

To install the library (not on pypi yet), run:
```py
# windows
py -m pip install canvacord

# macos/linux
python3 -m pip canvacord
```

For the dev version do:

```python
git clone https://github.com/DevSnowflake/canvacord-py
cd canvacord-py
```

# Quick Start

```python
from canvacord.core import Canvacord
import io

async def jokeoverhead(avatar: str) -> io.BytesIO:
    cc = Canvacord()
    data = await cc.fun.jokeoverhead(avatar)
    cc.async_session.close() # close the session
    return data
```

Or, if you already have an aiohttp session:

```python
from canvacord.core import Canvacord
import io
import aiohttp

async def jokeoverhead(avatar: str) -> io.BytesIO:
    async with aiohttp.ClientSession() as session:
        cc = Canvacord(session)
        data = await cc.fun.jokeoverhead(avatar)
        # cc.async_session.close() no need to close since it's a context manager
        return data
```

# FAQ

### I would like to contribute, how do I help?
- You may open an issue or find an issue, fork the repo, make changes and submit an PR request. Please ensure your code 
  follows `CONTRIBUTING.md`
  
### I am getting unclosed aiohttp sessions
- If you are only seeing the warning, please access the async_session attr from Canvacord and close it yourself, as seen 
in quick start. You may also use a context manager, as well seen in quick-start.
  

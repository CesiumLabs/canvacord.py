import functools
from typing import Any, TypeVar

from canvacord.base import BaseImageGenerator

_T = TypeVar("_T")


def generator(func: _T) -> _T:
    func.__image_generator__ = True
    return func


class Generator:
    def __init__(self, func, *, gen: BaseImageGenerator):
        self.func = func
        self.gen = gen

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        if self.gen.async_mode:
            return self.gen.event_loop.run_in_executor(
                self.gen.executor, functools.partial(self.func, *args, **kwargs)
            )
        return self.func(*args, **kwargs)

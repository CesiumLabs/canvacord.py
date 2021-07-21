from canvacord.generator.fun import FunGenerator


class Canvacord:
    def __init__(self):
        self._fun_client = FunGenerator()

    @property
    def fun(self) -> FunGenerator:
        return self._fun_client

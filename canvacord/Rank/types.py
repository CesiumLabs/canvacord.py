from dataclasses import dataclass


@dataclass
class CanvaUser:
    current_xp: int
    required_xp: int
    level: int
    username: str
    discriminator: str

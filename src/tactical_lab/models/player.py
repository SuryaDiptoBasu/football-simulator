from dataclasses import dataclass


@dataclass
class Player:
    id: int
    name: str
    position: str

    pace: int
    passing: int
    shooting: int
    defending: int
    stamina: int
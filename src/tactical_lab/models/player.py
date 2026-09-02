from dataclasses import dataclass
from enum import Enum


class Position(Enum):
    GK = "GK"

    LB = "LB"
    CB = "CB"
    RB = "RB"

    DM = "DM"
    CM = "CM"
    AM = "AM"

    LW = "LW"
    RW = "RW"
    ST = "ST"


@dataclass
class Player:
    id: int
    name: str
    position: Position

    pace: int
    passing: int
    shooting: int
    defending: int
    stamina: int

    dribbling: int = 0
    physical: int = 0
    overall: int = 0
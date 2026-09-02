from dataclasses import dataclass, field

from tactical_lab.models.player import Player


@dataclass
class Tactics:
    formation: str = "4-3-3"

    pressing: str = "medium"
    defensive_line: str = "medium"

    passing_style: str = "mixed"
    attack_width: str = "balanced"

    counter_attack: bool = False


@dataclass
class Team:
    id: int
    name: str

    players: list[Player] = field(default_factory=list)

    tactics: Tactics = field(default_factory=Tactics)
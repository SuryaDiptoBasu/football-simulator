from dataclasses import dataclass, field


@dataclass
class TeamMatchStats:
    passes: int = 0
    interceptions: int = 0
    progressions: int = 0
    shots: int = 0
    goals: int = 0

    possession_ticks: int = 0


@dataclass
class MatchStats:
    home: TeamMatchStats = field(
        default_factory=TeamMatchStats
    )

    away: TeamMatchStats = field(
        default_factory=TeamMatchStats
    )
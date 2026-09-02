from dataclasses import dataclass, field

from tactical_lab.models.team import Team
from tactical_lab.models.field import BallZone
from tactical_lab.models.stats import MatchStats

@dataclass
class MatchState:
    home_team: Team
    away_team: Team

    home_score: int = 0
    away_score: int = 0

    possession_team_id: int | None = None
    ball_player_id: int | None = None

    ball_zone: BallZone = BallZone.DEFENSIVE

    #is_counter_attack: bool = False
    #counter_attack_actions_remaining: int = 0

    stats: MatchStats = field(
        default_factory=MatchStats
    )

    current_time: int = 0
    finished: bool = False
    
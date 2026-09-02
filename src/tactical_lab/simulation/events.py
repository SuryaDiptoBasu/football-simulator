from dataclasses import dataclass
from enum import Enum
from typing import Any


class EventType(str, Enum):
    MATCH_STARTED = "MATCH_STARTED"
    MATCH_ENDED = "MATCH_ENDED"

    POSSESSION_CHANGED = "POSSESSION_CHANGED"
    #COUNTER_ATTACK_STARTED = "COUNTER_ATTACK_STARTED"

    PASS = "PASS"
    INTERCEPTION = "INTERCEPTION"
    PROGRESSION = "PROGRESSION"
    SHOT = "SHOT"
    GOAL = "GOAL"


@dataclass
class MatchEvent:
    timestamp: int
    event_type: EventType

    team_id: int | None = None
    player_id: int | None = None

    data: dict[str, Any] | None = None
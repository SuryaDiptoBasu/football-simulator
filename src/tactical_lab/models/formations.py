from tactical_lab.models.player import Position


FORMATION_POSITIONS = {
    "3-4-3": [
        Position.GK,
        Position.CB,
        Position.CB,
        Position.CB,
        Position.LB,
        Position.CM,
        Position.CM,
        Position.RB,
        Position.LW,
        Position.ST,
        Position.RW,
    ],

    "4-3-3": [
        Position.GK,
        Position.LB,
        Position.CB,
        Position.CB,
        Position.RB,
        Position.CM,
        Position.CM,
        Position.DM,
        Position.LW,
        Position.ST,
        Position.RW,
    ],

    "3-5-2": [
        Position.GK,
        Position.CB,
        Position.CB,
        Position.CB,
        Position.LW,
        Position.CM,
        Position.DM,
        Position.CM,
        Position.RW,
        Position.ST,
        Position.ST,
    ],

    "4-5-1": [
        Position.GK,
        Position.LB,
        Position.CB,
        Position.CB,
        Position.RB,
        Position.LW,
        Position.CM,
        Position.DM,
        Position.CM,
        Position.RW,
        Position.ST,
    ],

    "4-2-3-1": [
        Position.GK,
        Position.LB,
        Position.CB,
        Position.CB,
        Position.RB,
        Position.DM,
        Position.DM,
        Position.LW,
        Position.AM,
        Position.RW,
        Position.ST,
    ],

    "4-4-2": [
        Position.GK,
        Position.LB,
        Position.CB,
        Position.CB,
        Position.RB,
        Position.LW,
        Position.CM,
        Position.CM,
        Position.RW,
        Position.ST,
        Position.ST,
    ],

    "5-4-1": [
        Position.GK,
        Position.LB,
        Position.CB,
        Position.CB,
        Position.CB,
        Position.RB,
        Position.LW,
        Position.CM,
        Position.CM,
        Position.RW,
        Position.ST,
    ],
}


POSITION_PASSING_OPTIONS = {
    Position.LB: {
        Position.LB,
        Position.CB,
        Position.DM,
        Position.CM,
        Position.LW,
    },
    Position.CB: {
        Position.LB,
        Position.CB,
        Position.RB,
        Position.DM,
        Position.CM,
    },
    Position.RB: {
        Position.CB,
        Position.RB,
        Position.DM,
        Position.CM,
        Position.RW,
    },
    Position.DM: {
        Position.LB,
        Position.CB,
        Position.RB,
        Position.DM,
        Position.CM,
        Position.AM,
        Position.LW,
        Position.RW,
    },
    Position.CM: {
        Position.DM,
        Position.CM,
        Position.AM,
        Position.LW,
        Position.RW,
        Position.ST,
    },
    Position.AM: {
        Position.CM,
        Position.DM,
        Position.LW,
        Position.RW,
        Position.ST,
    },
    Position.LW: {
        Position.LB,
        Position.CM,
        Position.AM,
        Position.RW,
        Position.ST,
    },
    Position.RW: {
        Position.RB,
        Position.CM,
        Position.AM,
        Position.LW,
        Position.ST,
    },
    Position.ST: {
        Position.CM,
        Position.AM,
        Position.LW,
        Position.RW,
        Position.ST,
    },
}


POSITION_PROGRESSION_OPTIONS = {
    Position.LB: {Position.DM, Position.CM, Position.LW},
    Position.CB: {Position.DM, Position.CM},
    Position.RB: {Position.DM, Position.CM, Position.RW},
    Position.DM: {
        Position.CM,
        Position.AM,
        Position.LW,
        Position.RW,
    },
    Position.CM: {
        Position.AM,
        Position.LW,
        Position.RW,
        Position.ST,
    },
    Position.AM: {Position.LW, Position.RW, Position.ST},
    Position.LW: {Position.AM, Position.ST},
    Position.RW: {Position.AM, Position.ST},
}


def get_formation_positions(formation: str) -> list[Position]:
    if formation not in FORMATION_POSITIONS:
        raise ValueError(
            f"Unsupported formation: {formation}"
        )

    return FORMATION_POSITIONS[formation].copy()


def get_passing_positions(position: Position) -> set[Position]:
    return POSITION_PASSING_OPTIONS.get(position, set())


def get_progression_positions(position: Position) -> set[Position]:
    return POSITION_PROGRESSION_OPTIONS.get(position, set())
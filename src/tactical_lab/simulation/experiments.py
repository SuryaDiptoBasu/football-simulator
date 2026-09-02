from dataclasses import dataclass

from tactical_lab.models.team import Team
from tactical_lab.simulation.engine import MatchEngine


@dataclass
class ExperimentResult:
    simulations: int
    home_wins: int
    away_wins: int
    draws: int

    home_goals: float
    away_goals: float
    home_possession: float
    away_possession: float
    home_passes: float
    away_passes: float
    home_interceptions: float
    away_interceptions: float
    home_progressions: float
    away_progressions: float
    home_shots: float
    away_shots: float


def run_experiment(
    home_team: Team,
    away_team: Team,
    num_simulations: int,
    seed: int | None = None,
) -> ExperimentResult:
    if num_simulations <= 0:
        raise ValueError("num_simulations must be greater than zero")

    home_wins = 0
    away_wins = 0
    draws = 0

    totals = {
        "home_goals": 0,
        "away_goals": 0,
        "home_possession": 0,
        "away_possession": 0,
        "home_passes": 0,
        "away_passes": 0,
        "home_interceptions": 0,
        "away_interceptions": 0,
        "home_progressions": 0,
        "away_progressions": 0,
        "home_shots": 0,
        "away_shots": 0,
    }

    for simulation_number in range(num_simulations):
        match_seed = (
            None
            if seed is None
            else seed + simulation_number
        )
        result = MatchEngine(
            home_team,
            away_team,
            seed=match_seed,
        ).run()

        if result.home_score > result.away_score:
            home_wins += 1
        elif result.away_score > result.home_score:
            away_wins += 1
        else:
            draws += 1

        totals["home_goals"] += result.home_score
        totals["away_goals"] += result.away_score

        home_stats = result.stats.home
        away_stats = result.stats.away
        total_possession = (
            home_stats.possession_ticks
            + away_stats.possession_ticks
        )

        totals["home_possession"] += (
            home_stats.possession_ticks / total_possession * 100
        )
        totals["away_possession"] += (
            away_stats.possession_ticks / total_possession * 100
        )

        totals["home_passes"] += home_stats.passes
        totals["away_passes"] += away_stats.passes
        totals["home_interceptions"] += home_stats.interceptions
        totals["away_interceptions"] += away_stats.interceptions
        totals["home_progressions"] += home_stats.progressions
        totals["away_progressions"] += away_stats.progressions
        totals["home_shots"] += home_stats.shots
        totals["away_shots"] += away_stats.shots

    average = lambda metric: totals[metric] / num_simulations

    return ExperimentResult(
        simulations=num_simulations,
        home_wins=home_wins,
        away_wins=away_wins,
        draws=draws,
        home_goals=average("home_goals"),
        away_goals=average("away_goals"),
        home_possession=average("home_possession"),
        away_possession=average("away_possession"),
        home_passes=average("home_passes"),
        away_passes=average("away_passes"),
        home_interceptions=average("home_interceptions"),
        away_interceptions=average("away_interceptions"),
        home_progressions=average("home_progressions"),
        away_progressions=average("away_progressions"),
        home_shots=average("home_shots"),
        away_shots=average("away_shots"),
    )

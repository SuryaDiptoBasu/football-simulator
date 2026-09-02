import argparse

from tactical_lab.main import create_team
from tactical_lab.models.clubs import get_club, get_club_names
from tactical_lab.models.formations import FORMATION_POSITIONS
from tactical_lab.models.team import Tactics
from tactical_lab.simulation.engine import MatchEngine
from tactical_lab.simulation.experiments import run_experiment


NUM_SIMULATIONS = 1000


def run_simulations(
    home_team,
    away_team,
    num_simulations: int,
) -> None:
    home_wins = 0
    away_wins = 0
    draws = 0

    total_home_goals = 0
    total_away_goals = 0

    print("\n============================")
    print("   TACTICAL LAB SIMULATOR")
    print("============================\n")

    print(
        f"{home_team.name} "
        f"vs "
        f"{away_team.name}"
    )

    print(
        f"\nRunning {num_simulations} simulations...\n"
    )

    for i in range(num_simulations):
        engine = MatchEngine(
            home_team,
            away_team,
        )

        result = engine.run()

        total_home_goals += result.home_score
        total_away_goals += result.away_score

        if result.home_score > result.away_score:
            home_wins += 1

        elif result.away_score > result.home_score:
            away_wins += 1

        else:
            draws += 1

        print(
            f"Simulation {i + 1:>3} | "
            f"{home_team.name} "
            f"{result.home_score} - "
            f"{result.away_score} "
            f"{away_team.name}"
        )

    print("\n============================")
    print("     SIMULATION RESULTS")
    print("============================\n")

    print(
        f"Total Simulations: {num_simulations}\n"
    )

    print(
        f"{home_team.name} Wins: "
        f"{home_wins} "
        f"({home_wins / num_simulations * 100:.2f}%)"
    )

    print(
        f"{away_team.name} Wins: "
        f"{away_wins} "
        f"({away_wins / num_simulations * 100:.2f}%)"
    )

    print(
        f"Draws: "
        f"{draws} "
        f"({draws / num_simulations * 100:.2f}%)"
    )

    print("\nAverage Goals:")

    print(
        f"{home_team.name}: "
        f"{total_home_goals / num_simulations:.2f}"
    )

    print(
        f"{away_team.name}: "
        f"{total_away_goals / num_simulations:.2f}"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Compare two football clubs over repeated simulations."
    )
    parser.add_argument(
        "--home",
        choices=get_club_names(),
        default="manchester-city",
    )
    parser.add_argument(
        "--away",
        choices=get_club_names(),
        default="real-madrid",
    )
    parser.add_argument(
        "--home-formation",
        choices=tuple(FORMATION_POSITIONS),
    )
    parser.add_argument(
        "--away-formation",
        choices=tuple(FORMATION_POSITIONS),
    )
    parser.add_argument(
        "--simulations",
        type=int,
        default=NUM_SIMULATIONS,
    )
    args = parser.parse_args()

    home_team = get_club(
        args.home,
        team_id=1,
        formation=args.home_formation,
    )
    away_team = get_club(
        args.away,
        team_id=2,
        formation=args.away_formation,
    )

    result = run_experiment(
        home_team,
        away_team,
        args.simulations,
        seed=42,
    )

    print("\n============================")
    print("     TACTICAL EXPERIMENT")
    print("============================\n")
    print(
        f"{home_team.name} vs {away_team.name}"
    )
    print(
        f"Formations: {home_team.tactics.formation} | "
        f"{away_team.tactics.formation}"
    )
    print(f"Simulations: {result.simulations}\n")

    print(
        f"Wins: {home_team.name} {result.home_wins} "
        f"({result.home_wins / result.simulations * 100:.2f}%) | "
        f"{away_team.name} {result.away_wins} "
        f"({result.away_wins / result.simulations * 100:.2f}%) | "
        f"Draws {result.draws} "
        f"({result.draws / result.simulations * 100:.2f}%)"
    )

    print("\nAverage metrics:")
    print(
        f"Goals:         {result.home_goals:.2f} | "
        f"{result.away_goals:.2f}"
    )
    print(
        f"Possession:    {result.home_possession:.1f}% | "
        f"{result.away_possession:.1f}%"
    )
    print(
        f"Passes:        {result.home_passes:.2f} | "
        f"{result.away_passes:.2f}"
    )
    print(
        f"Interceptions: {result.home_interceptions:.2f} | "
        f"{result.away_interceptions:.2f}"
    )
    print(
        f"Progressions:  {result.home_progressions:.2f} | "
        f"{result.away_progressions:.2f}"
    )
    print(
        f"Shots:         {result.home_shots:.2f} | "
        f"{result.away_shots:.2f}"
    )


if __name__ == "__main__":
    main()
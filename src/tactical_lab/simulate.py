from tactical_lab.main import create_team
from tactical_lab.models.team import Tactics
from tactical_lab.simulation.engine import MatchEngine


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
    home_team = create_team(
        1,
        "Red United",
        Tactics(
            formation="4-3-3",
            pressing="high",
            passing_style="short",
        ),
    )

    away_team = create_team(
        2,
        "Blue City",
        Tactics(
            formation="4-2-3-1",
            pressing="low",
            passing_style="direct",
            counter_attack=True,
        ),
    )

    run_simulations(
        home_team,
        away_team,
        NUM_SIMULATIONS,
    )


if __name__ == "__main__":
    main()
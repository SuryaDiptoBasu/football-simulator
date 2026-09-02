import argparse

from tactical_lab.models.clubs import get_club, get_club_names
from tactical_lab.models.formations import get_formation_positions
from tactical_lab.models.formations import FORMATION_POSITIONS
from tactical_lab.models.player import Player, Position
from tactical_lab.models.team import Tactics, Team
from tactical_lab.simulation.engine import MatchEngine


def create_team(
    team_id: int,
    name: str,
    tactics: Tactics,
) -> Team:

    positions = get_formation_positions(tactics.formation)

    players = []

    for i, position in enumerate(positions, start=1):

        if position == Position.GK:
            player = Player(
                id=i,
                name=f"{name} Player {i}",
                position=position,
                pace=50,
                passing=60,
                shooting=20,
                defending=85,
                stamina=70,
            )

        elif position in {Position.LB, Position.CB, Position.RB}:
            player = Player(
                id=i,
                name=f"{name} Player {i}",
                position=position,
                pace=65,
                passing=65,
                shooting=35,
                defending=85,
                stamina=80,
            )

        elif position in {Position.DM, Position.CM, Position.AM}:
            player = Player(
                id=i,
                name=f"{name} Player {i}",
                position=position,
                pace=70,
                passing=85,
                shooting=60,
                defending=65,
                stamina=85,
            )

        else:
            player = Player(
                id=i,
                name=f"{name} Player {i}",
                position=position,
                pace=85,
                passing=70,
                shooting=88,
                defending=35,
                stamina=75,
            )

        players.append(player)

    return Team(
        id=team_id,
        name=name,
        players=players,
        tactics=tactics,
    )


def format_time(seconds: int) -> str:
    minutes = seconds // 60
    seconds = seconds % 60

    return f"{minutes:02}:{seconds:02}"


def main():
    parser = argparse.ArgumentParser(
        description="Simulate one football match between two clubs."
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

    engine = MatchEngine(
        home_team,
        away_team,
        seed=42,
    )

    result = engine.run()

    print("\n============================")
    print("       TACTICAL LAB")
    print("============================\n")
    print(
        f"{home_team.name} ({home_team.tactics.formation}) "
        f"vs {away_team.name} ({away_team.tactics.formation})\n"
    )

    for event in engine.events:
        time = format_time(event.timestamp)

        team = None

        if event.team_id == home_team.id:
            team = home_team
        elif event.team_id == away_team.id:
            team = away_team

        player_name = None

        if team and event.player_id:
            player = next(
                (
                    p
                    for p in team.players
                    if p.id == event.player_id
                ),
                None,
            )

            if player:
                player_name = player.name

        output = f"{time} | {event.event_type.value}"

        if event.event_type.value == "PROGRESSION" and event.data:
            from_zone = event.data.get("from_zone")
            to_zone = event.data.get("to_zone")

            output += f" | {from_zone} → {to_zone}"

        if team:
            output += f" | {team.name}"

        if player_name:
            if event.event_type.value == "GOAL":
                output += f" | Scorer: {player_name}"
            else:
                output += f" | {player_name}"

        if event.event_type.value == "PASS":
            target_id = event.data.get(
                "target_player_id"
            )

            target = next(
                (
                    p
                    for p in team.players
                    if p.id == target_id
                ),
                None,
            )

            if target:
                output += f" → {target.name}"

        print(output)

    print("\nFINAL SCORE")

    print(
        f"{home_team.name} "
        f"{result.home_score}"
    )

    print(
        f"{away_team.name} "
        f"{result.away_score}"
    )

    goal_events = [
        event
        for event in engine.events
        if event.event_type.value == "GOAL"
    ]

    for event in goal_events:
        team = (
            home_team
            if event.team_id == home_team.id
            else away_team
        )
        scorer = next(
            (
                player
                for player in team.players
                if player.id == event.player_id
            ),
            None,
        )
        scorer_name = (
            scorer.name
            if scorer
            else "Unknown scorer"
        )
        print(
            f"{format_time(event.timestamp)} | "
            f"{team.name} | {scorer_name}"
        )

    stats = result.stats

    total_possession = (
        stats.home.possession_ticks
        + stats.away.possession_ticks
    )

    home_possession = (
        stats.home.possession_ticks
        / total_possession
        * 100
    )

    away_possession = (
        stats.away.possession_ticks
        / total_possession
        * 100
    )

    print("\nMATCH STATISTICS")
    print("============================")

    print(
        f"Possession: "
        f"{home_team.name} {home_possession:.1f}% | "
        f"{away_possession:.1f}% {away_team.name}"
    )

    print(
        f"Passes:     "
        f"{stats.home.passes} | {stats.away.passes}"
    )

    print(
        f"Interceptions: "
        f"{stats.home.interceptions} | "
        f"{stats.away.interceptions}"
    )

    print(
        f"Progressions: "
        f"{stats.home.progressions} | "
        f"{stats.away.progressions}"
    )

    print(
        f"Shots: "
        f"{stats.home.shots} | "
        f"{stats.away.shots}"
    )


if __name__ == "__main__":
    main()
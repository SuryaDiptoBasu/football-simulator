from tactical_lab.models.player import Player
from tactical_lab.models.team import Tactics, Team
from tactical_lab.simulation.engine import MatchEngine


def create_team(
    team_id: int,
    name: str,
    tactics: Tactics,
) -> Team:

    positions = [
        "GK",
        "DEF",
        "DEF",
        "DEF",
        "DEF",
        "MID",
        "MID",
        "MID",
        "FWD",
        "FWD",
        "FWD",
    ]

    players = []

    for i, position in enumerate(positions, start=1):

        if position == "GK":
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

        elif position == "DEF":
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

        elif position == "MID":
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
    home_team = create_team(
        1,
        "Manchester United",
        Tactics(
            formation="4-3-3",
            pressing="high",
            passing_style="short",
        ),
    )

    away_team = create_team(
        2,
        "Manchester City",
        Tactics(
            formation="4-2-3-1",
            pressing="low",
            passing_style="direct",
            counter_attack=True,
        ),
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
import random

from tactical_lab.models.match import MatchState
from tactical_lab.simulation.events import EventType, MatchEvent
from tactical_lab.models.field import BallZone
from tactical_lab.models.player import Position
from tactical_lab.models.formations import (
    get_passing_positions,
    get_progression_positions,
)

class MatchEngine:
    def __init__(self, home_team, away_team, seed: int | None = None):
        self.state = MatchState(
            home_team=home_team,
            away_team=away_team,
        )

        self.events: list[MatchEvent] = []

        self.random = random.Random(seed)

    def run(self) -> MatchState:
        self._emit(EventType.MATCH_STARTED)

        # Simplified: 90 minutes = 5400 seconds
        while self.state.current_time < 5400:
            self._simulate_tick()

        self.state.finished = True

        self._emit(EventType.MATCH_ENDED)

        return self.state

    def _simulate_tick(self) -> None:
        # Advance match by 5–20 seconds
        self.state.current_time += self.random.randint(5, 20)

        # Pick which team has possession
        if self.state.possession_team_id is None:
            team = self.random.choice(
                [
                    self.state.home_team,
                    self.state.away_team,
                ]
            )

            #self.state.possession_team_id = team.id

            player = self._choose_defensive_player(team)

            #self.state.ball_player_id = player.id

            self._change_possession(
                team,
                player,
                BallZone.DEFENSIVE,
            )

            self._emit(
                EventType.POSSESSION_CHANGED,
                team_id=team.id,
                player_id=player.id,
                data={
                    "zone": BallZone.DEFENSIVE.name,
                },
            )

            return

        attacking_team = self._get_team_by_id(
            self.state.possession_team_id
        )

        attacking_player = self._get_current_player(
            attacking_team
        )

        defending_team = self._get_opponent(attacking_team.id)

        pressing_modifier = self._get_pressing_modifier(
            defending_team
        )

        passing_modifier = self._get_passing_modifier(
            attacking_team
        )

        shot_modifier = self._get_shot_modifier(
            attacking_team
        )

        # pass_weight = 70 + passing_modifier * 100
        # interception_weight = 20 + pressing_modifier * 100
        # shot_weight = 10 + shot_modifier * 100

        # Decide what happens
        # action = self.random.choices(
        #     ["pass", "interception", "shot"],
        #     weights=[
        #         pass_weight,
        #         interception_weight,
        #         shot_weight,
        #     ],
        # )[0]

        team_stats = self._get_team_stats(
            attacking_team.id
        )

        team_stats.possession_ticks += 1

        action = self._choose_action(
            attacking_team,
            defending_team,
        )

        

        if action == "pass":

            target_player = self._choose_pass_target(
                attacking_team,
                attacking_player,
            )

            self._emit(
                EventType.PASS,
                team_id=attacking_team.id,
                player_id=attacking_player.id,
                data={
                    "target_player_id": target_player.id,
                },
            )

            pass_success_probability = (
                0.50
                + attacking_player.passing / 200
                + passing_modifier
                + (attacking_player.stamina - 75) / 1000
                + (attacking_player.dribbling - 75) / 2000
            )

            pass_success_probability = max(
                0.50,
                min(pass_success_probability, 0.95),
            )

            if self.random.random() < pass_success_probability:
                # PASS SUCCESSFUL
                team_stats = self._get_team_stats(
                    attacking_team.id
                )

                team_stats.passes += 1
                self.state.ball_player_id = target_player.id

                if self.state.ball_zone < BallZone.ATTACKING:

                    progression_probability = (
                        0.35
                        + (target_player.pace - 75) / 1000
                        + (target_player.dribbling - 75) / 2000
                    )
                    progression_probability = max(
                        0.25,
                        min(progression_probability, 0.45),
                    )

                    if self.random.random() < progression_probability:

                        previous_zone = self.state.ball_zone

                        self.state.ball_zone = BallZone(
                            self.state.ball_zone + 1
                        )

                        self._emit(
                            EventType.PROGRESSION,
                            team_id=attacking_team.id,
                            player_id=target_player.id,
                            data={
                                "from_zone": previous_zone.name,
                                "to_zone": self.state.ball_zone.name,
                            },
                        )


            else:
                # PASS FAILED → opponent wins possession
                self.state.possession_team_id = defending_team.id

                new_player = self._choose_defensive_player(
                    defending_team
                )

                self._change_possession(
                    defending_team,
                    new_player,
                    BallZone.DEFENSIVE,
                )

                self._emit(
                    EventType.INTERCEPTION,
                    team_id=defending_team.id,
                    player_id=new_player.id,
                )

        elif action == "interception":
            new_player = self._choose_defensive_player(
                defending_team
            )

            self._change_possession(
                defending_team,
                new_player,
                BallZone.DEFENSIVE,
            )

            self._emit(
                EventType.INTERCEPTION,
                team_id=defending_team.id,
                player_id=new_player.id,
                data={
                    "zone": BallZone.DEFENSIVE.name,
                },
            )

            team_stats = self._get_team_stats(
                defending_team.id
            )

            team_stats.interceptions += 1

        elif action == "shot":
            team_stats = self._get_team_stats(
                attacking_team.id
            )

            team_stats.shots += 1

            self._emit(
                EventType.SHOT,
                team_id=attacking_team.id,
                player_id=attacking_player.id,
            )

            goalkeeper = self._get_goalkeeper(defending_team)
            goalkeeper_penalty = (
                goalkeeper.defending / 4000
                if goalkeeper
                else 0
            )

            goal_probability = (
                0.02
                + attacking_player.shooting / 700
                + attacking_player.dribbling / 4000
                + attacking_player.physical / 6000
                + shot_modifier
                - goalkeeper_penalty
            )

            goal_probability = max(
                0.03,
                min(goal_probability, 0.30),
            )

            if self.random.random() < goal_probability:
                self._score_goal(
                    attacking_team.id,
                    attacking_player.id,
                )

            else:
        
                new_player = self._choose_defensive_player(
                    defending_team
                )

                self._change_possession(
                    defending_team,
                    new_player,
                    BallZone.DEFENSIVE,
                )

        elif action == "progress":
            team_stats = self._get_team_stats(
                attacking_team.id
            )

            team_stats.progressions += 1
            current_zone = self.state.ball_zone
            progression_target = self._choose_progression_target(
                attacking_team,
                attacking_player,
            )

            if progression_target:
                self.state.ball_player_id = progression_target.id

            if current_zone < BallZone.BOX:

                next_zone = BallZone(
                    current_zone + 1
                )

                self.state.ball_zone = next_zone

                self._emit(
                    EventType.PROGRESSION,
                    team_id=attacking_team.id,
                    player_id=(
                        progression_target.id
                        if progression_target
                        else attacking_player.id
                    ),
                    data={
                        "from_zone": current_zone.name,
                        "to_zone": next_zone.name,
                    },
                )

    def _score_goal(self, team_id: int, player_id: int) -> None:
        if team_id == self.state.home_team.id:
            self.state.home_score += 1
        else:
            self.state.away_score += 1

        self._emit(
            EventType.GOAL,
            team_id=team_id,
            player_id=player_id,
        )
        team_stats = self._get_team_stats(
            team_id
        )

        team_stats.goals += 1
        opponent = self._get_opponent(team_id)

        new_player = self._choose_possession_player(
            opponent
        )

        self._change_possession(
            opponent,
            new_player,
            BallZone.DEFENSIVE,
        )

    def _choose_pass_target(self, team, current_player):
        candidates = [
            player
            for player in team.players
            if player.id != current_player.id
            and player.position != Position.GK
            and player.position
            in get_passing_positions(current_player.position)
        ]

        if not candidates:
            candidates = [
                player
                for player in team.players
                if player.id != current_player.id
                and player.position != Position.GK
            ]

        return self.random.choice(candidates)

    def _choose_progression_target(self, team, current_player):
        candidates = [
            player
            for player in team.players
            if player.id != current_player.id
            and player.position
            in get_progression_positions(current_player.position)
        ]

        if not candidates:
            return None

        return self.random.choice(candidates)

    def _get_team_by_id(self, team_id: int):
        if team_id == self.state.home_team.id:
            return self.state.home_team

        return self.state.away_team

    def _get_opponent(self, team_id: int):
        if team_id == self.state.home_team.id:
            return self.state.away_team

        return self.state.home_team

    def _get_pressing_modifier(self, team) -> float:
        pressing = team.tactics.pressing

        modifiers = {
            "low": -0.05,
            "medium": 0.0,
            "high": 0.10,
        }

        return modifiers.get(pressing, 0.0)

    def _choose_possession_player(self, team):
        players = [
            player
            for player in team.players
            if player.position != Position.GK
        ]

        return self.random.choice(players)

    def _choose_defensive_player(self, team):
        defensive_positions = {
            Position.LB,
            Position.CB,
            Position.RB,
            Position.DM,
            Position.CM,
        }

        players = [
            player
            for player in team.players
            if player.position in defensive_positions
        ]

        if not players:
            return self._choose_possession_player(team)

        return self.random.choice(players)

    def _get_player_by_id(self, team, player_id):
        for player in team.players:
            if player.id == player_id:
                return player

        return None

    def _get_current_player(self, team):
        return self._get_player_by_id(
            team,
            self.state.ball_player_id,
        )


    def _get_passing_modifier(self, team) -> float:
        passing_style = team.tactics.passing_style

        modifiers = {
            "short": 0.10,
            "mixed": 0.0,
            "direct": -0.10,
        }

        return modifiers.get(passing_style, 0.0)

    def _get_shot_modifier(self, team) -> float:
        passing_style = team.tactics.passing_style

        modifiers = {
            "short": -0.02,
            "mixed": 0.0,
            "direct": 0.05,
        }

        modifier = modifiers.get(passing_style, 0.0)

        if team.tactics.counter_attack:
            modifier += 0.05

        return modifier

    def _change_possession(
        self,
        team,
        player,
        zone,
    ) -> None:
        self.state.possession_team_id = team.id
        self.state.ball_player_id = player.id
        self.state.ball_zone = zone

    def _choose_action(self, team, defending_team):
        zone = self.state.ball_zone

        if zone == BallZone.DEFENSIVE:

            actions = [
                "pass",
                "interception",
                "progress",
            ]

            weights = [
                70,
                20,
                10,
            ]

        elif zone == BallZone.MIDFIELD:

            actions = [
                "pass",
                "interception",
                "progress",
            ]

            weights = [
                55,
                25,
                20,
            ]

        elif zone == BallZone.ATTACKING:

            actions = [
                "pass",
                "interception",
                "progress",
                "shot",
            ]

            weights = [
                40,
                25,
                15,
                20,
            ]

        else:

            actions = [
                "pass",
                "interception",
                "shot",
            ]

            weights = [
                20,
                20,
                60,
            ]

        attribute_weights = {
            "pass": 1 + (self._get_team_average(team, "passing") - 75) / 20,
            "interception": 1 + (
                self._get_team_average(defending_team, "defending") - 75
            ) / 20,
            "progress": 1 + (
                self._get_team_average(team, "pace")
                + self._get_team_average(team, "dribbling")
                - 150
            ) / 40,
            "shot": 1 + (self._get_team_average(team, "shooting") - 75) / 20,
        }
        adjusted_weights = [
            max(1, weight * attribute_weights[action])
            for action, weight in zip(actions, weights)
        ]

        return self.random.choices(
            actions,
            weights=adjusted_weights,
            k=1,
        )[0]

    def _get_team_average(self, team, attribute: str) -> float:
        players = [
            player
            for player in team.players
            if player.position != Position.GK
        ]

        if not players:
            return 0

        return sum(getattr(player, attribute) for player in players) / len(players)

    def _get_goalkeeper(self, team):
        return next(
            (
                player
                for player in team.players
                if player.position == Position.GK
            ),
            None,
        )

    def _get_team_stats(self, team_id: int):
        if team_id == self.state.home_team.id:
            return self.state.stats.home

        return self.state.stats.away
    
    def _emit(
        self,
        event_type: EventType,
        team_id: int | None = None,
        player_id: int | None = None,
        data=None,
    ) -> None:
        event = MatchEvent(
            timestamp=self.state.current_time,
            event_type=event_type,
            team_id=team_id,
            player_id=player_id,
            data=data,
        )

        self.events.append(event)
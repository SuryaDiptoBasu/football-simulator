# Tactical Lab

A small casual football simulation game written in Python.

Pick two clubs, choose their formations, and let the match play out. The
engine creates match events such as passes, progressions, interceptions,
shots, and goals. You can also run the same matchup many times to see which
team usually comes out on top.

## Use the app

Install the project dependencies and start the Streamlit app:

```bash
uv sync
uv run streamlit run app.py
```

Then open the local address shown in the terminal. The app lets you choose
the home club, away club, formation for each side, and whether to play one
match or run many simulations.

## Run one match

This prints the match events, final score, scorers, and match statistics.

```bash
uv run python -m tactical_lab.main \
	--home liverpool \
	--away juventus \
	--home-formation 4-3-3 \
	--away-formation 4-2-3-1
```

Remember to leave a space before each `\` when writing a command over
multiple lines.

## Run many matches

This prints the overall results and average statistics for the matchup.

```bash
uv run python -m tactical_lab.simulate \
	--home barcelona \
	--away lyon \
	--home-formation 4-3-3 \
	--away-formation 3-5-2 \
	--simulations 1000
```

## Clubs

The project currently includes clubs from England, Spain, Germany, France,
and Italy. Each club has a 16-player squad and an 11-player starting lineup.

Available club IDs:

```text
manchester-city
real-madrid
bayern-munich
paris-saint-germain
inter-milan
arsenal
manchester-united
chelsea
liverpool
tottenham
barcelona
atletico-madrid
borussia-dortmund
bayer-leverkusen
rb-leipzig
as-monaco
lyon
marseille
juventus
ac-milan
napoli
roma
lazio
```

## Formations

```text
3-4-3
4-3-3
3-5-2
4-5-1
4-2-3-1
4-4-2
5-4-1
```

Changing a formation chooses a new starting eleven from the club's squad
and assigns players to the new positional slots.

## Player ratings

Players have simple game-style ratings for:

- Pace
- Passing
- Shooting
- Defending
- Stamina
- Dribbling
- Physical
- Overall

These ratings affect passing, progression, action choices, shots, and goals.
They are casual simulation ratings, not official FIFA data.

## Project layout

```text
src/tactical_lab/
├── main.py                 # One detailed match
├── simulate.py             # Repeated matchup experiments
├── models/
│   ├── clubs.py            # Clubs, squads, ratings, and lineups
│   ├── formations.py       # Formation positions and relationships
│   ├── player.py           # Player model and positions
│   ├── team.py             # Teams and tactics
│   ├── match.py            # Match state
│   └── stats.py            # Match statistics
└── simulation/
	├── engine.py           # Match simulation rules
	├── events.py           # Match events
	└── experiments.py      # Repeated simulations
```

This is still a simple game project, so the football logic is intentionally
lightweight. The fun part is trying different club and formation matchups
and seeing what happens.

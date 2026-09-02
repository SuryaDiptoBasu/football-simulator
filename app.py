import streamlit as st

from tactical_lab.models.clubs import get_club, get_club_names
from tactical_lab.models.formations import FORMATION_POSITIONS
from tactical_lab.simulation.engine import MatchEngine
from tactical_lab.simulation.experiments import run_experiment


st.set_page_config(
    page_title="Tactical Lab",
    page_icon="⚽",
    layout="wide",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Space+Grotesk:wght@500;600;700&display=swap');
    :root { --ink: #14221e; --muted: #66746c; --mint: #d9f36a; --paper: #f5f6ef; --line: #dce2d8; }
    .stApp { background: var(--paper); color: var(--ink); }
    [data-testid="stHeader"] { background: transparent; }
    .block-container { max-width: 1180px; padding-top: 3rem; padding-bottom: 4rem; }
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif; color: var(--ink); letter-spacing: 0; }
    p, label, .stMarkdown, .stText { font-family: 'DM Sans', sans-serif; }
    .eyebrow { color: #638000; font-size: .78rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; }
    .hero { border-bottom: 1px solid var(--line); padding-bottom: 2rem; margin-bottom: 1.8rem; }
    .hero h1 { font-size: clamp(2.6rem, 6vw, 5.4rem); line-height: .95; margin: .45rem 0 1rem; }
    .hero-copy { color: var(--muted); font-size: 1.08rem; max-width: 650px; }
    .panel { background: white; border: 1px solid var(--line); border-radius: 8px; padding: 1.2rem 1.35rem; }
    .team-label { font-size: .74rem; text-transform: uppercase; letter-spacing: .12em; color: var(--muted); font-weight: 700; }
    .team-name { font-family: 'Space Grotesk', sans-serif; font-size: 1.55rem; font-weight: 700; margin: .3rem 0 0; }
    .formation { color: #638000; font-weight: 700; }
    .score { background: var(--ink); color: white; border-radius: 8px; padding: 1.5rem; text-align: center; }
    .score-line { font-family: 'Space Grotesk', sans-serif; font-size: 2.6rem; font-weight: 700; }
    .metric { background: white; border-left: 4px solid var(--mint); border-top: 1px solid var(--line); border-right: 1px solid var(--line); border-bottom: 1px solid var(--line); border-radius: 4px; padding: .8rem 1rem; }
    .metric-label { color: var(--muted); font-size: .76rem; text-transform: uppercase; letter-spacing: .08em; }
    .metric-value { font-family: 'Space Grotesk', sans-serif; font-size: 1.35rem; font-weight: 700; }
    .event { border-bottom: 1px solid var(--line); padding: .65rem 0; font-family: 'DM Sans', sans-serif; }
    .event-time { color: #638000; font-weight: 700; min-width: 55px; display: inline-block; }
    .stButton > button { background: var(--ink); color: white; border: 0; border-radius: 4px; font-weight: 700; padding: .7rem 1rem; }
    .stButton > button:hover { background: #2c443b; color: var(--mint); }
    </style>
    """,
    unsafe_allow_html=True,
)


def team_card(team, label: str) -> None:
    st.markdown(
        f"""
        <div class="panel">
            <div class="team-label">{label}</div>
            <div class="team-name">{team.name}</div>
            <div class="formation">{team.tactics.formation} formation</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric(label: str, home_value: str, away_value: str) -> None:
    st.markdown(
        f"""
        <div class="metric">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{home_value} &nbsp;·&nbsp; {away_value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def format_time(seconds: int) -> str:
    return f"{seconds // 60:02}:{seconds % 60:02}"


st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">Football match laboratory</div>
        <h1>Pick a matchup.<br>See what happens.</h1>
        <div class="hero-copy">Choose two clubs, reshape their starting elevens, and run one match or a whole batch of simulations.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

club_ids = get_club_names()
formation_ids = tuple(FORMATION_POSITIONS)
club_labels = {club_id: get_club(club_id).name for club_id in club_ids}

left, right = st.columns(2, gap="large")
with left:
    st.markdown("#### Home side")
    home_id = st.selectbox(
        "Home club",
        club_ids,
        format_func=lambda club_id: club_labels[club_id],
        key="home_club",
    )
    home_default = get_club(home_id).tactics.formation
    home_formation = st.selectbox(
        "Home formation",
        formation_ids,
        index=formation_ids.index(home_default),
        key="home_formation",
    )
    home_team = get_club(home_id, team_id=1, formation=home_formation)

with right:
    st.markdown("#### Away side")
    away_id = st.selectbox(
        "Away club",
        club_ids,
        format_func=lambda club_id: club_labels[club_id],
        index=1 if len(club_ids) > 1 else 0,
        key="away_club",
    )
    away_default = get_club(away_id).tactics.formation
    away_formation = st.selectbox(
        "Away formation",
        formation_ids,
        index=formation_ids.index(away_default),
        key="away_formation",
    )
    away_team = get_club(away_id, team_id=2, formation=away_formation)

team_card(home_team, "Home")
team_card(away_team, "Away")

st.markdown("#### Starting elevens")
lineup_left, lineup_right = st.columns(2, gap="large")
with lineup_left:
    st.dataframe(
        [{"Position": player.position.value, "Player": player.name, "OVR": player.overall} for player in home_team.players],
        hide_index=True,
        width="stretch",
    )
with lineup_right:
    st.dataframe(
        [{"Position": player.position.value, "Player": player.name, "OVR": player.overall} for player in away_team.players],
        hide_index=True,
        width="stretch",
    )

st.markdown("#### Match mode")
mode = st.radio(
    "Choose how to play",
    ["One match", "Many simulations"],
    horizontal=True,
    label_visibility="collapsed",
)
simulation_count = 1
if mode == "Many simulations":
    simulation_count = st.slider("Number of simulations", 10, 10000, 1000, step=10)

if st.button("Run the match", type="primary", use_container_width=True):
    if mode == "One match":
        engine = MatchEngine(home_team, away_team, seed=42)
        result = engine.run()
        st.session_state["single_result"] = (home_team, away_team, engine, result)
        st.session_state.pop("experiment_result", None)
    else:
        experiment = run_experiment(home_team, away_team, simulation_count, seed=42)
        st.session_state["experiment_result"] = (home_team, away_team, experiment)
        st.session_state.pop("single_result", None)

if "single_result" in st.session_state:
    home_team, away_team, engine, result = st.session_state["single_result"]
    st.markdown("### Final score")
    st.markdown(
        f'<div class="score"><div class="team-name">{home_team.name} &nbsp; {result.home_score} — {result.away_score} &nbsp; {away_team.name}</div><div class="formation">{home_team.tactics.formation} vs {away_team.tactics.formation}</div></div>',
        unsafe_allow_html=True,
    )
    st.markdown("### Match stats")
    total_possession = (
        result.stats.home.possession_ticks
        + result.stats.away.possession_ticks
    )
    home_possession = (
        result.stats.home.possession_ticks
        / total_possession
        * 100
    )
    away_possession = (
        result.stats.away.possession_ticks
        / total_possession
        * 100
    )
    stats_left, stats_right = st.columns(2, gap="large")
    with stats_left:
        metric("Possession", f"{home_possession:.1f}%", f"{away_possession:.1f}%")
        metric("Passes", str(result.stats.home.passes), str(result.stats.away.passes))
        metric("Shots", str(result.stats.home.shots), str(result.stats.away.shots))
    with stats_right:
        metric("Interceptions", str(result.stats.home.interceptions), str(result.stats.away.interceptions))
        metric("Progressions", str(result.stats.home.progressions), str(result.stats.away.progressions))
        metric("Goals", str(result.stats.home.goals), str(result.stats.away.goals))

    st.markdown("### Match events")
    goal_events = [event for event in engine.events if event.event_type.value == "GOAL"]
    if goal_events:
        for event in goal_events:
            team = home_team if event.team_id == home_team.id else away_team
            player = next(player for player in team.players if player.id == event.player_id)
            st.markdown(
                f'<div class="event"><span class="event-time">{format_time(event.timestamp)}</span><strong>GOAL</strong> &nbsp; {team.name} &nbsp; {player.name}</div>',
                unsafe_allow_html=True,
            )
    else:
        st.caption("No goals in this match.")

elif "experiment_result" in st.session_state:
    home_team, away_team, result = st.session_state["experiment_result"]
    st.markdown("### Simulation results")
    st.markdown(
        f'<div class="score"><div class="team-name">{home_team.name} vs {away_team.name}</div><div class="formation">{result.simulations} simulations · {home_team.tactics.formation} vs {away_team.tactics.formation}</div></div>',
        unsafe_allow_html=True,
    )
    home_win_rate = result.home_wins / result.simulations * 100
    away_win_rate = result.away_wins / result.simulations * 100
    draw_rate = result.draws / result.simulations * 100
    st.markdown("### Results")
    result_left, result_mid, result_right = st.columns(3)
    result_left.metric(home_team.name, f"{home_win_rate:.1f}% wins")
    result_mid.metric("Draws", f"{draw_rate:.1f}%")
    result_right.metric(away_team.name, f"{away_win_rate:.1f}% wins")
    st.markdown("### Average match stats")
    stats_left, stats_right = st.columns(2, gap="large")
    with stats_left:
        metric("Goals", f"{result.home_goals:.2f}", f"{result.away_goals:.2f}")
        metric("Possession", f"{result.home_possession:.1f}%", f"{result.away_possession:.1f}%")
        metric("Passes", f"{result.home_passes:.1f}", f"{result.away_passes:.1f}")
    with stats_right:
        metric("Interceptions", f"{result.home_interceptions:.1f}", f"{result.away_interceptions:.1f}")
        metric("Progressions", f"{result.home_progressions:.1f}", f"{result.away_progressions:.1f}")
        metric("Shots", f"{result.home_shots:.1f}", f"{result.away_shots:.1f}")
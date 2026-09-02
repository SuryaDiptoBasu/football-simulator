from dataclasses import dataclass, replace

from tactical_lab.models.player import Player, Position
from tactical_lab.models.team import Tactics, Team
from tactical_lab.models.formations import get_formation_positions


SQUAD_POSITIONS = (
    Position.GK, Position.GK, Position.LB, Position.CB,
    Position.CB, Position.RB, Position.DM, Position.CM,
    Position.CM, Position.AM, Position.LW, Position.RW,
    Position.ST, Position.ST, Position.CM, Position.CB,
)


ADDITIONAL_CLUBS = {
    "arsenal": ("Arsenal", "England", "4-3-3", 84, ("David Raya", "Neto", "Ben White", "William Saliba", "Gabriel", "Jurrien Timber", "Declan Rice", "Martin Odegaard", "Kai Havertz", "Bukayo Saka", "Gabriel Martinelli", "Leandro Trossard", "Gabriel Jesus", "Raheem Sterling", "Thomas Partey", "Jakub Kiwior")),
    "manchester-united": ("Manchester United", "England", "4-3-3", 80, ("Andre Onana", "Altay Bayindir", "Diogo Dalot", "Matthijs de Ligt", "Lisandro Martinez", "Noussair Mazraoui", "Casemiro", "Bruno Fernandes", "Mason Mount", "Marcus Rashford", "Alejandro Garnacho", "Antony", "Rasmus Hojlund", "Joshua Zirkzee", "Christian Eriksen", "Harry Maguire")),
    "chelsea": ("Chelsea", "England", "4-2-3-1", 79, ("Robert Sanchez", "Filip Jorgensen", "Reece James", "Wesley Fofana", "Levi Colwill", "Malo Gusto", "Moises Caicedo", "Enzo Fernandez", "Cole Palmer", "Christopher Nkunku", "Mykhailo Mudryk", "Pedro Neto", "Nicolas Jackson", "Joao Felix", "Romeo Lavia", "Benoit Badiashile")),
    "liverpool": ("Liverpool", "England", "4-3-3", 86, ("Alisson", "Caoimhin Kelleher", "Trent Alexander-Arnold", "Virgil van Dijk", "Ibrahima Konate", "Andy Robertson", "Ryan Gravenberch", "Alexis Mac Allister", "Curtis Jones", "Dominik Szoboszlai", "Luis Diaz", "Mohamed Salah", "Darwin Nunez", "Diogo Jota", "Wataru Endo", "Joe Gomez")),
    "tottenham": ("Tottenham Hotspur", "England", "4-3-3", 80, ("Guglielmo Vicario", "Fraser Forster", "Pedro Porro", "Cristian Romero", "Micky van de Ven", "Destiny Udogie", "Yves Bissouma", "Rodrigo Bentancur", "James Maddison", "Dejan Kulusevski", "Son Heung-min", "Brennan Johnson", "Dominic Solanke", "Timo Werner", "Pape Matar Sarr", "Radu Dragusin")),
    "barcelona": ("FC Barcelona", "Spain", "4-3-3", 85, ("Marc-Andre ter Stegen", "Inaki Pena", "Jules Kounde", "Ronald Araujo", "Pau Cubarsi", "Alejandro Balde", "Frenkie de Jong", "Pedri", "Gavi", "Dani Olmo", "Raphinha", "Lamine Yamal", "Robert Lewandowski", "Ferran Torres", "Fermin Lopez", "Andreas Christensen")),
    "atletico-madrid": ("Atletico Madrid", "Spain", "3-5-2", 83, ("Jan Oblak", "Juan Musso", "Nahuel Molina", "Jose Maria Gimenez", "Robin Le Normand", "Reinildo Mandava", "Rodrigo De Paul", "Marcos Llorente", "Koke", "Antoine Griezmann", "Samuel Lino", "Angel Correa", "Julian Alvarez", "Alexander Sorloth", "Conor Gallagher", "Axel Witsel")),
    "borussia-dortmund": ("Borussia Dortmund", "Germany", "4-3-3", 81, ("Gregor Kobel", "Alexander Meyer", "Julian Ryerson", "Nico Schlotterbeck", "Niklas Sule", "Ramy Bensebaini", "Emre Can", "Julian Brandt", "Marcel Sabitzer", "Jamie Gittens", "Karim Adeyemi", "Donyell Malen", "Serhou Guirassy", "Maximilian Beier", "Felix Nmecha", "Waldemar Anton")),
    "bayer-leverkusen": ("Bayer Leverkusen", "Germany", "3-4-3", 85, ("Lukas Hradecky", "Matej Kovar", "Jeremie Frimpong", "Jonathan Tah", "Edmond Tapsoba", "Piero Hincapie", "Granit Xhaka", "Alejandro Grimaldo", "Robert Andrich", "Florian Wirtz", "Nathan Tella", "Martin Terrier", "Victor Boniface", "Patrik Schick", "Exequiel Palacios", "Arthur")),
    "rb-leipzig": ("RB Leipzig", "Germany", "4-4-2", 80, ("Peter Gulacsi", "Maarten Vandevoordt", "Benjamin Henrichs", "Willi Orban", "Castello Lukeba", "David Raum", "Xaver Schlager", "Nicolas Seiwald", "Kevin Kampl", "Xavi Simons", "Lois Openda", "Antonio Nusa", "Benjamin Sesko", "Yussuf Poulsen", "Christoph Baumgartner", "Lukas Klostermann")),
    "as-monaco": ("AS Monaco", "France", "4-4-2", 79, ("Philipp Kohn", "Radoslaw Majecki", "Vanderson", "Thilo Kehrer", "Mohammed Salisu", "Caio Henrique", "Denis Zakaria", "Youssouf Fofana", "Aleksandr Golovin", "Takumi Minamino", "Eliesse Ben Seghir", "Maghnes Akliouche", "Folarin Balogun", "Breel Embolo", "Lamine Camara", "Wilfried Singo")),
    "lyon": ("Olympique Lyonnais", "France", "4-3-3", 77, ("Lucas Perri", "Anthony Lopes", "Clinton Mata", "Duje Caleta-Car", "Moussa Niakhate", "Nicolas Tagliafico", "Nemanja Matic", "Maxence Caqueret", "Corentin Tolisso", "Rayan Cherki", "Ernest Nuamah", "Malick Fofana", "Alexandre Lacazette", "Georges Mikautadze", "Jordan Veretout", "Orel Mangala")),
    "marseille": ("Olympique de Marseille", "France", "4-3-3", 78, ("Geronimo Rulli", "Jeffrey de Lange", "Jonathan Clauss", "Leonardo Balerdi", "Derek Cornelius", "Ulisses Garcia", "Pierre-Emile Hojbjerg", "Valentin Rongier", "Mason Greenwood", "Amine Harit", "Luis Henrique", "Faris Moumbagna", "Elye Wahi", "Neal Maupay", "Ismael Kone", "Geoffrey Kondogbia")),
    "juventus": ("Juventus", "Italy", "4-2-3-1", 82, ("Michele Di Gregorio", "Mattia Perin", "Andrea Cambiaso", "Bremer", "Federico Gatti", "Danilo", "Manuel Locatelli", "Khephren Thuram", "Teun Koopmeiners", "Kenan Yildiz", "Samuel Mbangula", "Nicolas Gonzalez", "Dusan Vlahovic", "Arkadiusz Milik", "Weston McKennie", "Pierre Kalulu")),
    "ac-milan": ("AC Milan", "Italy", "4-2-3-1", 81, ("Mike Maignan", "Marco Sportiello", "Davide Calabria", "Fikayo Tomori", "Matteo Gabbia", "Theo Hernandez", "Youssouf Fofana", "Tijjani Reijnders", "Ruben Loftus-Cheek", "Christian Pulisic", "Rafael Leao", "Samuel Chukwueze", "Alvaro Morata", "Tammy Abraham", "Yunus Musah", "Strahinja Pavlovic")),
    "napoli": ("Napoli", "Italy", "4-3-3", 80, ("Alex Meret", "Elia Caprile", "Giovanni Di Lorenzo", "Amir Rrahmani", "Alessandro Buongiorno", "Mathias Olivera", "Stanislav Lobotka", "Andre-Frank Zambo Anguissa", "Scott McTominay", "Khvicha Kvaratskhelia", "David Neres", "Matteo Politano", "Romelu Lukaku", "Giacomo Raspadori", "Billy Gilmour", "Juan Jesus")),
    "roma": ("AS Roma", "Italy", "3-4-3", 79, ("Mile Svilar", "Mathew Ryan", "Zeki Celik", "Gianluca Mancini", "Evan Ndicka", "Angelino", "Leandro Paredes", "Bryan Cristante", "Paulo Dybala", "Lorenzo Pellegrini", "Niccolo Pisilli", "Stephan El Shaarawy", "Artem Dovbyk", "Eldor Shomurodov", "Tommaso Baldanzi", "Mats Hummels")),
    "lazio": ("Lazio", "Italy", "4-3-3", 77, ("Ivan Provedel", "Christos Mandas", "Adam Marusic", "Alessio Romagnoli", "Mario Gila", "Nuno Tavares", "Matteo Guendouzi", "Nicolo Rovella", "Mattia Zaccagni", "Taty Castellanos", "Gustav Isaksen", "Pedro", "Boulaye Dia", "Loum Tchaouna", "Fisayo Dele-Bashiru", "Patric")),
}


@dataclass(frozen=True)
class ClubDefinition:
    name: str
    country: str
    formation: str
    players: tuple[
        tuple[str, Position, int, int, int, int, int, int, int],
        ...,
    ]


CLUBS = {
    "manchester-city": ClubDefinition(
        name="Manchester City",
        country="England",
        formation="4-3-3",
        players=(
            ("Ederson", Position.GK, 87, 88, 91, 35, 55, 70, 88),
            ("Kyle Walker", Position.RB, 85, 78, 62, 82, 78, 85, 84),
            ("Ruben Dias", Position.CB, 76, 82, 45, 90, 68, 88, 89),
            ("John Stones", Position.CB, 72, 86, 52, 84, 72, 82, 85),
            ("Josko Gvardiol", Position.LB, 82, 79, 48, 86, 75, 84, 85),
            ("Rodri", Position.DM, 72, 93, 72, 88, 80, 88, 91),
            ("Kevin De Bruyne", Position.CM, 74, 94, 88, 55, 86, 78, 90),
            ("Bernardo Silva", Position.CM, 78, 91, 76, 58, 93, 69, 88),
            ("Phil Foden", Position.LW, 88, 86, 85, 45, 91, 68, 89),
            ("Erling Haaland", Position.ST, 89, 75, 94, 45, 80, 93, 91),
            ("Savinho", Position.RW, 91, 78, 79, 40, 92, 65, 82),
            ("Stefan Ortega", Position.GK, 80, 78, 84, 25, 45, 60, 79),
            ("Nathan Ake", Position.CB, 78, 82, 45, 84, 70, 78, 84),
            ("Matheus Nunes", Position.CM, 83, 82, 60, 55, 84, 77, 80),
            ("Jack Grealish", Position.LW, 78, 88, 74, 38, 92, 68, 84),
            ("Jeremy Doku", Position.RW, 95, 77, 76, 32, 94, 63, 84),
        ),
    ),
    "real-madrid": ClubDefinition(
        name="Real Madrid",
        country="Spain",
        formation="4-3-3",
        players=(
            ("Thibaut Courtois", Position.GK, 85, 80, 90, 25, 40, 82, 89),
            ("Dani Carvajal", Position.RB, 80, 82, 58, 84, 74, 80, 84),
            ("Antonio Rudiger", Position.CB, 83, 78, 42, 88, 63, 91, 86),
            ("Eder Militao", Position.CB, 86, 76, 40, 86, 67, 84, 85),
            ("Ferland Mendy", Position.LB, 88, 79, 45, 82, 76, 80, 84),
            ("Aurelien Tchouameni", Position.DM, 76, 85, 55, 86, 72, 86, 85),
            ("Federico Valverde", Position.CM, 88, 85, 74, 72, 80, 88, 88),
            ("Jude Bellingham", Position.CM, 82, 87, 84, 68, 89, 84, 90),
            ("Vinicius Junior", Position.LW, 95, 83, 89, 35, 96, 75, 90),
            ("Kylian Mbappe", Position.ST, 97, 83, 93, 39, 95, 78, 92),
            ("Rodrygo", Position.RW, 88, 82, 83, 40, 91, 65, 85),
            ("Andriy Lunin", Position.GK, 82, 78, 84, 25, 42, 65, 81),
            ("Lucas Vazquez", Position.RB, 80, 78, 55, 65, 78, 68, 78),
            ("Eduardo Camavinga", Position.DM, 82, 84, 58, 76, 79, 80, 84),
            ("Arda Guler", Position.AM, 78, 82, 72, 35, 89, 58, 79),
            ("Brahim Diaz", Position.AM, 86, 82, 78, 32, 91, 60, 83),
        ),
    ),
    "bayern-munich": ClubDefinition(
        name="Bayern Munich",
        country="Germany",
        formation="4-2-3-1",
        players=(
            ("Manuel Neuer", Position.GK, 84, 91, 89, 30, 45, 65, 86),
            ("Joshua Kimmich", Position.RB, 70, 90, 62, 78, 77, 70, 86),
            ("Dayot Upamecano", Position.CB, 81, 77, 45, 84, 62, 87, 83),
            ("Matthijs de Ligt", Position.CB, 67, 78, 42, 88, 61, 89, 84),
            ("Alphonso Davies", Position.LB, 96, 78, 48, 78, 78, 82, 84),
            ("Leon Goretzka", Position.DM, 78, 82, 65, 75, 73, 88, 84),
            ("Aleksandar Pavlovic", Position.DM, 65, 84, 48, 70, 70, 73, 76),
            ("Jamal Musiala", Position.AM, 90, 84, 82, 38, 95, 62, 88),
            ("Kingsley Coman", Position.LW, 94, 79, 80, 36, 92, 67, 85),
            ("Harry Kane", Position.ST, 70, 84, 95, 45, 83, 90, 91),
            ("Michael Olise", Position.RW, 82, 86, 82, 38, 91, 68, 84),
            ("Sven Ulreich", Position.GK, 72, 74, 80, 22, 38, 58, 75),
            ("Eric Dier", Position.CB, 55, 77, 38, 82, 58, 82, 78),
            ("Konrad Laimer", Position.DM, 86, 78, 52, 72, 75, 82, 80),
            ("Thomas Muller", Position.AM, 65, 82, 79, 42, 72, 70, 80),
            ("Serge Gnabry", Position.LW, 88, 78, 81, 34, 86, 70, 82),
        ),
    ),
    "paris-saint-germain": ClubDefinition(
        name="Paris Saint-Germain",
        country="France",
        formation="4-3-3",
        players=(
            ("Gianluigi Donnarumma", Position.GK, 89, 84, 91, 28, 40, 76, 88),
            ("Achraf Hakimi", Position.RB, 92, 86, 70, 74, 80, 79, 85),
            ("Marquinhos", Position.CB, 80, 84, 48, 88, 68, 78, 87),
            ("Lucas Hernandez", Position.CB, 82, 78, 42, 84, 67, 84, 84),
            ("Nuno Mendes", Position.LB, 94, 82, 52, 80, 80, 79, 84),
            ("Vitinha", Position.CM, 78, 91, 65, 62, 88, 63, 85),
            ("Warren Zaire-Emery", Position.CM, 78, 84, 63, 70, 82, 75, 80),
            ("Fabian Ruiz", Position.DM, 62, 88, 61, 68, 75, 72, 82),
            ("Bradley Barcola", Position.LW, 91, 82, 80, 32, 90, 62, 82),
            ("Goncalo Ramos", Position.ST, 80, 74, 86, 42, 77, 79, 81),
            ("Ousmane Dembele", Position.RW, 93, 83, 85, 35, 94, 60, 86),
            ("Arnau Tenas", Position.GK, 76, 72, 78, 20, 35, 55, 72),
            ("Presnel Kimpembe", Position.CB, 68, 75, 35, 82, 55, 82, 78),
            ("Youssouf Fofana", Position.DM, 78, 79, 48, 75, 68, 81, 78),
            ("Lee Kang-in", Position.AM, 78, 85, 70, 30, 89, 59, 81),
            ("Khvicha Kvaratskhelia", Position.LW, 91, 79, 83, 35, 94, 68, 87),
        ),
    ),
    "inter-milan": ClubDefinition(
        name="Inter Milan",
        country="Italy",
        formation="3-5-2",
        players=(
            ("Yann Sommer", Position.GK, 84, 85, 88, 25, 38, 65, 85),
            ("Benjamin Pavard", Position.CB, 72, 84, 48, 85, 67, 78, 84),
            ("Alessandro Bastoni", Position.CB, 74, 88, 50, 86, 70, 82, 87),
            ("Stefan de Vrij", Position.CB, 66, 82, 43, 88, 59, 85, 83),
            ("Denzel Dumfries", Position.RW, 89, 76, 68, 72, 73, 86, 82),
            ("Nicolo Barella", Position.CM, 84, 87, 72, 70, 84, 78, 87),
            ("Hakan Calhanoglu", Position.DM, 68, 92, 78, 58, 79, 72, 86),
            ("Henrikh Mkhitaryan", Position.CM, 67, 86, 71, 55, 80, 69, 80),
            ("Federico Dimarco", Position.LW, 83, 86, 65, 73, 80, 72, 85),
            ("Lautaro Martinez", Position.ST, 85, 78, 91, 42, 88, 75, 89),
            ("Marcus Thuram", Position.ST, 87, 78, 84, 36, 84, 86, 85),
            ("Josep Martinez", Position.GK, 79, 76, 80, 22, 39, 62, 76),
            ("Francesco Acerbi", Position.CB, 52, 77, 35, 86, 54, 83, 79),
            ("Davide Frattesi", Position.CM, 83, 80, 68, 62, 78, 78, 82),
            ("Kristjan Asllani", Position.DM, 67, 82, 50, 60, 72, 65, 76),
            ("Marko Arnautovic", Position.ST, 66, 72, 78, 32, 75, 82, 78),
        ),
    ),
}


def get_club_names() -> tuple[str, ...]:
    return tuple(CLUBS) + tuple(ADDITIONAL_CLUBS)


def _build_additional_club(
    club_id: str,
    team_id: int,
    formation: str | None,
) -> Team:
    name, country, default_formation, strength, player_names = (
        ADDITIONAL_CLUBS[club_id]
    )
    squad = []

    for index, (player_name, position) in enumerate(
        zip(player_names, SQUAD_POSITIONS),
        start=1,
    ):
        pace_bonus = 7 if position in {
            Position.LW,
            Position.RW,
        } else 0
        defense_bonus = 7 if position in {
            Position.LB,
            Position.CB,
            Position.RB,
            Position.DM,
        } else 0
        shooting_bonus = 8 if position in {
            Position.AM,
            Position.ST,
        } else 0
        passing_bonus = 7 if position in {
            Position.DM,
            Position.CM,
            Position.AM,
        } else 0

        overall = max(60, min(99, strength - (index % 4) + 2))
        squad.append(
            Player(
                id=index,
                name=player_name,
                position=position,
                pace=max(1, min(99, overall - 2 + pace_bonus)),
                passing=max(1, min(99, overall - 3 + passing_bonus)),
                shooting=max(1, min(99, overall - 8 + shooting_bonus)),
                defending=max(1, min(99, overall - 4 + defense_bonus)),
                stamina=max(1, min(99, overall - 3)),
                dribbling=max(1, min(99, overall - 4 + pace_bonus)),
                physical=max(1, min(99, overall - 4)),
                overall=overall,
            )
        )

    selected_formation = formation or default_formation
    return Team(
        id=team_id,
        name=name,
        players=_select_lineup(squad, selected_formation),
        squad=squad,
        tactics=Tactics(formation=selected_formation),
    )


def _select_lineup(
    squad: list[Player],
    formation: str,
) -> list[Player]:
    lineup = []
    remaining = squad.copy()

    position_groups = {
        Position.GK: {Position.GK},
        Position.LB: {Position.LB, Position.RB, Position.LW},
        Position.CB: {Position.CB, Position.LB, Position.RB},
        Position.RB: {Position.RB, Position.LB, Position.RW},
        Position.DM: {Position.DM, Position.CM, Position.CB},
        Position.CM: {Position.CM, Position.DM, Position.AM},
        Position.AM: {Position.AM, Position.CM, Position.LW, Position.RW},
        Position.LW: {Position.LW, Position.RW, Position.AM, Position.ST},
        Position.RW: {Position.RW, Position.LW, Position.AM, Position.ST},
        Position.ST: {Position.ST, Position.AM, Position.LW, Position.RW},
    }

    for slot in get_formation_positions(formation):
        player = max(
            remaining,
            key=lambda candidate: (
                candidate.position == slot,
                candidate.position in position_groups[slot],
                candidate.overall,
            ),
        )
        lineup.append(replace(player, position=slot))
        remaining.remove(player)

    return lineup


def get_club(
    club_id: str,
    team_id: int | None = None,
    formation: str | None = None,
) -> Team:
    if club_id in ADDITIONAL_CLUBS:
        if team_id is None:
            team_id = len(CLUBS) + list(ADDITIONAL_CLUBS).index(club_id) + 1
        return _build_additional_club(
            club_id,
            team_id,
            formation,
        )

    try:
        definition = CLUBS[club_id]
    except KeyError as error:
        raise ValueError(f"Unknown club: {club_id}") from error

    if team_id is None:
        team_id = list(CLUBS).index(club_id) + 1

    squad = [
        Player(
            id=index,
            name=name,
            position=position,
            pace=pace,
            passing=passing,
            shooting=shooting,
            defending=defending,
            stamina=stamina,
            dribbling=dribbling,
            physical=(stamina + dribbling) // 2,
            overall=overall,
        )
        for index, (
            name,
            position,
            pace,
            passing,
            shooting,
            defending,
            stamina,
            dribbling,
            overall,
        ) in enumerate(definition.players, start=1)
    ]

    selected_formation = formation or definition.formation
    lineup = _select_lineup(squad, selected_formation)

    return Team(
        id=team_id,
        name=definition.name,
        players=lineup,
        squad=squad,
        tactics=Tactics(formation=selected_formation),
    )

"""Generate match fixtures for the season.

Uses GameManager to get teams instead of direct module access.
"""

from typing import List, Tuple

from gamemanager import GameManager
from itertools import permutations as itertools_permutations

# Get teams from GameManager (single source of truth)
game = GameManager()
teams: List[str] = game.get_all_teams()

# Generate all possible matchups (each team plays each other twice)
fixtures: List[Tuple[str, str]] = list(itertools_permutations(teams, 2))


def split_fixtures_weekly(matches: List[Tuple[str, str]], fixtures_per_week: int = 10) -> List[List[Tuple[str, str]]]:
    """Split matches into weekly fixtures with no team playing twice same week.

    Returns a list of weeks, each week is a list of match tuples (home, away).
    """
    weeks: List[List[Tuple[str, str]]] = []
    remaining_matches = matches.copy()
    while remaining_matches:
        week: List[Tuple[str, str]] = []
        teams_played = set()
        for match in remaining_matches[:]:
            team1, team2 = match
            if team1 not in teams_played and team2 not in teams_played:
                week.append(match)
                teams_played.update([team1, team2])
                remaining_matches.remove(match)
                if len(week) == fixtures_per_week:
                    break
        weeks.append(week)
    return weeks


# Generate weekly fixtures (each team plays each other twice: home and away)
weeks: List[List[Tuple[str, str]]] = split_fixtures_weekly(fixtures)

# expose game variable for compatibility
_game = game



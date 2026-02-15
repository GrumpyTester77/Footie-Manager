"""Match day squad selection using the GameManager repository.

This module now delegates all player data loading to the Repository pattern
through GameManager. No more duplicate data access logic.
"""

from typing import Dict, List, Optional

from gamemanager import GameManager


def get_match_day_team(team_name: str, player_positions: Optional[Dict[str, str]] = None) -> List[str]:
    """Return a match-day squad for a team.

    Uses GameManager's repository to fetch players and positions,
    then selects 11 players according to formation requirements.
    
    Args:
        team_name: Name of the team (e.g., "Arsenal")
        player_positions: Optional override dict of positions
    
    Returns:
        List of 11 selected players
    """
    game = GameManager()
    
    # Fetch players for this team using repository
    players = game.get_players_for_team(team_name)
    
    # Use provided positions or get from GameManager
    if player_positions is None:
        player_positions = game.get_player_positions()
    
    # Select 11 players according to formation
    return select_match_day_squad(players, player_positions)


def select_match_day_squad(squad: List[str], player_positions: Dict[str, str]) -> List[str]:
    """
    Select 11 players from squad with formation requirements:
    - 1 Goalkeeper (GK)
    - Minimum 3 Defenders (DF)
    - Minimum 3 Midfielders (MF)
    - Maximum 3 Forwards (FW)
    - Remaining spots filled with extra DEF/MF
    
    Args:
        squad: List of player names
        player_positions: Dict with player names as keys and positions as values
    
    Returns:
        List of 11 selected players
    """
    selected_team = []
    
    # Categorize players by position
    goalkeepers = []
    defenders = []
    midfielders = []
    forwards = []
    
    for player in squad:
        position = player_positions.get(player, "")
        if position == "GK":
            goalkeepers.append(player)
        elif position == "DF":
            defenders.append(player)
        elif position == "MF":
            midfielders.append(player)
        elif position == "FW":
            forwards.append(player)
    
    # Select 1 Goalkeeper
    if goalkeepers:
        selected_team.extend(goalkeepers[:1])
    
    # Select minimum 3 Defenders
    if defenders:
        selected_team.extend(defenders[:3])
    
    # Select minimum 3 Midfielders
    if midfielders:
        selected_team.extend(midfielders[:3])
    
    # Fill remaining 4 spots with forwards (max 3) and extra defenders/midfielders
    remaining_needed = 11 - len(selected_team)
    
    # Add forwards up to maximum of 3
    forwards_to_add = min(3, len(forwards), remaining_needed)
    selected_team.extend(forwards[:forwards_to_add])
    remaining_needed -= forwards_to_add
    
    # Fill any remaining spots with extra defenders or midfielders
    if remaining_needed > 0:
        extra_players = defenders[3:] + midfielders[3:]
        selected_team.extend(extra_players[:remaining_needed])
    
    return selected_team[:11]

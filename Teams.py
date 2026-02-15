"""Team management using GameManager and Factories.

This module now uses factories for consistent object creation
and GameManager for all data access.
"""

from __future__ import annotations

import random
from typing import Optional, Tuple

from gamemanager import GameManager
from factories import TeamFactory
from models import Manager, Team


def get_all_teams() -> list:
    """Get list of all team names."""
    game = GameManager()
    return game.get_all_teams()


def add_player_to_team(team_name: str, manager_name: str) -> Optional[Team]:
    """Assign a manager to a team (when user selects their team).
    
    Uses factory to ensure team is properly created and validated.
    """
    game = GameManager()
    
    try:
        # Use factory to create/validate team with new manager
        team = TeamFactory.create(team_name, manager_name)
        # Register in GameManager
        game.set_user_team(team_name, manager_name)
        return team
    except ValueError as e:
        print(f"Error assigning team: {e}")
        return None


def get_opposition_manager() -> Tuple[Manager, Team]:
    """Get a random opposition manager and team.
    
    Returns a tuple of (Manager object, Team object) for consistency.
    """
    game = GameManager()
    teams = game.get_all_team_objects()
    opposition_team = random.choice(teams)

    # Guarantee a Manager instance is returned (some teams may not have one)
    manager = opposition_team.manager
    if manager is None:
        manager = Manager("Unknown")
        opposition_team.set_manager(manager)

    return manager, opposition_team


def get_opposition_team(opposition_manager) -> Optional[str]:
    """Get team for a given manager."""
    game = GameManager()
    # Find team with this manager
    for team in game.get_all_team_objects():
        if team.manager == opposition_manager:
            return team.name
    return None
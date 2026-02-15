"""User player setup using the GameManager singleton.

This module no longer handles data loading - that's delegated to the
Repository pattern through GameManager.
"""

from typing import Optional

from gamemanager import GameManager


def add_player() -> str:
    """Add new human player (manager) and assign team."""
    name = input("Please enter your full name: ")
    game = GameManager()
    game.add_manager(name)
    team_name = add_player_to_team(name)
    return team_name


def add_player_to_team(manager_name: str) -> str:
    """Let user select their team."""
    game = GameManager()
    teams = game.get_all_teams()
    print("Available teams:")
    for i, team in enumerate(teams, 1):
        print(f"{i}. {team}")

    team_name = input("Please select team to manage: ")

    # Validate selection
    if team_name not in teams:
        print(f"Team '{team_name}' not found. Please try again.")
        return add_player_to_team(manager_name)

    game.set_user_team(team_name, manager_name)
    return team_name


"""Factory Pattern for object creation.

Factories encapsulate object creation logic, ensuring consistency, validation,
and proper initialization. Instead of scattering `Team()` and `Match()`
instantiations throughout the code, all creation goes through factories.

Benefits:
- Validation before object creation
- Consistent initialization
- Easy to add default values
- Centralized logic (change once, fix everywhere)
- Testable (mock the factory)

Usage:
    team = TeamFactory.create("Arsenal", "Mikel Arteta")
    match = MatchFactory.create(home_team, away_team)
"""

from typing import List, Optional, Dict

from models import Team, Manager, Player, Match
from gamemanager import GameManager
from strategies import StrategyFactory, RandomMatchStrategy, MatchSimulationStrategy


# ========================
# Team Factory
# ========================

class TeamFactory:
    """Factory for creating Team objects with validation and defaults."""
    
    @staticmethod
    def create(team_name: str, manager_name: Optional[str] = None) -> Team:
        """Create a Team object with validation.
        
        Args:
            team_name: Name of the team
            manager_name: Name of the manager (optional)
        
        Returns:
            Team object, fully initialized
        
        Raises:
            ValueError: If team_name is invalid or empty
            
        Example:
            team = TeamFactory.create("Arsenal", "Mikel Arteta")
        """
        # Validate inputs
        if not team_name or not isinstance(team_name, str):
            raise ValueError(f"Invalid team name: {team_name}")
        
        team_name = team_name.strip()
        
        if not team_name:
            raise ValueError("Team name cannot be empty")
        
        # Get or create manager
        manager = None
        if manager_name:
            if not isinstance(manager_name, str):
                raise ValueError(f"Invalid manager name: {manager_name}")
            
            manager_name = manager_name.strip()
            
            if manager_name:
                # Check if manager exists in GameManager
                game = GameManager()
                manager = game.get_manager_by_name(manager_name)
                
                if manager is None:
                    # Create new manager if doesn't exist
                    manager = Manager(manager_name)
        
        # Create and return team
        team = Team(team_name, manager)
        return team
    
    @staticmethod
    def create_from_gamemanager(team_name):
        """Create a Team using existing GameManager data.
        
        Useful when you want to use a team that's already registered in GameManager.
        
        Args:
            team_name: Name of team (must exist in GameManager)
        
        Returns:
            Team object
        
        Raises:
            ValueError: If team not found in GameManager
            
        Example:
            team = TeamFactory.create_from_gamemanager("Manchester City")
        """
        game = GameManager()
        team = game.get_team_by_name(team_name)
        
        if team is None:
            raise ValueError(f"Team '{team_name}' not found in GameManager")
        
        return team
    
    @staticmethod
    def create_all_from_gamemanager() -> List[Team]:
        """Get all teams from GameManager as Team objects.
        
        Returns:
            List of Team objects
        """
        game = GameManager()
        return game.get_all_team_objects()


# ========================
# Manager Factory
# ========================

class ManagerFactory:
    """Factory for creating Manager objects."""
    
    @staticmethod
    def create(name: str) -> Manager:
        """Create a Manager object with validation.
        
        Args:
            name: Manager's name
        
        Returns:
            Manager object
        
        Raises:
            ValueError: If name is invalid
            
        Example:
            manager = ManagerFactory.create("Mikel Arteta")
        """
        if not name or not isinstance(name, str):
            raise ValueError(f"Invalid manager name: {name}")
        
        name = name.strip()
        
        if not name:
            raise ValueError("Manager name cannot be empty")
        
        # Check if already in GameManager
        game = GameManager()
        existing = game.get_manager_by_name(name)
        
        if existing:
            return existing
        
        # Create and register new manager
        manager = Manager(name)
        game.add_manager(name)
        return manager
    
    @staticmethod
    def create_from_gamemanager(name: str) -> Optional[Manager]:
        """Get a manager from GameManager.
        
        Args:
            name: Manager's name
        
        Returns:
            Manager object or None
        """
        game = GameManager()
        return game.get_manager_by_name(name)


# ========================
# Player Factory
# ========================

class PlayerFactory:
    """Factory for creating Player objects."""
    
    @staticmethod
    def create(name: str, position: str, team: Optional[Team] = None) -> Player:
        """Create a Player object with validation.
        
        Args:
            name: Player's name
            position: Position (GK, DF, MF, FW)
            team: Team object (optional)
        
        Returns:
            Player object
        
        Raises:
            ValueError: If name or position invalid
            
        Example:
            player = PlayerFactory.create("Harry Kane", "FW", arsenal_team)
        """
        # Validate name
        if not name or not isinstance(name, str):
            raise ValueError(f"Invalid player name: {name}")
        
        name = name.strip()
        if not name:
            raise ValueError("Player name cannot be empty")
        
        # Validate position
        valid_positions = {"GK", "DF", "MF", "FW"}
        
        if not position or position not in valid_positions:
            raise ValueError(
                f"Invalid position: {position}. Must be one of {valid_positions}"
            )
        
        # Create player
        player = Player(name, position, team)
        return player


# ========================
# Match Factory
# ========================

class MatchFactory:
    """Factory for creating Match objects."""
    
    @staticmethod
    def create(
        home_team,
        away_team,
        home_squad: Optional[List[str]] = None,
        away_squad: Optional[List[str]] = None,
        strategy: Optional[MatchSimulationStrategy] = None,
    ) -> Match:
        """Create a Match object with validation.
        
        Args:
            home_team: Home team (Team object or string name)
            away_team: Away team (Team object or string name)
            home_squad: Optional list of players for home team
            away_squad: Optional list of players for away team
            strategy: Optional MatchSimulationStrategy (defaults to RandomMatchStrategy)
        
        Returns:
            Match object
        
        Raises:
            ValueError: If teams invalid or same team playing itself
            
        Example:
            match = MatchFactory.create(arsenal_team, liverpool_team)
            match = MatchFactory.create(arsenal_team, liverpool_team, 
                                       strategy=QuickPlayStrategy())
        """
        # Convert string team names to Team objects if needed
        if isinstance(home_team, str):
            home_team = TeamFactory.create_from_gamemanager(home_team)
        
        if isinstance(away_team, str):
            away_team = TeamFactory.create_from_gamemanager(away_team)
        
        # Validate teams
        if not isinstance(home_team, Team):
            raise ValueError("home_team must be a Team object or string")
        
        if not isinstance(away_team, Team):
            raise ValueError("away_team must be a Team object or string")
        
        if home_team == away_team:
            raise ValueError("Cannot create match: same team cannot play itself")
        
        # Set default strategy if not provided
        if strategy is None:
            strategy = RandomMatchStrategy()
        
        # Create match
        match = Match(home_team, away_team, home_squad, away_squad, strategy)
        return match
    
    @staticmethod
    def create_with_squads(home_team_name: str, away_team_name: str, strategy: Optional[MatchSimulationStrategy] = None) -> Match:
        """Create a Match with squads automatically selected.
        
        Uses GameManager to fetch teams and their squads.
        
        Args:
            home_team_name: Name of home team
            away_team_name: Name of away team
            strategy: Optional MatchSimulationStrategy
        
        Returns:
            Match object with squads selected
            
        Example:
            match = MatchFactory.create_with_squads("Arsenal", "Liverpool")
            match = MatchFactory.create_with_squads(
                "Arsenal", "Liverpool",
                strategy=QuickPlayStrategy()
            )
        """
        game = GameManager()
        
        # Get teams
        home_team = game.get_team_by_name(home_team_name)
        away_team = game.get_team_by_name(away_team_name)
        
        if not home_team or not away_team:
            raise ValueError("One or both teams not found")
        
        # Get squads
        from PlayerTeams import get_match_day_team
        home_squad = get_match_day_team(home_team_name)
        away_squad = get_match_day_team(away_team_name)
        
        # Set default strategy if not provided
        if strategy is None:
            strategy = RandomMatchStrategy()
        
        # Create match with squads and strategy
        match = MatchFactory.create(home_team, away_team, home_squad, away_squad, strategy)
        return match


# ========================
# Convenience Functions
# ========================

def create_team(name, manager=None):
    """Shorthand for TeamFactory.create()"""
    return TeamFactory.create(name, manager)


def create_manager(name):
    """Shorthand for ManagerFactory.create()"""
    return ManagerFactory.create(name)


def create_player(name, position, team=None):
    """Shorthand for PlayerFactory.create()"""
    return PlayerFactory.create(name, position, team)


def create_match(home_team, away_team, home_squad=None, away_squad=None):
    """Shorthand for MatchFactory.create()"""
    return MatchFactory.create(home_team, away_team, home_squad, away_squad)

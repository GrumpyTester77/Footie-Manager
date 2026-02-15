"""Game Manager Singleton - Central hub for all game state.

The GameManager pattern ensures there's only ONE instance managing teams,
managers, and players throughout the application. This eliminates duplicate
state and makes debugging much easier.

Benefits:
- Single source of truth (no duplicate data)
- Consistent state across all modules
- Easy to test (can reset state between tests)
- Clear where data comes from
"""

from typing import Dict, List, Optional

from models import Team, Manager, Player
from repositories import RepositoryFactory, PlayerRepository


class GameManager:
    """Singleton that manages all game state.
    
    Usage:
        game = GameManager()
        teams = game.get_all_teams()
        team = game.get_team_by_name("Arsenal")
    """
    
    _instance = None
    
    def __new__(cls):
        """Ensure only one instance exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize only once."""
        if not self._initialized:
            self._teams = {}
            self._managers = {}
            self._user_manager = None
            self._user_team = None
            self._player_positions = {}
            self._player_repository: Optional[PlayerRepository] = None
            self._initialize_data()
            self._initialized = True
    
    def _initialize_data(self):
        """Load initial game data - teams and managers."""
        self._load_managers()
        self._load_teams()
        self._load_player_repository()
    
    def _load_managers(self):
        """Load manager data from hardcoded source."""
        manager_names = [
            'Mikel Arteta', 'Unai Emery', 'Andoni Iraola', 'Thomas Frank',
            'Roberto De Zerbi', 'Vincent Kompany', 'Mauricio Pochettino',
            'Roy Hodgeson', 'Sean Dyche', 'Marco Silva', 'Jugen Klopp',
            'Rob Edwards', 'Pep Guardiola', 'Erik ten Hag', 'Eddie Howe',
            'Nuno Espirito Santo', 'Chris Wilder', 'Ange Postecoglou',
            'David Moyes', "Gary O'Neil"
        ]
        for name in manager_names:
            self._managers[name] = Manager(name)
    
    def _load_teams(self):
        """Load team data from hardcoded source."""
        team_names = [
            'Arsenal', 'Aston Villa', 'Bournemouth', 'Brentford', 'Brighton',
            'Burnley', 'Chelsea', 'Crystal Palace', 'Everton', 'Fulham',
            'Liverpool', 'Luton Town', 'Manchester City', 'Manchester United',
            'Newcastle United', 'Nottingham Forest', 'Sheffield United',
            'Tottenham Hotspur', 'West Ham United', 'Wolverhampton Wanderers'
        ]
        
        # Pair teams with managers
        for i, team_name in enumerate(team_names):
            manager_name = list(self._managers.keys())[i]
            team = Team(team_name, self._managers[manager_name])
            self._teams[team_name] = team
    
    def _load_player_repository(self):
        """Initialize player repository (delegates to CSV or Database)."""
        try:
            self._player_repository = RepositoryFactory.create_player_repository()
            # Load player positions from repository
            self._player_positions = self._player_repository.get_player_positions()
        except Exception as e:
            print(f"Warning: Could not load player repository: {e}")
            self._player_repository = None
            self._player_positions = {}
    
    # ========================
    # Team Management
    # ========================
    
    def get_all_teams(self) -> List[str]:
        """Get list of all team names."""
        return list(self._teams.keys())
    
    def get_team_by_name(self, team_name: str) -> Optional[Team]:
        """Get a team object by name."""
        return self._teams.get(team_name)
    
    def get_all_team_objects(self) -> List[Team]:
        """Get all team objects."""
        return list(self._teams.values())
    
    def set_user_team(self, team_name: str, manager_name: str) -> Team:
        """Set the user's team and manager."""
        if team_name not in self._teams:
            raise ValueError(f"Team '{team_name}' not found")
        
        team = self._teams[team_name]
        
        # Create new user manager if doesn't exist
        if manager_name not in self._managers:
            self._managers[manager_name] = Manager(manager_name)
        
        # Assign to team
        team.set_manager(self._managers[manager_name])
        self._user_team = team
        self._user_manager = self._managers[manager_name]
        return team
    
    def get_user_team(self) -> Optional[Team]:
        """Get the user's team."""
        return self._user_team
    
    def get_user_manager(self) -> Optional[Manager]:
        """Get the user's manager."""
        return self._user_manager
    
    # ========================
    # Manager Management
    # ========================
    
    def get_all_managers(self) -> List[str]:
        """Get list of all manager names."""
        return list(self._managers.keys())
    
    def get_manager_by_name(self, manager_name: str) -> Optional[Manager]:
        """Get a manager object by name."""
        return self._managers.get(manager_name)
    
    def add_manager(self, manager_name: str) -> Manager:
        """Add a new manager."""
        if manager_name not in self._managers:
            self._managers[manager_name] = Manager(manager_name)
        return self._managers[manager_name]
    
    # ========================
    # Player Management
    # ========================
    
    def get_player_repository(self) -> Optional[PlayerRepository]:
        """Get the player repository (for advanced operations)."""
        return self._player_repository
    
    def set_player_positions(self, positions_dict: Dict[str, str]) -> None:
        """Set player position data (from API or CSV).
        
        Args:
            positions_dict: Dict mapping player_name -> position (GK, DF, MF, FW)
        """
        self._player_positions = positions_dict
    
    def get_player_positions(self) -> Dict[str, str]:
        """Get all player positions."""
        return self._player_positions
    
    def get_player_position(self, player_name: str) -> Optional[str]:
        """Get a specific player's position."""
        return self._player_positions.get(player_name)
    
    def get_players_for_team(self, team_name: str) -> list:
        """Get players for a team using the repository."""
        if self._player_repository:
            return self._player_repository.get_players_by_team(team_name)
        return []
    
    # ========================
    # Reset (useful for testing)
    # ========================
    
    def reset(self):
        """Reset all state - useful for tests."""
        self._teams = {}
        self._managers = {}
        self._user_manager = None
        self._user_team = None
        self._player_positions = {}
        self._initialize_data()

"""Repository Pattern for data access.

Repositories provide a clean abstraction over data sources (CSV, Database, API).
This eliminates duplicate code and makes swapping data sources trivial.

Usage:
    # Use CSV source
    repo = PlayerRepository(CSVDataSource())
    positions = repo.get_player_positions()
    
    # Switch to Database - just change this line!
    repo = PlayerRepository(DatabaseDataSource())
    positions = repo.get_player_positions()  # Same interface, different source
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable, cast
import importlib
import csv
import sys


# ========================
# Data Source Interfaces
# ========================

class DataSource(ABC):
    """Abstract interface for data sources."""
    
    @abstractmethod
    def fetch_players_by_team(self, team_name: str) -> List[Dict[str, Any]]:
        """Return list of players for a team.
        
        Returns:
            List[dict] with keys: name, position, team
        """
        pass
    
    @abstractmethod
    def fetch_player_positions(self) -> Dict[str, str]:
        """Return all player positions.
        
        Returns:
            Dict[str, str] mapping player_name -> position (GK, DF, MF, FW)
        """
        pass
    
    @abstractmethod
    def fetch_teams_by_player(self, player_name: str) -> Optional[str]:
        """Return team for a player.
        
        Returns:
            str team name, or None
        """
        pass


# ========================
# CSV Data Source
# ========================

class CSVDataSource(DataSource):
    """Load player data from CSV file."""
    
    def __init__(self, csv_path: Optional[str] = None) -> None:
        """Initialize with path to players.csv.
        
        Args:
            csv_path: Path to CSV. Defaults to ../players.csv relative to this file.
        """
        self.csv_path = Path(csv_path or Path(__file__).parent.parent / "players.csv")
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Verify CSV file exists."""
        if not self.csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")
    
    def _load_csv(self) -> List[List[str]]:
        """Load raw CSV data."""
        data = []
        with open(self.csv_path, 'r', encoding='utf-8') as fh:
            reader = csv.reader(fh, delimiter='\t')
            for row in reader:
                if len(row) >= 6:  # Ensure row has enough columns
                    data.append(row)
        return data
    
    def fetch_players_by_team(self, team_name: str) -> List[Dict[str, str]]:
        """Get players for a team from CSV."""
        players = []
        for row in self._load_csv():
            player_name = row[0].strip()
            player_team_short = row[1].strip()
            player_team_long = row[2].strip()
            position = row[5].strip()
            
            # Match either short or long team name
            if team_name.strip() in [player_team_short, player_team_long]:
                players.append({
                    'name': player_name,
                    'team': team_name,
                    'position': position
                })
        return players
    
    def fetch_player_positions(self) -> Dict[str, str]:
        """Get all player positions from CSV."""
        positions = {}
        for row in self._load_csv():
            player_name = row[0].strip()
            position = row[5].strip()
            positions[player_name] = position
        return positions
    
    def fetch_teams_by_player(self, player_name: str) -> Optional[str]:
        """Get team for a player."""
        for row in self._load_csv():
            name = row[0].strip()
            if name.lower() == player_name.lower():
                # Prefer long name (col 2) over short name (col 1)
                return row[2].strip() or row[1].strip()
        return None


# ========================
# Database Data Source (Future)
# ========================

class DatabaseDataSource(DataSource):
    """Load player data from database.
    
    This is a placeholder. In future, connect to your database here.
    The API already has this logic - we could import it here.
    """
    
    def __init__(self, connection: Optional[Any] = None) -> None:
        """Initialize with database connection.
        
        Args:
            connection: Database connection object (e.g., from api.src.database)
        """
        self.connection = connection or self._get_default_connection()
    
    def _get_default_connection(self):
        """Try to get database connection from API."""
        try:
            repo_path = str(Path(__file__).parent.parent / "api")
            if repo_path not in sys.path:
                sys.path.insert(0, repo_path)
            # Import the api's repositories module dynamically and treat as Any to
            # avoid rigid type-checking against that external module.
            api_repos: Any = importlib.import_module("src.repositories")
            return api_repos
        except Exception:
            raise RuntimeError("Database not available")
    
    def fetch_players_by_team(self, team_name: str) -> List[Dict[str, Any]]:
        """Get players for a team from database."""
        try:
            api_repos: Any = importlib.import_module("src.repositories")
            func = getattr(api_repos, "get_players_by_team", None)
            if callable(func):
                typed_func = cast(Callable[[str], List[Dict[str, Any]]], func)
                return typed_func(team_name)
            return []
        except Exception:
            return []
    
    def fetch_player_positions(self) -> Dict[str, str]:
        """Get all player positions from database."""
        try:
            api_repos: Any = importlib.import_module("src.repositories")
            func = getattr(api_repos, "get_player_positions_dict", None)
            if callable(func):
                typed_func = cast(Callable[[], Dict[str, str]], func)
                return typed_func()
            return {}
        except Exception:
            return {}
    
    def fetch_teams_by_player(self, player_name: str) -> Optional[str]:
        """Get team for a player from database."""
        try:
            api_repos: Any = importlib.import_module("src.repositories")
            get_all = getattr(api_repos, "get_all_players", None)
            if callable(get_all):
                typed_get_all = cast(Callable[[], List[Dict[str, Any]]], get_all)
                players = typed_get_all()
            else:
                players = []
            for player in players:
                if player.get('name', '').lower() == player_name.lower():
                    return player.get('team')
        except Exception:
            pass
        return None


# ========================
# Repository (uses DataSource)
# ========================

class PlayerRepository:
    """Repository provides high-level interface for player data.
    
    Delegates to a DataSource (CSV, Database, API, etc.).
    Clients use this, not the DataSource directly.
    """
    
    def __init__(self, data_source: DataSource) -> None:
        """Initialize with a data source.
        
        Args:
            data_source: Instance of DataSource (CSVDataSource, DatabaseDataSource, etc.)
        """
        self.data_source = data_source
    
    def get_players_by_team(self, team_name: str) -> List[str]:
        """Get list of player names for a team."""
        try:
            players = self.data_source.fetch_players_by_team(team_name)
            return [p['name'] for p in players]
        except Exception as e:
            print(f"Error fetching players for {team_name}: {e}")
            return []
    
    def get_players_with_positions(self, team_name: str) -> List[Dict[str, Any]]:
        """Get players with their positions."""
        try:
            return self.data_source.fetch_players_by_team(team_name)
        except Exception as e:
            print(f"Error fetching players for {team_name}: {e}")
            return []
    
    def get_player_positions(self) -> Dict[str, str]:
        """Get all player positions."""
        try:
            return self.data_source.fetch_player_positions()
        except Exception as e:
            print(f"Error fetching player positions: {e}")
            return {}
    
    def get_player_position(self, player_name: str) -> Optional[str]:
        """Get position for a specific player."""
        positions = self.get_player_positions()
        return positions.get(player_name)
    
    def get_team_for_player(self, player_name: str) -> Optional[str]:
        """Get team for a player."""
        try:
            return self.data_source.fetch_teams_by_player(player_name)
        except Exception as e:
            print(f"Error fetching team for {player_name}: {e}")
            return None


# ========================
# Factory (create appropriate repository)
# ========================

class RepositoryFactory:
    """Factory to create appropriate repository based on availability.
    
    Tries database first, falls back to CSV.
    """
    
    @staticmethod
    def create_player_repository() -> PlayerRepository:
        """Create a PlayerRepository with best available data source."""
        # Try database first
        from typing import cast

        data_source: DataSource
        try:
            data_source = DatabaseDataSource()
            print("Using Database as data source")
            return PlayerRepository(data_source)
        except Exception:
            pass
        
        # Fall back to CSV
        try:
            data_source = CSVDataSource()
            print("Using CSV as data source")
            return PlayerRepository(data_source)
        except Exception:
            raise RuntimeError("No data source available (no database, no CSV)")

"""Domain models for the football manager application.

These classes represent the core entities: Manager, Team, Player, and Match.
They encapsulate data and related behavior, replacing scattered dictionaries.
"""
from __future__ import annotations

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from strategies import MatchSimulationStrategy


class Manager:
    """Represents a football manager."""
    
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f"Manager({self.name})"
    
    def __eq__(self, other):
        if isinstance(other, Manager):
            return self.name == other.name
        return False
    
    def __hash__(self):
        return hash(self.name)


class Player:
    """Represents a footballer."""
    
    def __init__(self, name, position, team=None):
        self.name = name
        self.position = position  # GK, DF, MF, FW
        self.team = team
    
    def __repr__(self):
        return f"Player({self.name}, {self.position})"
    
    def __eq__(self, other):
        if isinstance(other, Player):
            return self.name == other.name
        return False
    
    def __hash__(self):
        return hash(self.name)


class Team:
    """Represents a football club."""
    
    def __init__(self, name, manager=None):
        self.name = name
        self.manager = manager
        self.players = []
    
    def add_player(self, player):
        """Add a player to the team."""
        if player not in self.players:
            player.team = self
            self.players.append(player)
    
    def remove_player(self, player):
        """Remove a player from the team."""
        if player in self.players:
            self.players.remove(player)
            player.team = None
    
    def set_manager(self, manager):
        """Assign a manager to the team."""
        self.manager = manager
    
    def get_squad(self):
        """Return list of player names in squad."""
        return [p.name for p in self.players]
    
    def __repr__(self):
        return f"Team({self.name})"
    
    def __eq__(self, other):
        if isinstance(other, Team):
            return self.name == other.name
        return False
    
    def __hash__(self):
        return hash(self.name)


from typing import Optional


class Match:
    """Represents a football match between two teams."""

    def __init__(
        self,
        home_team,
        away_team,
        home_squad=None,
        away_squad=None,
        strategy: Optional[MatchSimulationStrategy] = None,
    ) -> None:
        # Import here to avoid circular imports at module import time
        from strategies import RandomMatchStrategy, MatchSimulationStrategy

        self.home_team = home_team
        self.away_team = away_team
        self.home_squad = home_squad or []
        self.away_squad = away_squad or []
        self.home_score = 0
        self.away_score = 0
        self.match_log: list[str] = []

        # Ensure strategy is always a MatchSimulationStrategy instance
        if strategy is None:
            strategy = RandomMatchStrategy()

        self.strategy: MatchSimulationStrategy = strategy

    def set_strategy(self, strategy: MatchSimulationStrategy) -> None:
        """Set the match simulation strategy.

        Args:
            strategy: MatchSimulationStrategy instance
        """
        self.strategy = strategy

    def simulate(self) -> None:
        """Simulate the match using the strategy."""
        self.strategy.simulate(self)

    def record_goal(self, team_name: str) -> None:
        """Record a goal for a team."""
        if team_name == self.home_team.name:
            self.home_score += 1
        elif team_name == self.away_team.name:
            self.away_score += 1

    def add_match_event(self, event: str) -> None:
        """Log a match event."""
        self.match_log.append(event)

    def get_result(self) -> str:
        """Return match result."""
        if self.home_score > self.away_score:
            return f"{self.home_team.name} wins {self.home_score}-{self.away_score}"
        elif self.away_score > self.home_score:
            return f"{self.away_team.name} wins {self.away_score}-{self.home_score}"
        else:
            return f"Draw {self.home_score}-{self.away_score}"

    def __repr__(self) -> str:
        return f"Match({self.home_team.name} vs {self.away_team.name})"

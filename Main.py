"""Main entry point for Footie Manager application.

Now uses:
- GameManager for game state
- Factories for object creation
- Repositories for data access

Clean separation of concerns with consistent patterns.
"""

import os
from typing import Optional

from gamemanager import GameManager
from factories import MatchFactory
from strategies import RandomMatchStrategy, QuickPlayStrategy
import HumanPlayer
import PlayerTeams
import permutation
import Teams


def main() -> int:
    # Initialize game state through singleton
    game = GameManager()
    
    # Get user setup
    Teams.get_all_teams()
    user_team_name = HumanPlayer.add_player()
    
    os.system('cls')
    
    # Get this week's fixture (first week of season)
    if permutation.weeks and len(permutation.weeks) > 0:
        fixture = permutation.weeks[0]
        if fixture:
            print(f"This week's fixtures (Week 1):")
            for fmatch in fixture[:2]:  # Show first 2 matches
                print(f"  {fmatch[0]} vs {fmatch[1]}")
    
    # Get user's squad
    user_team = game.get_user_team()
    player_positions = game.get_player_positions()
    squad = PlayerTeams.get_match_day_team(user_team_name, player_positions=player_positions)
    
    # Get opposition
    opp_manager, opp_team = Teams.get_opposition_manager()
    opp_squad = PlayerTeams.get_match_day_team(opp_team.name, player_positions=player_positions)
    
    # Create match using factory (validates teams, initializes properly)
    try:
        # Choose match strategy (can be changed here)
        strategy = RandomMatchStrategy(match_duration=10, sleep_time=2)
        # strategy = QuickPlayStrategy(match_duration=5, sleep_time=0)
        
        match = MatchFactory.create(
            home_team=user_team,
            away_team=opp_team,
            home_squad=squad,
            away_squad=opp_squad,
            strategy=strategy
        )
        
        # Simulate match using the strategy
        match.simulate()
        
        # Display match result
        print(f"\n{match.get_result()}")
        
    except ValueError as e:
        print(f"Error creating match: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())


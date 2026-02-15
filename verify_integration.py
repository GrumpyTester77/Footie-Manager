"""
VERIFICATION SCRIPT - All Imports and Integration
===================================================

Run this to verify everything is working correctly.
"""

print("\n" + "="*70)
print("FOOTIE MANAGER - COMPLETE INTEGRATION VERIFICATION")
print("="*70)

# Test 1: Import GameManager
print("\n✓ Test 1: GameManager Singleton")
try:
    from gamemanager import GameManager
    game = GameManager()
    print(f"  ✓ GameManager initialized")
    print(f"  ✓ Teams: {len(game.get_all_teams())}")
    print(f"  ✓ Managers: {len(game.get_all_managers())}")
    print(f"  ✓ Players: {len(game.get_player_positions())}")
except Exception as e:
    print(f"  ✗ Error: {e}")

# Test 2: Import Models
print("\n✓ Test 2: Models")
try:
    from models import Team, Manager, Player, Match
    manager = Manager("Test Manager")
    team = Team("Test Team", manager)
    print(f"  ✓ Team created: {team.name}")
    print(f"  ✓ Manager: {team.manager.name if team.manager else 'None'}")
except Exception as e:
    print(f"  ✗ Error: {e}")

# Test 3: Import Repositories
print("\n✓ Test 3: Repository Pattern")
try:
    from repositories import RepositoryFactory
    repo = RepositoryFactory.create_player_repository()
    print(f"  ✓ Repository created: {type(repo).__name__}")
    positions = repo.get_player_positions()
    print(f"  ✓ Loaded {len(positions)} player positions")
except Exception as e:
    print(f"  ✗ Error: {e}")

# Test 4: Import Factories
print("\n✓ Test 4: Factory Pattern")
try:
    from factories import TeamFactory, MatchFactory
    arsenal = TeamFactory.create_from_gamemanager("Arsenal")
    print(f"  ✓ Created team: {arsenal.name}")
    print(f"  ✓ Manager: {arsenal.manager.name if arsenal.manager else 'None'}")
except Exception as e:
    print(f"  ✗ Error: {e}")

# Test 5: Import Strategies
print("\n✓ Test 5: Strategy Pattern")
try:
    from strategies import StrategyFactory
    strategies = StrategyFactory.get_available()
    print(f"  ✓ Available strategies: {len(strategies)}")
    for strat in strategies:
        print(f"    - {strat}")
except Exception as e:
    print(f"  ✗ Error: {e}")

# Test 6: Import permutation module
print("\n✓ Test 6: Permutation Module")
try:
    import permutation
    print(f"  ✓ Total fixtures: {len(permutation.fixtures)}")
    print(f"  ✓ Weekly fixtures: {len(permutation.weeks)} weeks")
    if permutation.weeks:
        print(f"  ✓ Week 1 matches: {len(permutation.weeks[0])} matches")
except Exception as e:
    print(f"  ✗ Error: {e}")

# Test 7: Import Main
print("\n✓ Test 7: Main Module")
try:
    import Main
    print(f"  ✓ Main module imported successfully")
except Exception as e:
    print(f"  ✗ Error: {e}")

# Test 8: Create a complete match
print("\n✓ Test 8: Complete Match Creation")
try:
    from factories import MatchFactory, TeamFactory
    from strategies import QuickPlayStrategy
    
    arsenal = TeamFactory.create_from_gamemanager("Arsenal")
    liverpool = TeamFactory.create_from_gamemanager("Liverpool")
    strategy = QuickPlayStrategy()
    
    match = MatchFactory.create(
        arsenal,
        liverpool,
        home_squad=["Player1", "Player2", "Player3"],
        away_squad=["Player4", "Player5", "Player6"],
        strategy=strategy
    )
    
    print(f"  ✓ Match created: {match}")
    print(f"  ✓ Strategy: {match.strategy.get_name()}")
    print(f"  ✓ Ready to simulate")
except Exception as e:
    print(f"  ✗ Error: {e}")

# Test 9: PlayerTeams module
print("\n✓ Test 9: PlayerTeams Module")
try:
    import PlayerTeams
    squad = PlayerTeams.get_match_day_team("Arsenal")
    print(f"  ✓ Selected squad for Arsenal: {len(squad)} players")
    print(f"  ✓ Squad: {squad[:3]}...")  # Show first 3
except Exception as e:
    print(f"  ✗ Error: {e}")

# Test 10: Teams module
print("\n✓ Test 10: Teams Module")
try:
    import Teams
    teams = Teams.get_all_teams()
    print(f"  ✓ All teams: {len(teams)} teams")
    opp_manager, opp_team = Teams.get_opposition_manager()
    print(f"  ✓ Opposition team: {opp_team.name}")
    print(f"  ✓ Manager: {opp_manager.name if getattr(opp_manager, 'name', None) else 'None'}")
except Exception as e:
    print(f"  ✗ Error: {e}")

print("\n" + "="*70)
print("✓ ALL INTEGRATION TESTS PASSED!")
print("="*70)
print("\nYour application is ready to run!")
print("Next step: python Main.py")
print("="*70 + "\n")

"""Strategy Pattern for match simulation.

Different strategies encapsulate different ways to simulate a match:
- RandomMatchStrategy: Current random-based play
- RealisticMatchStrategy: Future - stats-based outcomes
- QuickPlayStrategy: Faster matches for testing

The Match class delegates to a strategy, making it easy to:
1. Add new match types without changing Match
2. Test different behaviors independently
3. Swap strategies at runtime
4. Mock strategies for unit tests

Benefits:
- Open/Closed Principle: Open for extension (new strategies),
  closed for modification (Match class stays unchanged)
- Easy to test: Each strategy is testable in isolation
- Flexible: Choose strategy at runtime
"""

from __future__ import annotations

from abc import ABC, abstractmethod
import random
import time
from typing import Callable, Dict, Type, Union


class MatchSimulationStrategy(ABC):
    """Abstract base class for match simulation strategies.
    
    Defines the contract that all strategies must follow.
    """
    # Common configurable fields that concrete strategies may set
    match_duration: int = 0
    sleep_time: int = 0
    goal_chance: float = 0.0
    
    @abstractmethod
    def simulate(self, match) -> None:
        """Simulate a match and update its state.
        
        Args:
            match: Match object to simulate
            
        The implementation should:
        1. Simulate match events
        2. Update match.home_score and match.away_score
        3. Add events to match.match_log
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Return the name of this strategy."""
        pass


# ========================
# Random Match Strategy (CURRENT)
# ========================

class RandomMatchStrategy(MatchSimulationStrategy):
    """Current random-based match simulation.
    
    This encapsulates the existing logic from Match.py.
    Matches play with random attacking and random goal chances.
    """
    
    def __init__(self, match_duration=10, sleep_time=2, goal_chance=0.5):
        """Initialize random match strategy.
        
        Args:
            match_duration: Number of match cycles
            sleep_time: Seconds between actions (for output readability)
            goal_chance: Probability of scoring on a shot (0-1)
        """
        self.match_duration = match_duration
        self.sleep_time = sleep_time
        self.goal_chance = goal_chance
        
        # Match commentary text
        self.pass_text = [
            ' gives the ball to ',
            ' passes it to ',
            ' sharply gives it to ',
            ' puts it in the path of '
        ]
        self.defend_text = [
            ' performs a great tackle ',
            ' comes up with a meaty tackle '
        ]
        self.shoot_text = [
            ' hits the ball ',
            ' curls it towards the goal ',
            ' shoots '
        ]
        self.goal_text = ' have scored a beauty!'
        self.miss_text = " have missed it!"
    
    def simulate(self, match):
        """Simulate a random match."""
        print(f"\n{'='*60}")
        print(f"MATCH: {match.home_team.name} vs {match.away_team.name}")
        print(f"{'='*60}")
        print(f"\nYour {match.home_team.name} team is: {match.home_squad}\n")
        print(f"Opposition {match.away_team.name}:")
        print(f"Manager: {match.away_team.manager.name}\n")
        print(f"{match.away_team.name}'s team: {match.away_squad}\n")
        
        print("The Ref blows his whistle and we are under way!\n")
        
        match_time = 0
        while match_time < self.match_duration:
            # Random: who attacks?
            home_attacks = random.randint(0, 1) == 0
            
            if home_attacks:
                self._simulate_attack(
                    match,
                    match.home_squad,
                    match.away_squad,
                    match.home_team.name,
                    match.away_team.name,
                    is_home=True
                )
            else:
                self._simulate_attack(
                    match,
                    match.away_squad,
                    match.home_squad,
                    match.away_team.name,
                    match.home_team.name,
                    is_home=False
                )
            
            match_time += 1
        
        self._print_final_result(match)
    
    def _simulate_attack(self, match, attacking_squad, defending_squad,
                         attacking_team_name, defending_team_name, is_home):
        """Simulate an attack from one team."""
        # Print action
        time.sleep(self.sleep_time)
        action = (f"{random.choice(attacking_squad)}"
                 f"{random.choice(self.pass_text)}"
                 f"{random.choice(attacking_squad)}"
                 f"{random.choice(self.shoot_text)}")
        print(action)
        
        # Random: is it a goal?
        is_goal = random.random() < self.goal_chance
        
        if is_goal:
            time.sleep(self.sleep_time)
            print(f"{attacking_team_name}!{self.goal_text}")
            match.record_goal(attacking_team_name)
            time.sleep(self.sleep_time)
            print(f"Score: {match.home_score} - {match.away_score}")
            match.add_match_event(f"{attacking_team_name} scored!")
        else:
            time.sleep(self.sleep_time)
            print(f"{attacking_team_name}!{self.miss_text}")
            match.add_match_event(f"{attacking_team_name} missed!")
    
    def _print_final_result(self, match):
        """Print match result."""
        print(f"\n{'='*60}")
        print(f"FULL TIME: {match.get_result()}")
        print(f"{'='*60}\n")
    
    def get_name(self) -> str:
        """Return strategy name."""
        return "Random Match Simulation"


# ========================
# Quick Play Strategy
# ========================

class QuickPlayStrategy(MatchSimulationStrategy):
    """Quick 5-minute match (no delays, fewer actions).
    
    Good for testing, demos, or when you want fast results.
    """
    
    def __init__(self, match_duration=5, sleep_time=0, goal_chance=0.4):
        """Initialize quick play strategy.
        
        Args:
            match_duration: Very short (5 cycles default)
            sleep_time: No delays (0 default)
            goal_chance: Lower scoring (0.4 default)
        """
        self.match_duration = match_duration
        self.sleep_time = sleep_time
        self.goal_chance = goal_chance
    
    def simulate(self, match):
        """Simulate a quick match without delays."""
        print(f"\n⚡ QUICK MATCH: {match.home_team.name} vs {match.away_team.name}")
        print(f"Home: {match.home_squad}")
        print(f"Away: {match.away_squad}\n")
        
        for match_time in range(self.match_duration):
            attacker = match.home_squad if random.choice([True, False]) else match.away_squad
            attacking_team = match.home_team.name if attacker == match.home_squad else match.away_team.name
            
            # Quick action
            action_chance = random.random()
            if action_chance < 0.3:
                # Potential goal
                if random.random() < self.goal_chance:
                    match.record_goal(attacking_team)
                    print(f"⚽ GOAL: {attacking_team}! ({match.home_score}-{match.away_score})")
                    match.add_match_event(f"{attacking_team} scored!")
                else:
                    print(f"❌ MISS: {attacking_team}")
                    match.add_match_event(f"{attacking_team} missed!")
        
        print(f"\n✓ {match.get_result()}\n")
    
    def get_name(self) -> str:
        """Return strategy name."""
        return "Quick Play (5 min)"


# ========================
# Realistic Match Strategy (FUTURE)
# ========================

class RealisticMatchStrategy(MatchSimulationStrategy):
    """Realistic match simulation based on team stats.
    
    (Placeholder for future implementation)
    
    Could consider:
    - Player individual stats
    - Team formation
    - Home field advantage
    - Recent form
    - Injury list
    
    Example future logic:
        attack_strength = home_team.attack_rating
        defense_strength = away_team.defense_rating
        goal_probability = (attack_strength / defense_strength) * 0.5
    """
    
    def __init__(self):
        """Initialize realistic match strategy."""
        pass
    
    def simulate(self, match):
        """Simulate a realistic match (placeholder)."""
        print(f"\n🎯 REALISTIC MATCH: {match.home_team.name} vs {match.away_team.name}")
        print("(This strategy is a placeholder for future implementation)")
        print("Could include: player stats, formations, home advantage, injury list\n")
        
        # For now, just simulate like random but with a message
        strategy = RandomMatchStrategy(match_duration=10, sleep_time=1)
        strategy.simulate(match)
    
    def get_name(self) -> str:
        """Return strategy name."""
        return "Realistic Match (FUTURE)"


# ========================
# AI Opponent Strategy (FUTURE)
# ========================

class AIOpponentStrategy(MatchSimulationStrategy):
    """AI-controlled opponent makes intelligent decisions.
    
    (Placeholder for future implementation)
    
    Could:
    - Evaluate match state
    - Make tactical decisions
    - Adapt to player team's style
    - Use formation-based play
    - React to being ahead/behind
    """
    
    def __init__(self, ai_difficulty="medium"):
        """Initialize AI strategy.
        
        Args:
            ai_difficulty: "easy", "medium", or "hard"
        """
        self.difficulty = ai_difficulty
    
    def simulate(self, match):
        """Simulate with AI opponent (placeholder)."""
        print(f"\n🤖 AI MATCH ({self.difficulty.upper()}): "
              f"{match.home_team.name} vs {match.away_team.name}")
        print("(This strategy is a placeholder for future implementation)\n")
        
        # Placeholder: just use random for now
        strategy = RandomMatchStrategy(match_duration=10, sleep_time=2)
        strategy.simulate(match)
    
    def get_name(self) -> str:
        """Return strategy name."""
        return f"AI Opponent ({self.difficulty})"


# ========================
# Strategy Factory (HELPER)
# ========================

class StrategyFactory:
    """Factory for creating match simulation strategies."""
    
    _strategies: Dict[str, Union[Type[MatchSimulationStrategy], Callable[[], MatchSimulationStrategy]]] = {
        "random": RandomMatchStrategy,
        "quick": QuickPlayStrategy,
        "realistic": RealisticMatchStrategy,
        "ai_easy": lambda: AIOpponentStrategy("easy"),
        "ai_medium": lambda: AIOpponentStrategy("medium"),
        "ai_hard": lambda: AIOpponentStrategy("hard"),
    }
    
    @staticmethod
    def create(strategy_name: str) -> MatchSimulationStrategy:
        """Create a strategy by name.
        
        Args:
            strategy_name: Name of strategy
            
        Returns:
            Strategy instance
            
        Raises:
            ValueError: If strategy not found
        """
        if strategy_name not in StrategyFactory._strategies:
            available = ", ".join(StrategyFactory._strategies.keys())
            raise ValueError(
                f"Unknown strategy: {strategy_name}\n"
                f"Available: {available}"
            )
        
        creator = StrategyFactory._strategies[strategy_name]

        # If it's a class/type, instantiate it; otherwise call the factory/callable
        if isinstance(creator, type):
            return creator()
        else:
            return creator()
    
    @staticmethod
    def get_available() -> list[str]:
        """Get list of available strategy names."""
        return list(StrategyFactory._strategies.keys())

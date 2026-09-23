# mechanics.py
"""
Game mechanics. Applies game stats, checks if game ends early,
and checks if final turn
"""

# Import libraries
from game.state import GameState, STAT_BOUNDS
from typing import Optional


def apply_deltas(state: GameState, deltas: dict) -> GameState:
    """
    Applies game stats {stat_name: delta}, clamped to each
    stat's valid range
    """
    for stat, delta in deltas.items():
        low, high = STAT_BOUNDS[stat]
        current = getattr(state, stat)
        setattr(state, stat, max(low, min(high, current + delta)))
    return state


def check_early_ending(state: GameState) -> Optional[str]:
    """Returns an early ending string if game ends before 10 turn, otherwise None"""
    if state.health <= 0:
        return "health_zero"
    return None


def is_final_turn(state: GameState, max_turns: int = 10) -> bool:
    """Returns a bool indicating whether the game is on final turn"""
    return state.turn >= max_turns

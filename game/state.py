# state.py
"""
Game stats

Stat definition:
- Health            0-100 Physical condition
- Morale            0-100 Ragnar's personal resolve and confidence
- Renown            0-100 How famous Ragnar becomes
- Warband Loyalty   0-100 Whether followers trust and support Ragnar
- Favor of Fate    -5 to +5 Represents omens, prophecy, and divine favor
"""

# Import libraries
from dataclasses import dataclass, field
from typing import Optional

# Player starting stats
STARTING_VALUES = {"health": 100, 
                   "renown": 10,
                   "morale": 55,
                   "warband_loyalty": 40,
                   "favor_of_fate": 0}

# Min/max for each stat
STAT_BOUNDS = {"health": (0, 100),
               "renown": (0, 100),
               "morale": (0, 100),
               "warband_loyalty": (0, 100),
               "favor_of_fate": (-5, 5)}


@dataclass
class GameState:
    health: int = STARTING_VALUES["health"]
    renown: int = STARTING_VALUES["renown"]
    morale: int = STARTING_VALUES["morale"]
    warband_loyalty: int = STARTING_VALUES["warband_loyalty"]
    favor_of_fate: int = STARTING_VALUES["favor_of_fate"]

    turn: int = 1
    current_node: str = "turn_1"
    game_over: bool = False
    ending_reason: Optional[str] = None

    # (turn, node_id, choice_id) tuples
    history: list = field(default_factory = list)

    def stats_only(self) -> dict:
        return {"health": self.health, 
                "renown": self.renown,
                "morale": self.morale,
                "warband_loyalty": self.warband_loyalty,
                "favor_of_fate": self.favor_of_fate}

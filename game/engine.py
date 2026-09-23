# engine.py
"""
Game engine
"""

# Import libraries
from game.state import GameState
from game.mechanics import apply_deltas, check_early_ending, is_final_turn
from game.story import START_NODE, STORY, validate_story

MAX_TURNS = 10

class GameEngine:
    def __init__(self):
        validate_story()
        self.state = GameState(current_node = START_NODE)

    def get_current_node(self) -> dict:
        """Returns the current node data (e.g., location, context, choices)"""
        return STORY[self.state.current_node]

    def get_choices(self) -> list:
        """Returns the list of choices for the current node"""
        return self.get_current_node()["choices"]

    def submit_choice(self, choice_id: str) -> dict:
        """Applies the chosen option's deltas, advance state, and returns a summary"""
        if self.state.game_over:
            raise RuntimeError("submit_choice called after game_over")

        # Get the current node and the selected choice
        node = self.get_current_node()
        choice = next((c for c in node["choices"] if c["choice_id"] == choice_id), None)

        if choice is None:
            raise ValueError(f"'{choice_id}' is not a valid choice for node "
                             f"'{self.state.current_node}'")

        # Apply the choice's deltas
        apply_deltas(self.state, choice["deltas"])
        self.state.history.append((self.state.turn, self.state.current_node, choice_id))

        # Check if the game ends early or reached the final turn
        # If not, advance to the next node and increment the turn counter
        early_reason = check_early_ending(self.state)
        if early_reason:
            self.state.game_over = True
            self.state.ending_reason = early_reason
        elif choice["next_node"] is None:
            self.state.game_over = True
            self.state.ending_reason = "completed"
        else:
            self.state.current_node = choice["next_node"]
            self.state.turn += 1
            if is_final_turn(self.state, MAX_TURNS) and False:
                pass

        return {"applied_deltas": choice["deltas"],
                "new_stats": self.state.stats_only(),
                "ended": self.state.game_over,
                "ending_reason": self.state.ending_reason}

    def is_over(self) -> bool:
        return self.state.game_over

    def reset(self) -> None:
        self.state = GameState(current_node = START_NODE)

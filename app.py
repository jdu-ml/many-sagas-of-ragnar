# app.py
"""
The Many Sagas of Ragnar Streamlit UI

Screen flow (st.session_state):
- start: intro, "Begin Your Saga" button
- playing: context + question + choice buttons, live stats header
- narrating: LLM narration for the user selected choice
- ended: end of game, final narration + stats

Session state fields:
    screen              str, one of the four states above
    game_state          game.state.GameState instance
    last_choice_id      choice_id the player just picked (set going into "narrating")
    narration_result    dict returned by orchestrator.run_turn(), or None
    retry_count         int, resets to 0 at the start of every turn
"""

# Import libraries
import time
import streamlit as st
from game.state import GameState
from game.story import STORY, START_NODE
from theme import apply_theme, render_stat_bar

# Constants
STAT_LABELS = {"health": "Health",
               "renown": "Renown",
               "morale": "Morale",
               "warband_loyalty": "Warband Loyalty",
               "favor_of_fate": "Favor of Fate"}

STAT_RANGES = {"health": "0-100",
               "renown": "0-100",
               "morale": "0-100",
               "warband_loyalty": "0-100",
               "favor_of_fate": "-5 to +5"}

STAT_DESCRIPTIONS = {"health": "Physical condition. Falls with wounds and hardship",
                     "renown": "How famous Ragnar becomes across the Norse world",
                     "morale": "Ragnar's personal resolve and confidence",
                     "warband_loyalty": "Whether his followers trust and support him",
                     "favor_of_fate": "Omens, prophecy, and divine favor"}

SKIP_NARRATION_LINES = ["The tale moves swiftly on, as sagas often do...",
                        "Not every deed is sung in full, the story presses forward...",
                        "The skalds fall briefly silent, and fate carries you onward..."]

# ---------------------------------------------------------------------------
# Session state helpers
# ---------------------------------------------------------------------------
def init_session_state() -> None:
    """Sets up session_state on first load"""
    if "screen" not in st.session_state:
        st.session_state.screen = "start"
    if "game_state" not in st.session_state:
        st.session_state.game_state = GameState(current_node = START_NODE)
    if "last_choice_id" not in st.session_state:
        st.session_state.last_choice_id = None
    if "narration_result" not in st.session_state:
        st.session_state.narration_result = None
    if "retry_count" not in st.session_state:
        st.session_state.retry_count = 0
    if "processing" not in st.session_state:
        st.session_state.processing = False
    if "warmed_up" not in st.session_state:
        st.session_state.warmed_up = False
    if "last_deltas" not in st.session_state:
        st.session_state.last_deltas = {}


def reset_game() -> None:
    """Resets session_state to Playing"""
    st.session_state.screen = "playing"
    st.session_state.game_state = GameState(current_node = START_NODE)
    st.session_state.last_choice_id = None
    st.session_state.narration_result = None
    st.session_state.retry_count = 0
    st.session_state.processing = False
    st.session_state.last_deltas = {}


def warm_up_backend() -> None:
    """
    Loads the LLM client and vector store and then runs one throwaway
    retrieval and  one throwaway Groq call so the first real turn
    doesn't carry that load time
    """
    from rag.llm import get_llm, generate_narration
    from rag.retriever import retrieve

    get_llm()

    # Loads the embedding model
    try:
        retrieve("Ragnar Lothbrok")
    except Exception:
        pass

    # Loads LLM 
    try:
        generate_narration("Reply with only the word: ready")
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Shared UI pieces
# ---------------------------------------------------------------------------
def render_stats_header(state: GameState, location: str | None = None) -> None:
    """Renders live stats header (shown on the "playing" screen only)"""
    st.markdown(render_stat_bar(state), unsafe_allow_html = True)



def format_deltas(deltas: dict) -> str | None:
    """
    Formats a {stat: delta} dict into a display string, e.g.,
    "Renown +15, Health -5". Returns None if there's nothing to show.
    """
    parts = [f"{STAT_LABELS[stat]} {delta:+d}"
             for stat, delta in deltas.items()
             if delta != 0]

    return ", ".join(parts) if parts else None


def render_sidebar() -> None:
    """
    Persistent sidebar shown on every screen: a glossary of the five
    stats, and (only while a saga is in progress) a Danger Zone with a
    Restart Saga button that resets the game immediately
    """
    with st.sidebar:
        st.subheader("Stats Glossary")
        st.markdown("Choices affect these values")
        for stat_key, label in STAT_LABELS.items():
            st.markdown(f"**{label} ({STAT_RANGES[stat_key]})**  \n{STAT_DESCRIPTIONS[stat_key]}")

        if st.session_state.screen in ("playing", "narrating"):
            st.divider()
            st.markdown("**Danger Zone**")
            if st.button("Restart Saga", type = "primary", use_container_width = True):
                reset_game()
                st.rerun()


# ---------------------------------------------------------------------------
# Screen: start
# ---------------------------------------------------------------------------
def render_start_screen() -> None:
    st.write("Take on the role of Ragnar Lothbrok, legendary Viking king and "
             "raider. Across ten turns drawn from Norse saga and mythology, "
             "your choices will shape how his story is told.")

    if not st.session_state.warmed_up:
        with st.spinner("Waking the skalds... loading the narration engine and lore index..."):
            warm_up_backend()
        st.session_state.warmed_up = True

    _, center_col, _ = st.columns([1, 1, 1])
    with center_col:
        if st.button("Begin Your Saga", type = "primary", use_container_width = True):
            reset_game()
            st.rerun()


# ---------------------------------------------------------------------------
# Screen: playing
# ---------------------------------------------------------------------------
def _generate_narration() -> None:
    """
    Constructs the narration prompt, generates narration text via Groq,
    and stores the result in session_state.narration_result
    """
    from orchestrator import run_turn

    state = st.session_state.game_state
    node_id = state.current_node
    choice_id = st.session_state.last_choice_id

    with st.spinner("Your tale is unfolding..."):
        result = run_turn(node_id, choice_id)

    st.session_state.narration_result = result


def render_playing_screen() -> None:
    state = st.session_state.game_state
    node = STORY[state.current_node]
    location = node["location"]

    render_stats_header(state)

    st.markdown(f"#### Turn {node['turn']} of 10")
    st.header(node["title"])
    st.markdown(f"#### *{location}*")
    st.write(node["context"])
    st.write(f"**{node['question']}**")

    choice_number = "I"
    for choice in node["choices"]:
        is_selected = (st.session_state.processing and st.session_state.last_choice_id == choice["choice_id"])

        label = f"{choice_number}. {choice['text']}"

        key_suffix = "_selected" if is_selected else ""
        clicked = st.button(label, key = f"choice_{choice['choice_id']}{key_suffix}",
                            disabled = st.session_state.processing, 
                            type = "secondary", use_container_width = True)
        if clicked and not st.session_state.processing:
            st.session_state.processing = True
            st.session_state.last_choice_id = choice["choice_id"]
            st.session_state.retry_count = 0
            st.rerun()

        choice_number += "I"

    if st.session_state.processing:
        time.sleep(0.5)

        choice = next( c for c in node["choices"] if c["choice_id"] == st.session_state.last_choice_id)

        from game.mechanics import apply_deltas
        apply_deltas(state, choice["deltas"])
        state.history.append((state.turn, state.current_node, choice["choice_id"]))
        st.session_state.last_deltas = choice["deltas"]

        _generate_narration()

        st.session_state.screen = "narrating"
        st.rerun()


# ---------------------------------------------------------------------------
# Screen: narrating
# ---------------------------------------------------------------------------
def render_narrating_screen() -> None:
    state = st.session_state.game_state
    node = STORY[state.current_node]
    choice = next(c for c in node["choices"] if c["choice_id"] == st.session_state.last_choice_id)
    choice_outcome = choice["outcome_title"]

    delta_text = format_deltas(st.session_state.get("last_deltas", {}))
    if delta_text:
        st.caption(delta_text)

    result = st.session_state.narration_result

    # If narration is successful
    if result["success"]:
        st.header(f"{choice_outcome}")
        st.write(result["narration"])

        is_last_turn = choice["next_node"] is None
        label = "See How the Saga Ends" if is_last_turn else "Continue"

        if st.button(label, type = "primary"):
            _advance_turn(choice)
            st.rerun()
        return

    # If narration is unsucessful
    st.warning(result["ui_error"])

    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.retry_count < 1:
            if st.button("Try Again"):
                st.session_state.retry_count += 1
                _generate_narration()
                st.rerun()
    with col2:
        if st.button("Skip Narration"):
            import random
            st.session_state.narration_result = {"success": True,
                                                 "narration": random.choice(SKIP_NARRATION_LINES),
                                                 "retrieved_chunks": result["retrieved_chunks"],
                                                 "category": result["category"],
                                                 "prompt": result["prompt"],
                                                 "error": result["error"],
                                                 "ui_error": None}
            st.rerun()


def _advance_turn(choice: dict) -> None:
    """Moves session state to the next node (or the ended screen if terminal)"""
    state = st.session_state.game_state

    if choice["next_node"] is None:
        state.game_over = True
        state.ending_reason = state.ending_reason or "completed"
        st.session_state.processing = False
        st.session_state.screen = "ended"
    else:
        state.current_node = choice["next_node"]
        state.turn += 1
        st.session_state.last_choice_id = None
        st.session_state.narration_result = None
        st.session_state.retry_count = 0
        st.session_state.processing = False
        st.session_state.screen = "playing"


# ---------------------------------------------------------------------------
# Screen: ended
# ---------------------------------------------------------------------------
def render_ended_screen() -> None:
    state = st.session_state.game_state
    result = st.session_state.narration_result

    st.header("The Saga Ends")

    if result and result.get("narration"):
        st.write(result["narration"])

    st.divider()
    st.write("**Your saga is remembered as:**")

    st.markdown("  \n".join(f"**{STAT_LABELS[stat_key]}:** {getattr(state, stat_key)}"
            for stat_key in STAT_LABELS))

    st.write("")
    _, _, corner = st.columns([1, 3, 1])
    with corner:
        if st.button("Play Again", type = "primary", use_container_width = True):
            reset_game()
            st.rerun()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:

    # Set browser page 
    st.set_page_config(page_title = "The Many Sagas of Ragnar", page_icon = "⚔️")

    # Apply theme
    apply_theme()

    # Initialize session state
    init_session_state()

    # Show side bar
    render_sidebar()

    # Show title
    st.title("The Many Sagas of Ragnar")
    st.markdown("<p style='text-align: center;'><em>a Viking saga, told differently each time</em></p>",
                unsafe_allow_html = True)

    screen = st.session_state.screen

    if screen == "start":
        render_start_screen()
    elif screen == "playing":
        render_playing_screen()
    elif screen == "narrating":
        render_narrating_screen()
    elif screen == "ended":
        render_ended_screen()
    else:
        st.error(f"Unknown screen state: {screen}")


if __name__ == "__main__":
    main()

# orchestrator.py
"""
Connects game/story.py, rag/retriever.py, rag/prompts.py, and rag/llm.py 
into one narration flow per turn
- get_prompt_for_turn(): retrieval + prompt building. Deterministic
    given the same (node_id, choice_id), so it's safe to cache
- run_turn(): calls get_prompt_for_turn(), then calls the LLM. NOT
    cached

Callers (CLI test script, Streamlit) should only call run_turn().
get_prompt_for_turn() is exposed separately mainly so Streamlit's caching
decorator can be applied to it directly
"""

# Import libraries
from game.story import STORY
from rag.retriever import retrieve
from rag.prompts import get_category_for_turn, build_retrieval_query, build_narration_prompt
from rag.llm import generate_narration

# Constants
UI_ERROR_MESSAGE = "The skalds falter in their telling of this tale... try again."


def _get_choice(node_id: str, choice_id: str) -> tuple[dict, dict]:
    """Returns the node and one of its choices from STORY"""
    if node_id not in STORY:
        raise ValueError(f"'{node_id}' is not a valid story node")

    node = STORY[node_id]
    choice = next((c for c in node["choices"] if c["choice_id"] == choice_id), None)

    if choice is None:
        raise ValueError(f"'{choice_id}' is not a valid choice for node '{node_id}'")

    return node, choice


def get_prompt_for_turn(node_id: str, choice_id: str) -> dict:
    """
    Constructs narration prompt for the turn by building the retrieval query 
    and retrieving grounding lore
    """
    node, choice = _get_choice(node_id, choice_id)

    current_context = node["context"]
    choice_text = choice["text"]
    outcome = choice["outcome"]
    next_node_id = choice["next_node"]
    next_context = STORY[next_node_id]["context"] if next_node_id is not None else None

    category = get_category_for_turn(node["turn"])
    query = build_retrieval_query(outcome, next_context)
    retrieved_chunks = retrieve(query, category = category)

    prompt = build_narration_prompt(current_context, choice_text, outcome,
                                     next_context, retrieved_chunks)

    return {"prompt": prompt,
            "retrieved_chunks": retrieved_chunks,
            "category": category}


def run_turn(node_id: str, choice_id: str) -> dict:
    """
    Constructs the narration prompt and generates narration text via Groq.

    On Groq failure (rag.llm.generate_narration raises RuntimeError), this
    is caught here rather than re-raised - the caller (CLI, Streamlit)
    should check `success` rather than use try/except. This is also the
    entry point retry buttons should call again: get_prompt_for_turn()'s
    result should be cached by the caller (e.g. via st.cache_data) so a
    retry only re-attempts the Groq call, not retrieval or prompt-building.

    Returns a dict with:
        success            bool
        narration          str | None - generated text on success
        retrieved_chunks   list - always populated
        category           str | None - from get_category_for_turn()
        prompt             str - always included, for debug panel + retry
        error              str | None - technical error detail, None on success
        ui_error           str | None - player-facing message, None on success
    """
    prompt_data = get_prompt_for_turn(node_id, choice_id)
    prompt = prompt_data["prompt"]

    try:
        narration = generate_narration(prompt)
    except RuntimeError as e:
        return {"success": False,
                "narration": None,
                "retrieved_chunks": prompt_data["retrieved_chunks"],
                "category": prompt_data["category"],
                "prompt": prompt,
                "error": str(e),
                "ui_error": UI_ERROR_MESSAGE}

    return {"success": True,
            "narration": narration,
            "retrieved_chunks": prompt_data["retrieved_chunks"],
            "category": prompt_data["category"],
            "prompt": prompt,
            "error": None,
            "ui_error": None}

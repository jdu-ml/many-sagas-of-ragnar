# prompts.py
"""
Constructs the retrieval query and narration prompt
- retrieval query is handed to rag.retriever.retrieve()
- narration prompt is handed to rag.llm.generate_narration()
"""

# Import libraries
from langchain_core.prompts import PromptTemplate


def get_category_for_turn(turn_number: int) -> str | None:
    """
    Maps a turn number to a retrieval category ("saga_history", "mythology").
    None for unfiltered retrieval across all sources
    """
    
    # TURN_CATEGORY_MAP = {
    #     1: "saga_history",   # vengeance for Siward - saga/family conflict
    #     2: "saga_history",   # winning Lagertha - saga material
    #     3: "saga_history",   # the serpent - saga material
    #     4: "mythology",      # grief/funeral rites - burial practices, mythology
    #     5: "saga_history",   # Aslaug vs Ingibjorg - saga material
    #     6: "mythology",      # Sigurd's serpent birthmark - omens/prophecy
    #     7: "saga_history",   # Paris - saga/history
    #     8: "saga_history",   # Ireland - saga/history
    #     9: "saga_history",   # word from Northumbria - saga/history
    #     10: "mythology",     # the snake pit / Valhalla - mythology
    # }
    # return TURN_CATEGORY_MAP.get(turn_number)
    
    return None


def build_retrieval_query(outcome: str, next_context: str | None) -> str:
    """
    Builds the retrieval query for a turn's chosen outcome.

    Convention: query = this choice's `outcome` + the next node's `context`
    """
    if not outcome or not outcome.strip():
        raise ValueError("build_retrieval_query() requires a non-empty outcome")

    if next_context is None:
        return outcome

    return f"{outcome}\n{next_context}"


def format_lore(retrieved_chunks: list[dict]) -> str:
    """
    Formats retriever.retrieve()'s output into the "RELEVANT NORSE LORE" block.
    Each chunk is presented with its source title for traceability
    """
    if not retrieved_chunks:
        return "(no relevant lore retrieved)"

    return "\n\n".join(f"[{chunk['title']}] {chunk['text']}" for chunk in retrieved_chunks)


NARRATION_TEMPLATE = PromptTemplate.from_template(
    """You are the narrator of a Viking historical-fiction adventure, in the tone of the TV series Vikings.

    PLAYER: Ragnar Lothbrok

    CURRENT CONTEXT (already shown to the player, do not repeat):
    {current_context}

    PLAYER'S CHOICE: {choice_text}
    OUTCOME (author-written beat to expand into narrative): {choice_outcome}

    NEXT CONTEXT (must lead into this, do not narrate its events):
    {next_context}

    RELEVANT NORSE LORE: {lore_block}

    INSTRUCTIONS:
    - Narrate in second person ("you"), never third person ("Ragnar draws his sword").
    His name/epithet is fine only in dialogue said to or about him by others
    (e.g. "they call you Ragnar Lothbrok, hairy-breeches").

    - Expand OUTCOME into what happens next. Use the supplied lore to ground it and to
    reconcile OUTCOME with NEXT CONTEXT if they'd otherwise conflict.

    - NEXT CONTEXT is for your awareness only - do not preview, foreshadow, or
    hint at any person, object, place, or event that first appears there.

    - Stop once OUTCOME is resolved, on a quiet transitional beat - not on the
    edge of a new scene or challenge.

    - Exactly 1 paragraph, max 4 sentences.

    - Stay true to OUTCOME and the story's tone - no invented mechanics, no choices,
    no material from the Vikings TV show or other fictional settings.
    """)

ENDING_TEMPLATE = PromptTemplate.from_template(
    """You are the narrator of a Viking historical-fiction adventure, in the tone of the TV series Vikings.

    PLAYER: Ragnar Lothbrok

    CURRENT CONTEXT (already shown to the player, do not repeat):
    {current_context}

    PLAYER'S CHOICE: {choice_text}
    OUTCOME (author-written beat to expand into narrative): {choice_outcome}

    RELEVANT NORSE LORE: {lore_block}

    INSTRUCTIONS:
    - Narrate in second person ("you"), never third person ("Ragnar draws his sword").
    His name/epithet is fine only in dialogue said to or about him by others.

    - Expand OUTCOME into the ending. Ground it in the supplied lore. Bring the story to a close.

    - Exactly 1 paragraph, max 4 sentences.

    - Stay true to OUTCOME and the story's tone - no invented mechanics, no choices,
    no material from the Vikings TV show or other fictional settings.
    """)

def build_narration_prompt(current_context: str, choice_text: str, choice_outcome: str,
                           next_context: str | None, retrieved_chunks: list[dict]) -> str:
    """Builds the narration prompt"""

    values = {"current_context": current_context,
              "choice_text": choice_text,
              "choice_outcome": choice_outcome,
              "lore_block": format_lore(retrieved_chunks)}

    if next_context is None:
        return ENDING_TEMPLATE.format(**values)

    return NARRATION_TEMPLATE.format(next_context=next_context, **values)

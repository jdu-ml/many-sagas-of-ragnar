# prompts.py
"""
Constructs the retrieval query and narration prompt
- retrieval query is handed to rag.retriever.retrieve()
- narration prompt is handed to rag.llm.generate_narration()
"""


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


def build_narration_prompt(current_context: str, choice_text: str, choice_outcome: str, 
                           next_context: str | None, retrieved_chunks: list[dict]) -> str:
    """Builds the narration prompt"""
    
    lore_block = format_lore(retrieved_chunks)

    if next_context is None:
        return f"""You are the narrator of a Viking historical-fiction adventure, in the tone of the TV series Vikings.

                PLAYER: Ragnar Lothbrok

                CURRENT CONTEXT (already shown to the player, do not repeat):
                {current_context}

                PLAYER'S CHOICE: {choice_text}
                OUTCOME (author-written beat to expand into narrative): {choice_outcome}

                RELEVANT NORSE LORE: {lore_block}

                INSTRUCTIONS:
                - This is the final turn. Narrate the ending itself, expanding on OUTCOME.
                - Write exactly 1 paragraph with no more than 4 sentences to bring the story to a close.
                - Use the supplied Norse lore as grounding for how this death/ending is portrayed.
                - Do not change the game outcome or invent game mechanics.
                - Do not introduce choices.
                - Keep the narrative appropriate to the current story and tone
                - Narrate in second person ("you"), matching the POV used in CURRENT CONTEXT and OUTCOME.
                Do not describe Ragnar's actions in third person (e.g. "Ragnar draws his sword"). Using 
                his name or epithet is fine only when it's something said about or to him by others 
                (e.g. "they call you Ragnar Lothbrok, hairy-breeches")
                """

    return f"""You are the narrator of a Viking historical-fiction adventure, in the tone of the TV series Vikings.

            PLAYER: Ragnar Lothbrok

            CURRENT CONTEXT (already shown to the player, do not repeat):
            {current_context}

            PLAYER'S CHOICE: {choice_text}
            OUTCOME (author-written beat to expand into narrative): {choice_outcome}

            NEXT CONTEXT (must lead into this, do not narrate its events):
            {next_context}

            RELEVANT NORSE LORE: {lore_block}

            INSTRUCTIONS:
            - Narrate what happens as a result of the player's choice, expanding on OUTCOME.
            - Use the supplied Norse lore as grounding and to support reconciling OUTCOME
            with NEXT CONTEXT where they would otherwise conflict.
            - Stop as soon as OUTCOME has been resolved. Your narration should end on a
            quiet, transitional beat (e.g. time passing, a mood, a journey continuing) -
            NOT on the edge of a new scene, encounter, or challenge.
            - NEXT CONTEXT is given only so you know what must remain true afterward -
            it is NOT something to preview, foreshadow, or write toward. Do not mention,
            describe, or hint at any specific person, object, place, creature, trial, or
            event that first appears in NEXT CONTEXT. If NEXT CONTEXT introduces a bear,
            for example, your narration must not mention a bear, an animal, a guardian,
            a trial, or anything suggesting one is coming.
            - Write exactly 1 paragraph with no more than 4 sentences. Do not write a full scene.
            - Do not change the game outcome or invent game mechanics.
            - Do not introduce choices.
            - Keep the narrative appropriate to the current story and tone.
            - Narrate in second person ("you"), matching the POV used in CURRENT CONTEXT and OUTCOME.
            Do not describe Ragnar's actions in third person (e.g. "Ragnar draws his sword"). Using 
            his name or epithet is fine only when it's something said about or to him by others 
            (e.g. "they call you Ragnar Lothbrok, hairy-breeches")
            """

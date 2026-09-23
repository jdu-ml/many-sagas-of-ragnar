# story.py
"""
Story arc

Each node has:
- turn              int, 1-10
- title             title of turn
- location          location of turn
- context           narrative for the turn
- question          question for the player to answer
- choices           list of choice dicts:
                      choice_id   unique text id for the choice
                      text        text shown to the player
                      deltas      dict {stat: delta} of stats based on the choice
                      outcome     outcome of choice that the LLM narrates      
"""

START_NODE = "turn_1"

STORY = {
    "turn_1": {
        "turn": 1,
        "title": "Vengeance for Siward",
        "location": "Home",
        "context": ("Your grandfather, King Siward, has been slain by the Swedish "
                    "King Fro, who has publicly humiliated the women of your family. "
                    "Among those fighting on the front lines is a shieldmaiden named "
                    "Lagertha, disguised alongside the men."),
        "question": "How do you respond to King Fro's provocation?",
        "choices": [
            {
                "choice_id": "declare_war",
                "text": "Rally your kin publicly and declare open war",
                "deltas": {"health": -5, "morale": 5, "renown": 15, "warband_loyalty": 10},
                "outcome_title": "War Won in the Open",
                "outcome": ("Ragnar summons his kin and allies openly, declaring war "
                            "on Fro. The warband rallies to him with pride and the "
                            "war against Fro is won in the open field."),
                "next_node": "turn_2",
            },
            {
                "choice_id": "secret_strike",
                "text": "Raise an army in secret and strike without warning",
                "deltas": {"morale": 5, "renown": 10, "warband_loyalty": 5},
                "outcome_title": "A Secret Victory",
                "outcome": ("Ragnar gathers a small, loyal band in secret and falls "
                            "on Fro's forces before word can spread. The victory is "
                            "swift."),
                "next_node": "turn_2",
            },
            {
                "choice_id": "blot_odin",
                "text": "Perform an animal blot dedicated to Odin, God of War",
                "deltas": {"health": -5, "morale": 5, "renown": 15, "warband_loyalty": 8, "favor_of_fate": 2},
                "outcome_title": "Odin's Favor",
                "outcome": ("Before raising a weapon, Ragnar offers a blot to "
                            "Odin, asking favor in the coming war. The omens are "
                            "read as good and the war against Fro is won with the "
                            "war-god's favor believed to be at Ragnar's back."),
                "next_node": "turn_2",
            },
        ],
    },
    "turn_2": {
        "turn": 2,
        "title": "Winning Lagertha",
        "location": "Norway",
        "context": ("The war against King Fro is won. Impressed by Lagertha's fierce "
                    "courage and warrior skills, you seek her hand, but she tests "
                    "you by guarding her home with a bear and a hound."),
        "question": "How do you face her trial?",
        "choices": [
            {
                "choice_id": "fight_beasts",
                "text": "Kill the bear and hound in open combat",
                "deltas": {"health": -10, "morale": 5},
                "outcome_title": "The Trial by Combat",
                "outcome": ("Ragnar meets the bear and hound head-on, taking wounds "
                            "from both before cutting them down. Lagertha watches "
                            "the fight from her doorway and is satisfied that he "
                            "has proven himself the hard way."),
                "next_node": "turn_3",
            },
            {
                "choice_id": "outwit_beasts",
                "text": "Try to outwit the beasts rather than fight them",
                "deltas": {"morale": 5},
                "outcome_title": "Cunning Over Combat",
                "outcome": ("Ragnar studies the animals rather than charge at them. "
                            "He uses bait and terrain to separate and subdue them "
                            "without a hard fight. Lagertha finds the cunning as "
                            "convincing as brute strength would have been."),
                "next_node": "turn_3",
            },
            {
                "choice_id": "ask_lagertha",
                "text": "Ask Lagertha why she demands this trial",
                "deltas": {"health": -5, "morale": 3},
                "outcome_title": "An Honest Question",
                "outcome": ("Ragnar puts the question to Lagertha directly and she "
                            "answers plainly: she will not be won by a man she has "
                            "not tested herself. Respecting her answer, he faces the "
                            "trial and she agrees to marry him."),
                "next_node": "turn_3",
            },
        ],
    },
    "turn_3": {
        "turn": 3,
        "title": "The Serpent",
        "location": "Gotaland (Sweden)",
        "context": ("Lagertha bears you three children, but you grow tired of her "
                    "and leave. Word reaches you of a noblewoman, Thora Borgarhjortr, "
                    "whose father promises her hand to whoever slays the monstrous "
                    "serpent guarding her chamber. You travel to Gotaland for the challenge."),
        "question": "How do you approach the serpent?",
        "choices": [
            {
                "choice_id": "wear_gear",
                "text": "Wear protective clothing",
                "deltas": {"health": -3, "morale": 5, "renown": 10},
                "outcome_title": "Hairy-Breeches",
                "outcome": ("Ragnar coats his trousers in pitch (tar) and rolls them in "
                            "sand, protecting himself from the serpent's venom and "
                            "bite. He slays the beast and wins Thora's hand, and "
                            "the men begin calling him 'Lothbrok', hairy-breeches."),
                "next_node": "turn_4",
            },
            {
                "choice_id": "bare_armed",
                "text": "Face it bare-armed to prove your courage",
                "deltas": {"health": -10, "morale": 5, "renown": 13},
                "outcome_title": "Courage Bought in Blood",
                "outcome": ("Ragnar refuses any protection and meets the serpent "
                            "bare-armed. He kills it but not without the creature's "
                            "fangs finding him. He wins Thora's hand at real cost "
                            "and word of his raw courage spreads fast."),
                "next_node": "turn_4",
            },
            {
                "choice_id": "seer_counsel",
                "text": "Seek a seer's counsel before the fight",
                "deltas": {"health": -1, "morale": 5, "renown": 10, "favor_of_fate": 1},
                "outcome_title": "The Seer's Guidance",
                "outcome": ("Ragnar seeks a seer before facing the serpent, who "
                            "tells him how the beast's hide may be turned against "
                            "it. Guided by that counsel, he slays the serpent and "
                            "wins Thora's hand."),
                "next_node": "turn_4",
            },
        ],
    },
    "turn_4": {
        "turn": 4,
        "title": "Grief and the Sea",
        "location": "Gotaland (Sweden)",
        "context": ("Thora has borne you sons, but illness takes her from you. "
                    "You feel empty inside."),
        "question": "How do you carry your grief?",
        "choices": [
            {
                "choice_id": "return_to_raiding",
                "text": "Return to raiding immediately, losing yourself in war",
                "deltas": {"health": -8, "morale": -10, "renown": 15, "warband_loyalty": 10},
                "outcome_title": "Grief Buried at Sea",
                "outcome": ("Ragnar leaves Thora's rites to others and returns to "
                            "the sea almost at once, burying his grief under raids "
                            "and plunder. His name grows, but the loss follows him "
                            "quietly beneath the victories."),
                "next_node": "turn_5",
            },
            {
                "choice_id": "funeral_rite",
                "text": "Hold a great funeral rite honoring the old gods",
                "deltas": {"health": 10, "morale": 5, "favor_of_fate": 2},
                "outcome_title": "A Funeral Fit for a Jarl's Daughter",
                "outcome": ("Ragnar holds a funeral for Thora, honoring the old "
                            "gods with fire and offerings. The rite steadies him "
                            "and he feels the gods have taken notice of his grief."),
                "next_node": "turn_5",
            },
            {
                "choice_id": "volva_counsel",
                "text": "Seek a volva's counsel about what her death means",
                "deltas": {"morale": 3, "favor_of_fate": 1},
                "outcome_title": "Words from the Volva",
                "outcome": ("Ragnar seeks out a volva to ask what Thora's death "
                            "means. Her answer is unclear but not unkind, hinting"
                            "that his path is not yet finished with sorrow nor "
                            "with fate's favor."),
                "next_node": "turn_5",
            },
        ],
    },
    "turn_5": {
        "turn": 5,
        "title": "Aslaug or Ingibjorg",
        "location": "Norway",
        "context": ("In Norway, you encounter a girl disguised as a peasant who "
                    "claims to be Aslaug, secret daughter of legendary dragon-slayer "
                    "Sigurd and shieldmaiden Brynhild. At the same time, King Eystein "
                    "offers his daughter Ingibjorg's hand as a political marriage."),
        "question": "What do you do?",
        "choices": [
            {
                "choice_id": "marry_aslaug",
                "text": "Test Aslaug with a riddle and marry her if she solves it",
                "deltas": {"morale": 5, "favor_of_fate": 2},
                "outcome_title": "A Claim Proven True",
                "outcome": ("Ragnar gives Aslaug a riddle and her answer "
                            "proves her claim true. He marries her and the union "
                            "feels touched by fate rather than mere politics."),
                "next_node": "turn_6",
            },
            {
                "choice_id": "marry_ingibjorg",
                "text": "Accept Ingibjorg's hand for the political alliance",
                "deltas": {"morale": -5, "renown": 8, "favor_of_fate": -2},
                "outcome_title": "A Short-Lived Alliance",
                "outcome": ("Ragnar agrees to marry Ingibjorg, strengthening "
                            "ties with Eystein's kingdom. But the alliance is "
                            "short-lived. Before long, Aslaug's claim is proven "
                            "true and it is she who becomes his wife."),
                "next_node": "turn_6",
            },
            {
                "choice_id": "delay_decision",
                "text": "Delay the decision and consult a seer about the omens",
                "deltas": {"morale": 5, "favor_of_fate": 1},
                "outcome_title": "The Omens Point True",
                "outcome": ("Ragnar delays choosing between the two women and seeks "
                            "a seer's reading of the omens. The signs point clearly "
                            "toward Aslaug and he marries her soon after."),
                "next_node": "turn_6",
            },
        ],
    },
    "turn_6": {
        "turn": 6,
        "title": "Sons of the Serpent-Eye", # rename
        "location": "Norway",
        "context": ("Aslaug bears you sons, including Sigurd, born with a mark in "
                    "his eye like a serpent. Meanwhile, King Klak of Jutland stirs "
                    "rebellion among the Jutes."),
        "question": "Where do you turn your attention?",
        "choices": [
            {
                "choice_id": "deal_with_klak",
                "text": "Deal with King Klak's rebellion before it spreads",
                "deltas": {"health": -5, "morale": 3, "renown": 8, "warband_loyalty": 8},
                "outcome_title": "Rebellion Crushed",
                "outcome": ("Ragnar marches on Klak before the rebellion can gather "
                            "strength, putting it down at some cost to himself. His "
                            "warband sees a king who protects his rule directly, "
                            "rather than leaving it to others."),
                "next_node": "turn_7",
            },
            {
                "choice_id": "stay_with_sons",
                "text": "Stay to see your sons raised and trained as warriors",
                "deltas": {"health": 10, "morale": 5, "renown": -5},
                "outcome_title": "A Father's Time",
                "outcome": ("Ragnar chooses to stay near his growing sons, seeing "
                            "them trained in arms himself. His name fades slightly "
                            "from the raiding talk, but his heart is steadier for "
                            "the time spent."),
                "next_node": "turn_7",
            },
            {
                "choice_id": "seers_counsel",
                "text": "Consult seers surrounding your son's birthmark",
                "deltas": {"morale": 5, "favor_of_fate": 1},
                "outcome_title": "The Serpent-Eye Confirmed",
                "outcome": ("Ragnar has the seers read the mark in Sigurd's eye and "
                            "they confirm it as a sign of Aslaug's legendary "
                            "parentage. The household takes it as proof that the "
                            "gods favor this line."),
                "next_node": "turn_7",
            },
        ],
    },
    "turn_7": {
        "turn": 7,
        "title": "The Lure of Paris",
        "location": "Francia",
        "context": ("King Charles the Bald has granted you land in an attempt to "
                    "buy peace. But the wealth of Paris calls to you and your "
                    "restless men."),
        "question": "Do you honor the peace or break it?",
        "choices": [
            {
                "choice_id": "break_peace",
                "text": "Break the peace and sail up the Seine river to besiege the city",
                "deltas": {"health": -8, "morale": 5, "renown": 15, "warband_loyalty": 10, "favor_of_fate": -3},
                "outcome_title": "The Siege of Paris",
                "outcome": ("Ragnar abandons the peace and sails up the Seine river, laying "
                            "siege to Paris itself. The raid is a triumph that swells his "
                            "renown across the north, though some mutter that breaking a "
                            "sworn peace invites ill fortune."),
                "next_node": "turn_8",
            },
            {
                "choice_id": "honor_peace",
                "text": "Honor the agreement and hold your position",
                "deltas": {"health": 3, "renown": -5, "warband_loyalty": -5, "favor_of_fate": 2},
                "outcome_title": "An Oath Kept",
                "outcome": ("Ragnar holds to the peace granted by Charles the Bald, "
                            "resisting the pull of Paris's wealth. His restraint "
                            "earns no new songs but it is taken as a sign of favor "
                            "by those who value an oath kept."),
                "next_node": "turn_8",
            },
            {
                "choice_id": "test_defenses",
                "text": "Send a smaller raiding party first to test the city's defenses",
                "deltas": {"health": -5, "morale": 5, "renown": 15, "warband_loyalty": 8},
                "outcome_title": "Paris Bought Off",
                "outcome": ("Ragnar sends a smaller party ahead to probe the city's "
                            "defenses before committing further. The scouting raid "
                            "succeeds cleanly so Ragnar decides to sail up the Seine "
                            "river to besiege the city. They occupied Paris and withdrew "
                            "when they were paid a large amount of gold and silver."),
                "next_node": "turn_8",
            },
        ],
    },
    "turn_8": {
        "turn": 8,
        "title": "Footholds in Ireland",
        "location": "Home",
        "context": ("Years have passed. You look toward Ireland, where Norse "
                    "footholds have already taken root near Dublin. A campaign so "
                    "far from home carries real risk."),
        "question": "How do you campaign in Ireland?",
        "choices": [
            {
                "choice_id": "settle_dublin",
                "text": "Establish a lasting settlement near Dublin",
                "deltas": {"health": 10, "morale": 5, "renown": 10, "warband_loyalty": 5},
                "outcome_title": "A Lasting Foothold",
                "outcome": ("Ragnar commits to building a lasting foothold near "
                            "Dublin, putting down roots rather than raiding and "
                            "leaving. His men take pride in a permanent stronghold, "
                            "and his name grows as a founder as well as a raider."),
                "next_node": "turn_9",
            },
            {
                "choice_id": "raid_swiftly",
                "text": "Raid swiftly, leaving a smaller garrison behind",
                "deltas": {"health": -5, "morale": 3, "renown": 5, "warband_loyalty": -3},
                "outcome_title": "A Swift Raid",
                "outcome": ("Ragnar strikes fast and hard, taking what plunder he "
                            "can and leaving only a thin garrison behind. The raid "
                            "pays well, but some of his men resent being left so "
                            "exposed and undermanned."
                ),
                "next_node": "turn_9",
            },
            {
                "choice_id": "send_sons_ireland",
                "text": "Send your sons to lead the campaign while you rule at home",
                "deltas": {"health": 10, "morale": 3, "renown": -5},
                "outcome_title": "Campaign from Afar",
                "outcome": ("Ragnar sends his sons to lead the Irish campaign in his "
                            "place, staying behind to govern. He finds some peace in "
                            "watching them lead, even as his own name is invoked "
                            "less in the telling of the raid."
                ),
                "next_node": "turn_9",
            },
        ],
    },
    "turn_9": {
        "turn": 9,
        "title": "Word from Northumbria",
        "location": "Home",
        "context": ("News reaches you that King Aella of Northumbria has slaughtered "
                    "your men in Ireland. Your men look to you, waiting to see how "
                    "you respond."),
        "question": "How do you respond?",
        "choices": [
            {
                "choice_id": "sail_yourself",
                "text": "Sail immediately to Northumbria to avenge your men yourself",
                "deltas": {"health": -10, "morale": 5, "renown": 5, "warband_loyalty": 5},
                "outcome_title": "Vengeance for Men",
                "outcome": ("Ragnar refuses to send others in his place, sailing for "
                            "Northumbria himself with what force he can gather "
                            "quickly. The voyage and the fighting take a toll on "
                            "his body, but no one can say he sent others to bleed "
                            "for him."),
                "next_node": "turn_10",
            },
            {
                "choice_id": "gather_larger_force",
                "text": "Gather a larger force before moving against Aella",
                "deltas": {"morale": 3, "renown": -5, "warband_loyalty": 8},
                "outcome_title": "Calculated Vengeance",
                "outcome": ("Ragnar holds back from sailing at once, gathering a "
                            "larger force before committing to the crossing. The "
                            "delay steadies his men's resolve, even as it costs him "
                            "some of the urgency his name is known for."),
                "next_node": "turn_10",
            },
            {
                "choice_id": "send_sons_avenge",
                "text": "Send your sons in your place, staying to secure your kingdom",
                "deltas": {"renown": -5, "warband_loyalty": 3},
                "outcome_title": "A King's Duty",
                "outcome": ("Ragnar originally decides to send his sons to answer Aella's "
                            "slaughter, choosing to remain behind to hold his kingdom together. "
                            "Some men say Ragnar has grown weak while others urge him to "
                            "reconsider his decision. He ultimately decides to sail to "
                            "Northumbria himself with a small force."),
                "next_node": "turn_10",
            },
        ],
    },
    "turn_10": {
        "turn": 10,
        "title": "The Snake Pit",
        "location": "Northumbria",
        "context": ("Shipwrecked or overwhelmed, you are captured by King Aella's "
                    "men and cast into a pit of venomous serpents. Your death is "
                    "near, but your voice is not yet silenced."),
        "question": "What are your final words?",
        "choices": [
            {
                "choice_id": "vow_vengeance",
                "text": "Declare that vengeance will come, carried by your sons",
                "deltas": {},
                "outcome_title": "A Vow for Vengeance",
                "outcome": ("As the serpents close in, Ragnar's last words are his death "
                            "will not go unanswered. It is a vow the sagas say his sons "
                            "kept in full."),
                "next_node": None,
            },
            {
                "choice_id": "welcome_valhalla",
                "text": "Call upon the gods, welcoming Valhalla (afterlife for fallen heroes)",
                "deltas": {},
                "outcome_title": "Welcome Valhalla",
                "outcome": ("Ragnar meets the serpents' venom without fear, calling "
                            "on Odin and welcoming the death of a warrior as the "
                            "gate to Valhalla rather than an end."),
                "next_node": None,
            },
            {
                "choice_id": "curse_aella",
                "text": "Curse Aella and Northumbria with your last breath",
                "deltas": {},
                "outcome_title": "Curse Aella",
                "outcome": ("With his final breath, Ragnar curses Aella and all of "
                            "Northumbria, his voice carrying even as the venom takes "
                            "him. The curse becomes as much a part of his legend as "
                            "the death itself."),
                "next_node": None,
            },
        ],
    },
}


def validate_story() -> None:
    """
    Checks STORY: 
    - Every node has a title, location, context, question, and choices
    - Every choice:
        - Has a unique id
        - Has delta key(s) that are the stats
        - Has an outcome
        - Points to a turn or None
    """
    from game.state import STAT_BOUNDS

    seen_choice_ids = set()
    for node_id, node in STORY.items():
        assert node.get("title"), (f"{node_id} is missing a title")
        assert node.get("location"), (f"{node_id} is missing a location")
        assert node.get("context"), (f"{node_id} is missing context")
        assert node.get("question"), (f"{node_id} is missing a question")
        assert "choices" in node and len(node["choices"]) > 0, (f"{node_id} has no choices")

        for choice in node["choices"]:
            cid = choice["choice_id"]
            assert cid not in seen_choice_ids, f"duplicate choice_id: {cid}"
            seen_choice_ids.add(cid)

            for stat in choice["deltas"]:
                assert stat in STAT_BOUNDS, (f"{node_id}/{cid} references unknown stat '{stat}'")

            assert choice.get("outcome"), (f"{node_id}/{cid} is missing an outcome")

            nxt = choice["next_node"]
            assert nxt is None or nxt in STORY, (f"{node_id}/{cid} points to missing node '{nxt}'")

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
                      choice_id         unique text id for the choice
                      text              text shown to the player
                      deltas            dict {stat: delta} of stats based on the choice
                      outcome_title     title of outcome
                      outcome           outcome of choice that the LLM narrates     
                      next_node         next turn 
"""

START_NODE = "turn_1"

STORY = {
    "turn_1": {
        "turn": 1,
        "title": "Vengeance for Siward",
        "location": "Home",
        "context": ("Your grandfather, King Siward of Norway, has been slain by King Fro "
                    "of Sweden, who has subjected the women of the royal household to "
                    "public humiliation in the aftermath. Word of the killing and the "
                    "disgrace spreads quickly through your kin. Some of the very women "
                    "King Fro dishonored have disguised themselves in men's clothing to "
                    "join the front lines, among them a shieldmaiden named Lagertha."),
        "question": "How do you avenge your grandfather and answer this dishonor?",
        "choices": [
            {
                "choice_id": "declare_war",
                "text": "Rally your kin publicly and declare open war",
                "deltas": {"health": -8, "morale": 5, "renown": 15, "warband_loyalty": 10},
                "outcome_title": "War Won in the Open",
                "outcome": ("You summon your kin and allies openly, declaring war "
                            "on Fro. The warband rallies to you with pride and the "
                            "war against Fro is won in the open field."),
                "next_node": "turn_2",
            },
            {
                "choice_id": "secret_strike",
                "text": "Raise an army in secret and strike without warning",
                "deltas": {"health": -3, "morale": 5, "renown": 10, "warband_loyalty": 5},
                "outcome_title": "A Swift Victory",
                "outcome": ("You gather a small, loyal band in secret and fall on "
                            "Fro's forces before word can spread. The victory is "
                            "swift."),
                "next_node": "turn_2",
            },
            {
                "choice_id": "blot_odin",
                "text": "Perform a blot to Odin, God of War, before entering war",
                "deltas": {"health": -8, "morale": 5, "renown": 15, "warband_loyalty": 8, "favor_of_fate": 2},
                "outcome_title": "Odin's Favor",
                "outcome": ("Before raising a weapon, you offer an animal blot to "
                            "Odin, asking favor in the coming war. The omens are read "
                            "as good and the war against Fro is won with the "
                            "war-god's favor believed to be at your back."),
                "next_node": "turn_2",
            },
        ],
    },
    "turn_2": {
        "turn": 2,
        "title": "Winning Lagertha",
        "location": "Norway",
        "context": ("The war against King Fro is won and your name is beginning to travel "
                    "beyond your own hall. You remember Lagertha from the fighting: her "
                    "fierce courage and warrior skills on the battlefield stood apart from "
                    "the rest, and the memory of her has stayed with you since. Determined "
                    "to make her yours, you seek her hand, but she is not easily won and "
                    "will not simply accept a suitor. She tests you by guarding her home "
                    "with a bear and a hound, leaving you to prove yourself before she "
                    "considers the match."),
        "question": "How do you face her trial?",
        "choices": [
            {
                "choice_id": "fight_beasts",
                "text": "Kill the bear and hound in open combat",
                "deltas": {"health": -10, "morale": 5},
                "outcome_title": "Trial by Combat",
                "outcome": ("You meet the bear and hound head-on, taking wounds "
                            "from both before cutting them down. Lagertha watches "
                            "the fight from her doorway and is satisfied that you "
                            "have proven yourself the hard way."),
                "next_node": "turn_3",
            },
            {
                "choice_id": "outwit_beasts",
                "text": "Try to outwit the beasts rather than fight them",
                "deltas": {"morale": 5},
                "outcome_title": "Cunning Over Combat",
                "outcome": ("You study the animals rather than charge at them, "
                            "using bait and terrain to separate and subdue them "
                            "without a hard fight. Lagertha finds the cunning as "
                            "convincing as brute strength would have been."),
                "next_node": "turn_3",
            },
            {
                "choice_id": "ask_lagertha",
                "text": "Ask Lagertha why she demands this trial",
                "deltas": {"health": -5, "morale": 3},
                "outcome_title": "An Honest Question",
                "outcome": ("You put the question to Lagertha directly and she "
                            "answers plainly: she will not be won by a man she has "
                            "not tested herself. Respecting her answer, you face the "
                            "trial and she agrees to marry you."),
                "next_node": "turn_3",
            },
        ],
    },
    "turn_3": {
        "turn": 3,
        "title": "The Serpent",
        "location": "Norway",
        "context": ("Lagertha bears you three children, but you grow tired of the "
                    "marriage and leave her. Word reaches you of a noblewoman, Thora "
                    "Borgarhjortr, whose father has promised her hand to whoever can slay "
                    "the monstrous serpent guarding her chamber. Many suitors have tried "
                    "and failed, and the creature's reputation for cruelty has kept most "
                    "from even attempting it. You travel to Gotaland for the challenge."),
        "question": "How do you approach the serpent?",
        "choices": [
            {
                "choice_id": "wear_gear",
                "text": "Wear protective clothing",
                "deltas": {"health": -3, "morale": 5, "renown": 10},
                "outcome_title": "Hairy-Breeches",
                "outcome": ("You coat your trousers in pitch (tar) and roll them in "
                            "sand, protecting yourself from the serpent's venom and "
                            "bite. You slay the beast, win Thora's hand, and the "
                            "men begin calling you 'Lothbrok', hairy-breeches."),
                "next_node": "turn_4",
            },
            {
                "choice_id": "bare_armed",
                "text": "Face it bare-armed to prove your courage",
                "deltas": {"health": -10, "morale": 5, "renown": 13},
                "outcome_title": "Courage Bought in Blood",
                "outcome": ("You do not wear any protection and meet the serpent "
                            "bare-armed. You kill it but not without the creature's "
                            "fangs finding you. You win Thora's hand at real cost "
                            "and word of your raw courage spreads fast."),
                "next_node": "turn_4",
            },
            {
                "choice_id": "seer_counsel",
                "text": "Seek a seer's counsel before the fight",
                "deltas": {"health": -3, "morale": 5, "renown": 10, "favor_of_fate": 1},
                "outcome_title": "The Seer's Guidance",
                "outcome": ("You seek a seer before facing the serpent, who tells "
                            "you how the beast's hide may be turned against it. "
                            "Guided by that counsel, you slay the serpent and "
                            "win Thora's hand."),
                "next_node": "turn_4",
            },
        ],
    },
    "turn_4": {
        "turn": 4,
        "title": "Mourning Thora",
        "location": "Gotaland (Sweden)",
        "context": ("Thora has borne you sons and the years with her have been some "
                    "of the fullest of your life. Then illness takes hold of her, "
                    "swift and merciless, leaving no time for goodbyes. You feel "
                    "hollowed out by the loss, a grief unlike anything you have "
                    "carried before. Your men watch closely now, wondering how "
                    "you will carry this kind of sorrow."),
        "question": "How do you carry your grief?",
        "choices": [
            {
                "choice_id": "return_to_raiding",
                "text": "Return to raiding immediately, losing yourself in war",
                "deltas": {"health": -8, "morale": -10, "renown": 15, "warband_loyalty": 10},
                "outcome_title": "Grief Buried at Sea",
                "outcome": ("You leave Thora's funeral rite to others and return to "
                            "the sea almost at once, burying your grief under raids "
                            "and plunder. Your name grows, but the loss follows you "
                            "quietly beneath the victories."),
                "next_node": "turn_5",
            },
            {
                "choice_id": "funeral_rite",
                "text": "Hold a funeral rite for Thora",
                "deltas": {"health": 10, "morale": 5, "favor_of_fate": 2},
                "outcome_title": "A Funeral Fit for a Jarl's Daughter",
                "outcome": ("You hold a funeral for Thora, honoring the old gods "
                            "with fire and offerings. The rite steadies you and "
                            "you feel the gods have taken notice of your grief."),
                "next_node": "turn_5",
            },
            {
                "choice_id": "volva_counsel",
                "text": "Seek a volva's counsel about what her death means",
                "deltas": {"morale": 3, "favor_of_fate": 1},
                "outcome_title": "Words from the Volva",
                "outcome": ("You seek out a volva to ask what Thora's death "
                            "means. Her answer is unclear but not unkind, hinting "
                            "that your path is not yet finished with sorrow nor "
                            "with fate's favor."),
                "next_node": "turn_5",
            },
        ],
    },
    "turn_5": {
        "turn": 5,
        "title": "Aslaug or Ingibjorg",
        "location": "Norway",
        "context": ("In Norway, you encounter a girl disguised as a peasant who claims "
                    "to be Aslaug, secret daughter of the legendary dragon-slayer Sigurd "
                    "and the shieldmaiden Brynhild. Her claim seems impossible on its face, "
                    "yet something about her manner suggests she is speaking the truth. At "
                    "the same time, King Eystein offers his daughter Ingibjorg's hand as a "
                    "political marriage, a match that would strengthen your standing "
                    "considerably."),
        "question": "What path do you choose?",
        "choices": [
            {
                "choice_id": "marry_aslaug",
                "text": "Test Aslaug with a riddle and marry her if she solves it",
                "deltas": {"morale": 5, "favor_of_fate": 2},
                "outcome_title": "A Claim Proven True",
                "outcome": ("You give Aslaug a riddle: 'to arrive neither dressed nor "
                            "undressed, neither fasting nor eating, and neither alone"
                            " nor in company.' She solves the riddle. Impressed by her "
                            "intellect, you marry her and the union feels touched by "
                            "fate rather than mere politics."),
                "next_node": "turn_6",
            },
            {
                "choice_id": "marry_ingibjorg",
                "text": "Accept Ingibjorg's hand for the political alliance",
                "deltas": {"morale": -5, "renown": 8, "favor_of_fate": -2},
                "outcome_title": "A Short-Lived Alliance",
                "outcome": ("You agree to marry Ingibjorg, strengthening ties with "
                            "Eystein's kingdom. But the alliance is short-lived: further "
                            "signs come to light that confirm Aslaug's claim beyond "
                            "doubt. Convinced, you set the marriage aside and choose "
                            "Aslaug as your wife instead."),
                "next_node": "turn_6",
            },
            {
                "choice_id": "delay_decision",
                "text": "Delay the decision and consult a seer about the omens",
                "deltas": {"morale": 5, "favor_of_fate": 1},
                "outcome_title": "All Signs Point to Aslaug",
                "outcome": ("You delay choosing between the two women and seek a "
                            "seer's reading of the omens. The signs point clearly "
                            "toward Aslaug and you marry her soon after."),
                "next_node": "turn_6",
            },
        ],
    },
    "turn_6": {
        "turn": 6,
        "title": "Sons and Rebellion",
        "location": "Norway",
        "context": ("Aslaug bears you sons, including Sigurd, who is born with a mark "
                    "in his eye like a serpent. The years that follow are full and your "
                    "household grows stronger with each passing season. Meanwhile, King "
                    "Klak of Jutland stirs rebellion among the Jutes, testing whether "
                    "your hold on the region can survive your attention being elsewhere."),
        "question": "Where do you turn your attention?",
        "choices": [
            {
                "choice_id": "deal_with_klak",
                "text": "Deal with King Klak's rebellion before it spreads",
                "deltas": {"health": -5, "morale": 3, "renown": 8, "warband_loyalty": 8},
                "outcome_title": "Rebellion Crushed",
                "outcome": ("You march on Klak before the rebellion can gather strength, "
                            "putting it down at some cost to yourself. Your warband "
                            "sees you protecting your rule directly, rather than "
                            "leaving it to others."),
                "next_node": "turn_7",
            },
            {
                "choice_id": "stay_with_sons",
                "text": "Stay to see your sons raised and trained as warriors",
                "deltas": {"health": 10, "morale": 5, "renown": -5},
                "outcome_title": "A Father's Time",
                "outcome": ("You choose to stay near your growing sons, seeing "
                            "them trained in arms yourself. Your name fades slightly "
                            "from the raiding talk, but your heart is steadier for "
                            "the time spent."),
                "next_node": "turn_7",
            },
            {
                "choice_id": "seers_counsel",
                "text": "Consult seers about Sigurd's birthmark",
                "deltas": {"morale": 5, "favor_of_fate": 1},
                "outcome_title": "The Serpent-Eye Confirmed",
                "outcome": ("You have the seers read the mark in Sigurd's eye and "
                            "they confirm it as a sign of Aslaug's legendary "
                            "parentage. Your household takes it as proof that the "
                            "gods favor this line."),
                "next_node": "turn_7",
            },
        ],
    },
    "turn_7": {
        "turn": 7,
        "title": "The Lure of Paris",
        "location": "Francia",
        "context": ("Your raids and conquests have not gone unnoticed. King Charles "
                    "the Bald has granted you land in an attempt to buy peace, hoping "
                    "the gift will be enough to see you settle. For a time the "
                    "arrangement holds, your men grow comfortable with steadier, "
                    "safer gains. But the wealth of Paris proves too great a temptation "
                    "to ignore"),
        "question": "Do you honor the peace or break it?",
        "choices": [
            {
                "choice_id": "break_peace",
                "text": "Break the peace and besiege Paris",
                "deltas": {"health": -8, "morale": 5, "renown": 15, "warband_loyalty": 15, "favor_of_fate": -3},
                "outcome_title": "The Siege of Paris",
                "outcome": ("You abandon the peace, sail up the Seine river, and "
                            "besiege Paris itself. The raid is a triumph that swells "
                            "your reputation, though some mutter that breaking a sworn "
                            "peace invites ill fortune."),
                "next_node": "turn_8",
            },
            {
                "choice_id": "honor_peace",
                "text": "Honor the agreement and hold your position",
                "deltas": {"health": 5, "renown": -5, "warband_loyalty": -10, "favor_of_fate": 2},
                "outcome_title": "An Oath Kept",
                "outcome": ("You hold to the peace granted by Charles the Bald, resisting "
                            "the pull of Paris's wealth. Your restraint earns no new songs "
                            "and word soon reaches you that another Norse fleet has taken "
                            "the city. It stings to hear the glory you set aside claimed by "
                            "another's hand, even as your oath-keeping is taken as a sign of "
                            "favor by those who value an oath kept."),
                "next_node": "turn_8",
            },
            {
                "choice_id": "test_defenses",
                "text": "Send a smaller raiding party first to test the city's defenses",
                "deltas": {"health": -5, "morale": 5, "renown": 15, "warband_loyalty": 10},
                "outcome_title": "Paris Bought Off",
                "outcome": ("You send a smaller party ahead to probe the city's "
                            "defenses before committing further. The scouting raid "
                            "succeeds cleanly, so you decide to sail up the Seine "
                            "river to besiege the city. You occupy Paris and withdraw "
                            "once you are paid a large amount of gold and silver."),
                "next_node": "turn_8",
            },
        ],
    },
    "turn_8": {
        "turn": 8,
        "title": "Footholds in Ireland",
        "location": "Home",
        "context": ("Years have passed since Francia. You now look toward Ireland, where "
                    "Norse footholds have already taken root, carved out by others "
                    "willing to test the crossing. A campaign so far from home carries "
                    "real risk, stretching your men and resources. Still, the promise of "
                    "new land and plunder is not one you are inclined to ignore."),
        "question": "How do you campaign in Ireland?",
        "choices": [
            {
                "choice_id": "settle_dublin",
                "text": "Establish a lasting settlement near Dublin",
                "deltas": {"health": 10, "morale": 5, "renown": 10, "warband_loyalty": 10},
                "outcome_title": "A Lasting Foothold",
                "outcome": ("You commit to building a lasting foothold near "
                            "Dublin, putting down roots rather than raiding and "
                            "leaving. Your men take pride in a permanent stronghold, "
                            "and your name grows as a founder as well as a raider."),
                "next_node": "turn_9",
            },
            {
                "choice_id": "raid_swiftly",
                "text": "Raid swiftly, leaving a smaller garrison behind",
                "deltas": {"health": -5, "morale": 3, "renown": 5, "warband_loyalty": -5},
                "outcome_title": "A Swift Raid",
                "outcome": ("You strike fast and hard, taking what plunder you "
                            "can and leaving only a thin garrison behind. The raid "
                            "pays well, but some of your men resent being left so "
                            "exposed and undermanned."
                ),
                "next_node": "turn_9",
            },
            {
                "choice_id": "send_sons_ireland",
                "text": "Send your sons to lead the campaign while you rule at home",
                "deltas": {"health": 10, "morale": 3, "renown": -5},
                "outcome_title": "Campaign from Afar",
                "outcome": ("You send your sons to lead the Irish campaign in your "
                            "place, staying behind to govern. You find some peace in "
                            "watching them lead, even as your own name is invoked "
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
        "context": ("News reaches you that King Aella of Northumbria has slaughtered your "
                    "men in Ireland. A battered ship limps into harbor carrying the few who "
                    "escaped the massacre. Their tales speak of bloodshed, comrades left "
                    "unburied, and a king who believed he could spill your blood without "
                    "consequence. As silence falls over the hall, your men look to you for "
                    "an answer."),
        "question": "How do you respond?",
        "choices": [
            {
                "choice_id": "sail_yourself",
                "text": "Sail immediately to Northumbria to avenge your men yourself",
                "deltas": {"health": -10, "morale": 5, "renown": 5, "warband_loyalty": 5},
                "outcome_title": "Vengeance for Men",
                "outcome": ("You refuse to send others in your place, sailing for "
                            "Northumbria yourself with what force you can gather "
                            "quickly. The voyage and the fighting take a toll on "
                            "your body, but no one can say you sent others to bleed "
                            "for you."),
                "next_node": "turn_10",
            },
            {
                "choice_id": "gather_larger_force",
                "text": "Gather a larger force before moving against Aella",
                "deltas": {"morale": 3, "renown": -5, "warband_loyalty": 8},
                "outcome_title": "Calculated Vengeance",
                "outcome": ("You hold back from sailing at once, gathering a "
                            "larger force before committing to the crossing. The "
                            "delay steadies your men's resolve, even as it costs you "
                            "some of the urgency your name is known for."),
                "next_node": "turn_10",
            },
            {
                "choice_id": "send_sons_avenge",
                "text": "Send your sons in your place, staying to secure your kingdom",
                "deltas": {"renown": -5, "warband_loyalty": -8},
                "outcome_title": "A King's Duty",
                "outcome": ("You resolve to send your sons to answer Aella's slaughter, "
                            "intending to remain behind and rule. But word of the plan "
                            "spreads through your hall and some of your men say this is "
                            "not a wrong a king can leave to others. Their words linger "
                            "and before your sons' ships can depart, you decide not to "
                            "send them after all, gathering a crew of your own instead "
                            "and resolving to sail for Northumbria yourself."),
                "next_node": "turn_10",
            },
        ],
    },
    "turn_10": {
        "turn": 10,
        "title": "The Snake Pit",
        "location": "Northumbria",
        "context": ("Overwhelmed and outnumbered, you are captured by King Aella's men and "
                    "cast into a pit of venomous serpents. The cold press of the pit's walls "
                    "and the hiss of the snakes around you leave little doubt about how this "
                    "ends. No ally is coming. Your death is near and all of your men have "
                    "already fallen. Your voice is not yet silenced and the words you choose "
                    "now are the last the world will hear from you."),
        "question": "What are your final words?",
        "choices": [
            {
                "choice_id": "vow_vengeance",
                "text": "Declare that vengeance will come, carried by your sons",
                "deltas": {},
                "outcome_title": "A Legacy of Vengeance",
                "outcome": ("As the serpents close in, your last words vow that your death "
                            "will not go unanswered. It is a vow the sagas say your sons "
                            "kept in full."),
                "next_node": None,
            },
            {
                "choice_id": "welcome_valhalla",
                "text": "Call upon the gods, welcoming Valhalla (afterlife for fallen heroes)",
                "deltas": {},
                "outcome_title": "A Seat in Valhalla",
                "outcome": ("You meet the serpents' venom without fear, calling "
                            "on Odin and welcoming a warrior's death as the "
                            "gate to Valhalla rather than an end."),
                "next_node": None,
            },
            {
                "choice_id": "curse_aella",
                "text": "Curse Aella and Northumbria with your last breath",
                "deltas": {},
                "outcome_title": "A Dying Curse",
                "outcome": ("With your final breath, you curse Aella and all of "
                            "Northumbria, your voice carrying even as the venom takes "
                            "you. The curse becomes as much a part of your legend as "
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

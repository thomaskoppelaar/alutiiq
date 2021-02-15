import os
import json
from types import SimpleNamespace

from data import Card, session_objects
from screen import Screen

# Load card data
f = open("data/cards.json", "r")
card_data = json.load(f)
f.close()

del(f)

# System call to clear the console
def clear_screen():
    os.system('cls' if os.name=='nt' else 'clear')

# (Boilerplate) Load a json dict into an object
def load_card(card_name: str, card_data: [dict]) -> Card:
    """
    Makes a card object out of a json string.
    """

    card_string = json.dumps(card_data[card_name])
    card_obj = json.loads(card_string, object_hook=Card)
    return card_obj

def card_selection(choices: [str], cd, scr: Screen) -> Card:
    cards = cards_selection(choices, cd, scr, min=1, max=1)

    # Happens when player cancels the selection.
    if len(cards) == 0:
        return None
    else:
        return cards[0]

def cards_selection(choices: [str], cd, scr: Screen, min: int = 1, max: int = 1) -> [Card]:

    scr.log("You can buy cards in the store by inputting the name of the card.")
    
    # Ask the player for a choice
    player_choice = ""
    while 1:
        
        player_choice = scr.retrieve_user_input()
        player_choice = player_choice.lower()
        player_choice = player_choice.split(',')
        player_choice = [s.strip() for s in player_choice]

        if len(player_choice) == 0:
            scr.log("Enter an option.")
            continue

        elif player_choice[0] == "c":
            
            scr.log("Action cancelled.")
            return []

        # Min / max checking
        elif len(player_choice) < min:
            scr.log("You need to pick at least {0} card(s).".format(min))
        elif len(player_choice) > max:
            scr.log("You can only pick at most {0} card(s).".format(max))
        # TODO: Duplicate card checking

        else:
            res: [Card] = []
            for choice in player_choice:
                card_name = choice
                if choice.isdigit():
                    try:
                        index = int(choice) - 1
                        card_name = choices[index]
                        res.append(load_card(card_name, cd))
                    except:
                        scr.log("Invalid number choice!")
                        res = []
                        break
                else:
                    try:
                        res.append(load_card(card_name, cd))
                    except:
                        scr.log("Invalid card choice!")
                        res = []
                        break
            if len(res) == 0:
                continue
            else:
                return res
def get_turns() -> int:
    return session_objects.Turn_counter

def get_game_mode() -> str:
    return session_objects.Game_mode

def get_game_version() -> str:
    return session_objects.Game_version

def stub() -> None:
    return

def get_point_total() -> str:
    return "WIP"
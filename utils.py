import os
import json
from types import SimpleNamespace

from data import Card

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
def show_cards(cards: [str], cd, show_description: bool = False, show_type: bool = False, show_cost: bool = False) -> None:

    if len(cards) == 0:
        print("No available cards!")
        return
    
    i = 1
    for card_name in cards:
        card = load_card(card_name, cd)
        if show_type:
            print("  {0}. {1} ({2})".format(i, card.name, card.cardtype))
        else:
            print("  {0}. {1}".format(i, card.name))
        if show_cost:
            print("    - Costs: ${0}".format(card.cost))
        if show_description:
            print("    - {0}".format(card.description))
            print()
        i += 1
def card_selection(choices: [str], cd) -> Card:
    cards = cards_selection(choices, cd, min=1, max=1)

    # Happens when player cancels the selection.
    if len(cards) == 0:
        return None
    else:
        return cards[0]

def cards_selection(choices: [str], cd, min: int = 1, max: int = 1) -> [Card]:

    # Ask the player for a choice
    player_choice = ""
    while 1:
        print("For multiple inputs, separate the entries with a comma.")
        player_choice = input("Your choice: (C to cancel) ")
        player_choice = player_choice.lower()
        player_choice = player_choice.split(',')
        player_choice = [s.strip() for s in player_choice]

        if len(player_choice) == 0:
            print("Enter an option.")
            continue

        elif player_choice[0] == "c":
            clear_screen()
            print("Action cancelled.")
            return []

        # Min / max checking
        elif len(player_choice) < min:
            print("You need to pick at least {0} card(s).".format(min))
        elif len(player_choice) > max:
            print("You can only pick at most {0} card(s).".format(max))
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
                        print("Invalid number choice!")
                        res = []
                        continue
                else:
                    try:
                        res.append(load_card(card_name, cd))
                    except:
                        print("Invalid card choice!")
                        res = []
                        continue
            clear_screen()
            return res
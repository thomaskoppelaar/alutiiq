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
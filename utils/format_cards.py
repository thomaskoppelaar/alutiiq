import textwrap
from utils import load_card
from data import Card

def format_cards(cards: [str], width, show_description: bool = False, show_type: bool = False, show_cost: bool = False, custom_lines: [str] = None) -> [str]:
    
    res = []

    if len(cards) == 0:
        res.append("No available cards!")
        return res
    
    i = 1
    for card_name in cards:
        card = load_card(card_name)

        res.append("{0}. {1} {2} {3}".format(
            # Number
            i,

            # Name
            card.name,

            # Card type
            "({0})".format(card.cardtype) if show_type else "",

            # Card cost
            "- {0}$".format(card.cost) if show_cost else ""
        ))
        
        if show_description:
            wrapper = textwrap.TextWrapper(width=width)
            res = res + wrapper.wrap("  - " + card.description)

        # Custom lines can be added per card
        if custom_lines is not None:
            res.append(custom_lines[i-1])

        res.append("")

        i += 1

    return res

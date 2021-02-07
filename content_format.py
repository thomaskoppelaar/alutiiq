import textwrap

from utils import load_card, Card


def format_cards(cards: [str], cd, w, show_description: bool = False, show_type: bool = False, show_cost: bool = False) -> [str]:
    
    res = []

    if len(cards) == 0:
        res.append("No available cards!")
        return res
    
    i = 1
    for card_name in cards:
        card = load_card(card_name, cd)

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
            wrapper = textwrap.TextWrapper(width=w)
            res = res + wrapper.wrap("  - " + card.description)

            
            res.append("")
        i += 1

    return res
# Action cards probably deserve their own little file
from data.player import Player

# WIP
def routine(p: Player, s: dict, cd: dict) -> None:


    print("Which action do you want to play?")
    # WIP
    perform_action(p, s, cd, "magic spell")


# WIP
def perform_action(p: Player, s: dict, cd: dict, card_name: str) -> None:
    """
    Plays a card in the player's hand.
    Once a card is successfully played, the card gets put on the player's discard pile.
    """
    for card in p.current_hand:

        # Found the card that we want to play
        if "action" in card.cardtype and card.name == card_name:
            try:
                globals()[card.action](p, s, cd)
                p.actions_left -= 1
                p.current_hand.remove(card)
                p.discardpile.append(card)
                break
            except:
                print("")


def magic_spell(p: Player, s: dict, cd: dict) -> None:
    p.draw_cards(2)
    print("woosh I do thing")

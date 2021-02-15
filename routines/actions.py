# Action cards probably deserve their own little file
from data import Player, Card
from utils import clear_screen, load_card, card_selection
from routines import store
from screen import Screen

def routine(p: Player, s: dict, cd: dict, scr: Screen) -> None:
    """
    Action routine. Allows player to play action cards.
    """
    clear_screen()
    if p.actions_left <= 0:
        print("You don't have any actions left.")
        return
    action_cards: [str] = [card.name for card in p.current_hand if "action" in card.cardtype]
    if len(action_cards) == 0:
        print("You don't have any action cards to play.")
        return

    print("Which action do you want to play?")
    # show_cards(action_cards, cd, show_description=True)
    
    card: Card = card_selection(action_cards, cd, scr)
    
    if card is None: return

    perform_action(p, s, cd, card.name, scr)
   

def perform_action(p: Player, s: dict, cd: dict, card_name: str, scr: Screen) -> None:
    """
    Plays a card in the player's hand.
    Once a card is successfully played, the card gets put on the player's discard pile.
    """
    for card in p.current_hand:

        # Found the card that we want to play
        if "action" in card.cardtype and card.name == card_name:
            try:
                action_performed: bool = globals()[card.action](p, s, cd)

                if action_performed:
                    p.actions_left -= 1

                    # Move card from hand onto discard pile
                    p.card_played(card)

                break
            except:
                print("Action failed!")


def magic_spell(p: Player, s: dict, cd: dict, scr: Screen) -> bool:
    p.draw_cards(2)
    return True

def woodcutter(p: Player, s: dict, cd: dict, scr: Screen) -> bool:
    p.add_money(2)
    p.add_purchases(1)
    return True

def smithy(p: Player, s: dict, cd: dict, scr: Screen) -> bool:
    p.draw_cards(3)
    return True

def festival(p: Player, s: dict, cd: dict, scr: Screen) -> bool:
    p.add_actions(2)
    p.add_purchases(1)
    p.add_money(2)
    return True

def mine(p: Player, s: dict, cd: dict, scr: Screen) -> bool:
    money_cards = {}
    for card in p.current_hand:
        if "money" in card.cardtype:
            money_cards.update({card.name: card})
    
    if len(money_cards.keys()) == 0:
        print("No money cards to upgrade!")
        return False


    scr.log("Which card do you want to upgrade?")

    # show_cards(list(money_cards.keys()), cd)
        
    chosen_card = card_selection(list(money_cards.keys()), cd, scr)
    
    if chosen_card is None: return

    card_name = chosen_card.name

    clear_screen()
    if card_name == "platinum coin":
        scr.log("Sorry, the fun stops here.")
        return False
    elif card_name == "gold coin":
        p.trash_hand_card(money_cards[card_name])
        secret_card = load_card("platinum coin", cd)
        scr.log("That's some incredible value right there!")
        p.add_hand_card(secret_card)
        return True
    elif card_name == "silver coin":
        p.trash_hand_card(money_cards[card_name])
        store.gift_card(p, "gold coin", cd, s, pile="hand")
        scr.log("Upgraded a silver to a gold coin.")
        return True
    elif card_name == "copper coin":
        p.trash_hand_card(money_cards[card_name])
        store.gift_card(p, "silver coin", cd, s, pile="hand")
        scr.log("Upgraded a copper to a silver coin.")
        return True

def bandit_sp(p: Player, s: dict, cd: dict, scr: Screen) -> bool:
    store.gift_card(p, "gold coin", cd, s, pile="discard")
    return True

def village(p: Player, s: dict, cd: dict, scr: Screen) -> bool:
    p.add_actions(2)
    p.draw_cards(1, scr)
    return True
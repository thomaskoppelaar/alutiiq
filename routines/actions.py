# Action cards probably deserve their own little file
from data import Player, Card
from utils import clear_screen, load_card, input_card_selection, input_cards_selection, format_cards
from routines import store
from screen import Screen, r_main_content

def routine(p: Player, scr: Screen) -> None:
    """
    Action routine. Allows player to play action cards.
    """
    if p.actions_left <= 0:
        scr.log("You don't have any actions left.", 2)
        return
    action_cards: [str] = [card for card in p.current_hand if "action" in load_card(card).cardtype]
    if len(action_cards) == 0:
        scr.log("You don't have any action cards to play.", 2)
        return


    scr.show_main_content(
        ["Which action do you want to play?"] + format_cards(action_cards, r_main_content.width, show_description=True)
    )
    
    card: Card = input_card_selection(action_cards, scr)
    
    if card is None: return

    perform_action(p, card.name, scr)
   

def perform_action(p: Player, card_name: str, scr: Screen) -> None:
    """
    Plays a card in the player's hand.
    Once a card is successfully played, the card gets put on the player's discard pile.
    """
    for card in p.current_hand:

        # Found the card that we want to play
        if "action" in load_card(card).cardtype and card == card_name:
            # try:
                p.current_hand.remove(card)
                
                scr.log("Played card: {0}".format(card_name))
                action_performed: bool = globals()[load_card(card).action](p, scr)

                if action_performed:
                    p.cards_played.append(card)
                    p.actions_left -= 1
                else:
                    p.current_hand.append(card)
                break
            # except:
            #     p.current_hand.append(card)
            #     scr.log("Action failed!", 2)


def magic_spell(p: Player, scr: Screen) -> bool:
    p.draw_cards(2, scr)
    return True

def woodcutter(p: Player, scr: Screen) -> bool:
    p.add_money(2, scr)
    p.add_purchases(1, scr)
    return True

def smithy(p: Player, scr: Screen) -> bool:
    p.draw_cards(3, scr)
    return True

def festival(p: Player, scr: Screen) -> bool:
    p.add_actions(2, scr)
    p.add_purchases(1, scr)
    p.add_money(2, scr)
    return True

def mine(p: Player, scr: Screen) -> bool:
    money_cards = {}
    for card in p.current_hand:
        if "money" in load_card(card).cardtype:
            money_cards.update({card: card})
    
    if len(money_cards.keys()) == 0:
        scr.log("No money cards to upgrade!", 2)
        return False


    scr.show_main_content(
        ["Which card do you want to upgrade?"] + format_cards(money_cards.keys(), r_main_content.width)
    )
    
    chosen_card = input_card_selection(list(money_cards.keys()), scr)
    
    if chosen_card is None: return

    card_name = chosen_card.name

    upgrade_card = ""
    if card_name == "platinum coin":
        scr.log("Sorry, the fun stops here.", 2)
        return False
    elif card_name == "gold coin":
        upgrade_card = "platinum coin"
    
    elif card_name == "silver coin":
        upgrade_card = "gold coin"
    
    elif card_name == "copper coin":
       upgrade_card = "silver coin"
    else:
        return False
    
    if store.gift_card(p, upgrade_card, scr, pile="hand"):
        p.trash_hand_card(money_cards[card_name], scr)
        return True
    else:
        return False
    
def bandit_sp(p: Player, scr: Screen) -> bool:
    store.gift_card(p, "gold coin", scr, pile="discard")
    return True

def village(p: Player, scr: Screen) -> bool:
    p.add_actions(2, scr)
    p.draw_cards(1, scr)
    return True

def cellar(p: Player, scr: Screen) -> bool:

    cards = [i for i in p.current_hand]

    scr.show_main_content(
        ["Which cards do you want to discard?", "Separate your choices with a comma."] + format_cards(cards, r_main_content.width)
    )
    
    chosen_cards = input_cards_selection(cards, scr, min=1, max=len(p.current_hand))
    
    if chosen_cards == []: return False

    p.add_actions(1, scr)

    for card in chosen_cards:
        scr.log("Discarding: {0}".format(card.name))
        p.current_hand.remove(card.name)
        p.discardpile.append(card.name)
    
    p.draw_cards(len(chosen_cards), scr)

    return True

def council(p: Player, scr: Screen) -> bool:

    p.draw_cards(4, scr)
    p.add_purchases(1, scr)
    return True

def laboratory(p: Player, scr: Screen) -> bool:

    p.draw_cards(2, scr)
    p.add_actions(1, scr)
    return True

def moneylender(p: Player, scr: Screen) -> bool:

    if "copper coin" in p.current_hand:
        p.trash_hand_card("copper coin", scr)
        p.add_money(3, scr)
        return True
    
    else:
        scr.log("No copper coin to remove from your hand!", 2)
        return False

def chapel(p: Player, scr: Screen) -> bool:

    cards = [i for i in p.current_hand]

    scr.show_main_content(
        ["Which cards do you want to remove from your deck?", "Separate your choices with a comma."] + format_cards(cards, r_main_content.width)
    )
    
    chosen_cards = input_cards_selection(cards, scr, min=1, max=len(p.current_hand))
    
    if chosen_cards == []: return False

    for card in chosen_cards:
        p.trash_hand_card(card.name, scr)

    return True
from data import Player, Card, s_store
from utils import load_card, clear_screen, input_card_selection, format_cards
from screen import Screen
from screen import r_main_content

def purchase_card(p: Player, card: str, scr: Screen) -> bool:
    """
    The transaction method. Buys a card for a player using their balance.
    The purchased card gets taken out of the shop, and placed into the player's discard pile.
    """
    # Card doesn't exist in the store
    if card not in s_store:
        scr.log("This card doesn't exist in the store!", 2)
        return False

    # Card has 0 left in the store
    elif s_store.get(card) == 0:
        scr.log("This card cannot be bought anymore!", 2)
        return False

    # Player can't purchase any more cards
    elif p.purchases_left == 0:
        scr.log("You can't buy any more cards this turn!", 2)
        return False

    else:
        # Load in the card
        card_bought = load_card(card)

        if card_bought.cost > (p.current_hand_balance + p.bonus_coins - p.amount_spent):
            scr.log("Insufficient funds!", 2)
            return False
        
        # Confirm purchase
        p.purchases_left -= 1
        clear_screen()
        scr.log("Bought card: {0}".format(card), 1)

        p.add_discardpile_card(card_bought.name)

        # Subtract cost from balance
        p.amount_spent += card_bought.cost


        remove_card(card, scr)
        return True


def remove_card(card: str, scr) -> None:
    """
    Removes a card from the store.
    """

    # Remove one card from the store list
    s_store[card] -= 1

    if (s_store[card] == 0):
        scr.log("This was the last card of this type: There are none left.")

def gift_card(p: Player, card: str, scr, pile: str=None) -> bool:
    """
    Gifts a player a certain card. 
    """
    if pile is None:
        pile = "discard" 

    # Card doesn't exist in the store
    if card not in s_store.keys():
        scr.log("This card doesn't exist in the store!", 2)
        return False

    # Card has 0 left in the store
    elif s_store.get(card) == 0:
        scr.log("There are no more copies left of this card.", 2)
        return False

    else:
        scr.log("Received card: " + card, 1)

        # Decide where to add the card
        if pile == "hand":
            p.add_hand_card(card)
        elif pile == "draw":
            p.add_drawpile_card(card)
        else: 
            p.add_discardpile_card(card)

        remove_card(card, scr)
        return True

def routine(scr: Screen, p: Player) -> None:
    """
    Store routine. Allows player to view and buy cards.
    """

    content: [] = []
    content.append(("=#= Welcome to the store! =#=".center(r_main_content.width, " "), 1))
    content.append("Any bought item will go onto your discard pile.")
    content.append("Items for sale:")
    
    content = content + format_cards(
        list(s_store.keys()), r_main_content.width, 
        show_description=True, show_type=True, show_cost=True,
        custom_lines=["  - Left in stock: {0}".format(s_store.get(i)) for i in list(s_store.keys())]
    )

    content.append("You have: {0} (+{1}) - {2} = ${3} left."
        .format(
            p.current_hand_balance, 
            p.bonus_coins,
            p.amount_spent,
            p.current_hand_balance + p.bonus_coins - p.amount_spent
        )
    )
    

    scr.show_main_content(content)

    done = False
    # while we're not done with buying something, stay in this loop.
    while not done: 
        card: Card = input_card_selection(list(s_store.keys()), scr)

        # Check if cards was picked
        if card is None: 
            # scr.clear_main_content()
            done = True
            continue

        if (p.purchases_left <= 0):
            scr.log("You don't have any purchases left.", 2)
            continue
        
        done = purchase_card(p, card.name, scr)
    
    scr.clear_main_content()

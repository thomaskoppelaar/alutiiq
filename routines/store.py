from data import Player, Card
from utils import load_card, clear_screen, card_selection
from content_format import format_cards
from screen import regions, show_main_content

def purchase_card(p: Player, card_name, cd, store) -> None:
    """
    The transaction method. Buys a card for a player using their balance.
    The purchased card gets taken out of the shop, and placed into the player's discard pile.
    """
    # Card doesn't exist in the store
    if card_name not in store:
        print("This card doesn't exist in the store!")

    # Card has 0 left in the store
    elif store[card_name] == 0:
        print("This card cannot be bought anymore!")

    # Player can't purchase any more cards
    elif p.purchases_left == 0:
        print("You can't buy any more cards this turn!")

    else:
        # Load in the card
        card_bought = load_card(card_name, cd)

        if card_bought.cost > (p.current_hand_balance + p.bonus_coins - p.amount_spent):
            print("Insufficient funds!")
            return
        
        # Confirm purchase
        p.purchases_left -= 1
        clear_screen()
        print("Bought card: {0}".format(card_name))

        p.add_discardpile_card(card_bought)

        # Subtract cost from balance
        p.amount_spent += card_bought.cost

         


def remove_card(p: Player, card_name: str, cd, store) -> None:
    """
    Removes a card from the store.
    """

    # Remove one card from the store list
    store[card_name] -= 1

    if (store[card_name] == 0):
        print("This was the last card of this type: There are none left.")

def gift_card(p: Player, card_name: str, cd, store, pile: str=None) -> None:
    """
    Gifts a player a certain card. 
    """
    if pile is None:
        pile = "discard" 

    # Card doesn't exist in the store
    if card_name not in store:
        print("This card doesn't exist in the store!")

    # Card has 0 left in the store
    elif store[card_name] == 0:
        print("There are no more copies left of this card.")

    else:
        print("Received card:", card_name)

        card = load_card(card_name, cd)

       

        # Decide where to add the card
        if pile == "hand":
            p.add_hand_card(card)
        elif pile == "draw":
            p.add_drawpile_card(card)
        else: 
            p.add_discardpile_card(card)

        remove_card(p, card_name, cd, store)

def routine(p: Player, s: dict, cd) -> None:
    """
    Store routine. Allows player to view and buy cards.
    """

    # Get width of the main content
    width = regions["maincontent"][1]

    content: [str] = []
    content.append("=#= Welcome to the store! =#=".center(width, " "))
    content.append("Any bought item will go onto your discard pile.")
    content.append("Items for sale:")
    
    content = content + format_cards(list(s.keys()), cd, width, show_description=True, show_type=True, show_cost=True)

    content.append("You have: {0} (+{1}) - {2} = ${3} left."
        .format(
            p.current_hand_balance, 
            p.bonus_coins,
            p.amount_spent,
            p.current_hand_balance + p.bonus_coins - p.amount_spent
        )
    )
    content.append("Purchases left: {0}".format(p.purchases_left))

    show_main_content(content)

    # card: Card = card_selection(list(s.keys()), cd)

    # # Check if cards was picked
    # if card is None: return


    # if (p.purchases_left <= 0):
    #     print("You don't have any purchases left.")
    #     return
    
    # purchase_card(p, card.name, cd, s)

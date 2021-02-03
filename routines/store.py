from data import Player
from utils import load_card, clear_screen

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
    print("=#= Welcome to the store! =#=")
    print("Any bought item will go onto your discard pile.")
    print("Items for sale:")
    i = 1
    for name, qty in s.items():
        qty = "x("+str(qty)+")" if qty > 0 else "(sold out!)" 
        card = load_card(name, cd)
        card_price = "$" + str(card.cost)

        # example output:
        # 1. silver coin x(7) $3
        print(" {0}.".format(i), name, qty, card_price)
        print("  - {0}".format(card.description))
        print()
        i += 1

    print("You have: {0} (+{1}) - {2} = ${3} left."
        .format(
            p.current_hand_balance, 
            p.bonus_coins,
            p.amount_spent,
            p.current_hand_balance + p.bonus_coins - p.amount_spent
        )
    )
    print("Purchases left: {0}".format(p.purchases_left))

    print("(B)uy item, (C)ancel")
    player_choice = ""
    while 1:
        player_choice = input("Your choice: ")
        player_choice = player_choice.upper()

        if len(player_choice) == 0 or player_choice[0] not in ["B", "C"]:
            print("That's not an option!")
            continue

        if player_choice == "C":
            clear_screen()
            print("exited store.")
            break

        elif player_choice == "B":
            if (p.purchases_left <= 0):
                print("You don't have any purchases left.")
                break

            print("Which item would you like to buy? (C to cancel)")
            item_choice = input("Your purchase: ")
            item_choice = item_choice.lower()

            if (item_choice == "c"): break

            if item_choice.isdigit():
                try:
                    index = int(item_choice)-1
                    card_name = list(s.keys())[index]

                    purchase_card(p, card_name, cd, s)
                    break
                except:
                    print("Invalid number choice!")
            else:
                if s.get(item_choice) == None:
                    print("That item does not exist in the store.")
                    break
                else:
                    purchase_card(p, item_choice, cd, s)
                    break

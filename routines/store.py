from data.player import Player
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

        if card_bought.cost > p.current_turn_balance:
            print("Insufficient funds!")
            return
        
        # Confirm purchase
        p.purchases_left -= 1
        clear_screen()
        print("Bought card: {0}".format(card_name))
        print("===")

        # Add newly bought card to discard pile
        p.discardpile.append(card_bought)
        # And into deck
        p.deck.append(card_bought)

        # Subtract cost from balance
        p.current_turn_balance -= card_bought.cost

        # Remove one card from the store list
        store[card_name] -= 1   


def routine(p: Player, s: dict, cd) -> None:
    """
    Store routine. Allows player to view and buy cards.
    """
    print("=#= Welcome to the store! =#=")
    print("Items for sale:")
    i = 1
    for name, qty in s.items():
        qty = "x("+str(qty)+")" if qty > 0 else "(sold out!)" 
        card_price = "$" + str(load_card(name, cd).cost)

        # example output:
        # 1. silver coin x(7) $3
        print(" {0}.".format(i), name, qty, card_price)
        i += 1

    print("You have: ${0} left.".format(p.current_turn_balance))
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

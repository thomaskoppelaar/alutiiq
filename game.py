import random

from utils import load_card, clear_screen, card_data
from data.player import Player
from data.session_objects import Store
from routines import store
from routines import actions

def start_new_game(p: Player, cd) -> None:
    """
    Function that gets called at the start of a new game.

    p: The player object to start the game with.
    cd: The card data object.
    """

    # Add starter cards into deck
    p.deck = [load_card("copper coin", cd)] * 7
    p.deck += [load_card("land", cd)] * 3
    p.deck += [load_card("magic spell", cd)]
    
    
    # Copy deck into drawpile
    p.drawpile = p.deck.copy()

    # shuffle draw pile
    random.shuffle(p.drawpile)

    # Draw 5 cards
    p.draw_cards(5, verbose=False)


def start_turn(p: Player) -> None:

    # Get balance
    p.current_hand_balance = p.get_hand_value()

    # Set actions and purchases left
    p.purchases_left = 1
    p.actions_left = 1


def end_turn(p: Player) -> None:
    clear_screen()
    
    # Reset player balance
    p.current_hand_balance = 0
    p.bonus_coins = 0
    p.amount_spent = 0
    
    # Put all remaining cards in hard onto the discard pile
    print("Putting hand cards in discard pile...")
    p.hand_to_discard()
    
    # Draw 5 cards
    p.draw_cards(5, verbose=False)

    print("Ended turn.")


### Start of program


# Create player
mainguy = Player()

# Start the game as this new dude
start_new_game(mainguy, card_data)

while 1:
    start_turn(mainguy)

    mainguy.show_hand_cards()

    player_choice = ""

    while 1:

        print("show (S)tore, show (H)and")
        print("play (A)ction, (E)nd turn")
        print("screen (C)lear, (Q)uit game")

        player_choice = input("Your choice: ")
        player_choice = player_choice.upper()

        if player_choice not in ["E", "S", "H", "Q", "C", "A"]:
            print("That's not valid input!")
    
        if (player_choice == "Q"):
            exit(0)
        elif (player_choice == "C"):
            clear_screen()

        elif (player_choice == "H"):
            clear_screen()
            mainguy.show_hand_cards()

        elif (player_choice == "E"):
            end_turn(mainguy)
            break
        elif (player_choice == "S"):
            clear_screen()
            store.routine(mainguy, Store, card_data)
        elif (player_choice == "A"):
            actions.routine(mainguy, Store, card_data)

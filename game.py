import random

from utils import load_card, clear_screen, card_data
from data import Player, Store, session_objects
from routines import actions, store, turns, information

def start_new_game(p: Player, cd) -> None:
    """
    Function that gets called at the start of a new game.

    p: The player object to start the game with.
    cd: The card data object.
    """
    # Reset turn counter
    session_objects.Turn_counter = 0

    clear_screen()

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


### Start of program


# Create player
mainguy = Player()

# Start the game as this new dude
start_new_game(mainguy, card_data)

while 1:
    turns.start_turn(mainguy)

    mainguy.show_hand_cards()

    player_choice = ""

    while 1:
        print("=== Turn options ===")
        print("show (S)tore, show (H)and")
        print("play (A)ction, (E)nd turn")
        print("screen (C)lear, (Q)uit game")
        print("(I)nformation about a card")
        print("====================")

        player_choice = input("Your choice: ")
        player_choice = player_choice.upper()

        if (player_choice == "Q"):
            exit(0)
        elif (player_choice == "C"):
            clear_screen()

        elif (player_choice == "H"):
            clear_screen()
            mainguy.show_hand_cards()

        elif (player_choice == "E"):
            turns.end_turn(mainguy)
            break
        elif (player_choice == "S"):
            clear_screen()
            store.routine(mainguy, Store, card_data)
        elif (player_choice == "A"):
            actions.routine(mainguy, Store, card_data)
        elif (player_choice == "I"):
            information.routine(mainguy, Store, card_data)
        else:
            print("That's not valid input!")

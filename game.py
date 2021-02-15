import random
import curses

from utils import load_card, clear_screen, card_data
from data import Player, Store, session_objects
from routines import actions, store, turns, information
from screen import Screen


def start_new_game(p: Player, scr, cd) -> None:
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
    # p.deck += [load_card("magic spell", cd)]
    
    
    # Copy deck into drawpile
    p.drawpile = p.deck.copy()

    # shuffle draw pile
    random.shuffle(p.drawpile)

    # Draw 5 cards
    p.draw_cards(5, main_screen, verbose=False)


### Start of program


# Create player
mainguy = Player()

# Create screen
main_screen = Screen()
main_screen.init_screen()
main_screen.calibration_routine()
main_screen.display_main()

# Start the game as this new dude
start_new_game(mainguy, main_screen, card_data)

turns.start_turn(mainguy, main_screen)

# Wait for some input
c = ""
while c != "q":
    main_screen.move_cursor_to_userinput()

    main_screen.update_dynamic_values(mainguy.get_hand_value())
    main_screen.update_hand_card(mainguy.get_hand_cards())

    c = main_screen.retrieve_user_input().lower()

    if (c == "e"):
        turns.end_turn(mainguy, main_screen)
        turns.start_turn(mainguy, main_screen)
    elif (c == "s"):
        store.routine(main_screen, mainguy, Store, card_data)


main_screen.end_screen()

# while 1:
#     turns.start_turn(mainguy)

#     player_choice = ""

#     while 1:
#         mainguy.show_hand_cards()
#         print("=== Turn:", session_objects.Turn_counter, "===")
#         print("Actions left:", mainguy.actions_left)
#         print("Purchases left:", mainguy.purchases_left)
#         print("show (S)tore, show (H)and")
#         print("play (A)ction, (E)nd turn")
#         print("screen (C)lear, (Q)uit game")
#         print("(I)nformation about a card")
#         print("===============")

#         player_choice = input("Your choice: ")
#         player_choice = player_choice.upper()

#         if (player_choice == "Q"):
#             exit(0)
#         elif (player_choice == "C"):
#             clear_screen()

#         elif (player_choice == "H"):
#             clear_screen()
#             mainguy.show_hand_cards()

#         elif (player_choice == "E"):
#             turns.end_turn(mainguy)
#             break
#         elif (player_choice == "S"):
#             clear_screen()
#             store.routine(mainguy, Store, card_data)
#         elif (player_choice == "A"):
#             actions.routine(mainguy, Store, card_data)
#         elif (player_choice == "I"):
#             information.routine(mainguy, Store, card_data)
#         else:
#             print("That's not valid input!")

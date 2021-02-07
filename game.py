import random
import curses

from utils import load_card, clear_screen, card_data
from data import Player, Store, session_objects
from routines import actions, store, turns, information
import screen


def start_new_game(p: Player, cd) -> None:
    """
    Function that gets called at the start of a new game.

    p: The player object to start the game with.
    cd: The card data object.
    """
    # Reset turn counter
    session_objects.Turn_counter = 0

    clear_screen()
    print("=== ALUTIIQ ===")
    print("Version: 0.2")
    print("=== GAME START ===")

    # Add starter cards into deck
    p.deck = [load_card("copper coin", cd)] * 7
    p.deck += [load_card("land", cd)] * 3
    # p.deck += [load_card("magic spell", cd)]
    
    
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

# Create screen
main_screen = curses.initscr()
screen.init_screen(main_screen)
screen.calibration_routine(main_screen)
screen.display_main(main_screen)

turns.start_turn(mainguy)


# Wait for some input
c = ""
while c != "q":

    screen.update_dynamic_values(main_screen)
    screen.update_hand_card(main_screen, mainguy)

    c = screen.retrieve_user_input(main_screen)

    if (c == "e"):
        turns.end_turn(mainguy)
        turns.start_turn(mainguy)
    elif (c == "s"):
        store.routine(mainguy, Store, card_data)


screen.end_screen(main_screen)

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

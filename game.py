import random
import curses

from data import Player, s_store, session_objects
from utils import load_card, clear_screen, format_cards
from routines import actions, store, turns
from screen import Screen, r_main_content

def start_new_game(p: Player, scr) -> None:
    """
    Function that gets called at the start of a new game.

    p: The player object to start the game with.
    """
    # Reset turn counter
    session_objects.s_turn_counter = 0

    clear_screen()
    
    # Add starter cards into deck
    p.deck = ["copper coin"] * 7
    p.deck += ["land"] * 3
    
    # Copy deck into drawpile
    p.drawpile = p.deck.copy()

    # shuffle draw pile
    random.shuffle(p.drawpile)

    # Draw 5 cards
    p.draw_cards(5, main_screen, verbose=False)


### Start of game

# Create player
mainguy = Player()

# Create screen
main_screen = Screen()
main_screen.init_screen()
main_screen.calibration_routine()
main_screen.display_main()

# Start the game as this new dude
start_new_game(mainguy, main_screen)

turns.start_turn(mainguy, main_screen)

main_screen.update_turn_overview(
    mainguy.get_hand_value(), mainguy.actions_left, mainguy.purchases_left, mainguy.bonus_coins,
    mainguy.current_hand_balance + mainguy.bonus_coins - mainguy.amount_spent
)

# Wait for some input
c = ""
while c != "q":
    main_screen.move_cursor_to_userinput()

    # Update screen regions
    main_screen.update_top_dynamic_values(mainguy.get_deck_score())
    main_screen.update_hand_card(mainguy.get_hand_cards())

    # Display cards in hand
    card_set = {}
    for card in mainguy.current_hand:
        card_set[card] = card_set.get(card, 0) + 1

    content = []
    content.append(("=#= Cards currently in your hand: =#=".center(r_main_content.width, " "), 1))
    content = content + format_cards([card for card in card_set.keys()], r_main_content.width
        , show_description=True, show_type=True
        )
    main_screen.show_main_content(content)

    # Get userinput
    c = main_screen.retrieve_user_input().lower()

    # End turn
    if (c == "e"):
        turns.end_turn(mainguy, main_screen)
        turns.start_turn(mainguy, main_screen)
    
    # Store
    elif (c == "s"):
        store.routine(main_screen, mainguy)

    # Play Action
    elif (c == "a"):
        actions.routine(mainguy, main_screen)
    
    # Update screen regions after an action
    mainguy.current_hand_balance = mainguy.get_hand_value()
    main_screen.update_turn_overview(
        mainguy.get_hand_value(), mainguy.actions_left, mainguy.purchases_left, mainguy.bonus_coins,
        mainguy.current_hand_balance + mainguy.bonus_coins - mainguy.amount_spent
    )

# Close the screen
main_screen.end_screen()

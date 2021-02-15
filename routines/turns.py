from data import Player, session_objects
from utils import clear_screen
from screen import Screen

def start_turn(p: Player, scr: Screen) -> None:

    

    # Get balance
    p.current_hand_balance = p.get_hand_value()

    # Set actions and purchases left
    p.purchases_left = 1
    p.actions_left = 1

    session_objects.Turn_counter += 1

    scr.log("Started turn {0}.".format(session_objects.Turn_counter))


def end_turn(p: Player, scr: Screen) -> None:
    scr.clear_main_content()
    scr.clear_history()
    
    # Reset player balance
    p.current_hand_balance = 0
    p.bonus_coins = 0
    p.amount_spent = 0

    if session_objects.Game_mode == "castle race":
        if any(card.name == "castle" for card in p.deck):
            print("=== GAME WON ===")
            print("You've won the castle race!")
            print("Turns taken:", session_objects.Turn_counter)
            input("Press enter to exit.")
            exit(0)

    p.played_cards_to_discard()
    
    # Put all remaining cards in hard onto the discard pile
    scr.log("Putting hand cards in discard pile...")
    p.hand_to_discard()
    
    # Draw 5 cards
    p.draw_cards(5, scr, verbose=True)

    scr.log("Ended turn.")

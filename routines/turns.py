from data import Player
from utils import clear_screen

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

# Action cards probably deserve their own little file
from data.player import Player
from utils import clear_screen

def routine(p: Player, s: dict, cd: dict) -> None:
    """
    Action routine. Allows player to play action cards.
    """
    clear_screen()
    if p.actions_left <= 0:
        print("You don't have any actions left.")
        return
    action_cards = [card for card in p.current_hand if "action" in card.cardtype]
    if len(action_cards) == 0:
        print("You don't have any action cards to play.")
        return

    print("Which action do you want to play?")
    for card in action_cards:
        print(" -", card.name)
    
    player_choice = ""
    while 1:
        player_choice = input("Your choice: (C to cancel) ")
        player_choice = player_choice.lower()

        if len(player_choice) == 0:
            print("Enter an option.")
            continue

        if player_choice == "c":
            print("Action cancelled.")
            break
        else:
            perform_action(p, s, cd, player_choice)
            break


# WIP
def perform_action(p: Player, s: dict, cd: dict, card_name: str) -> None:
    """
    Plays a card in the player's hand.
    Once a card is successfully played, the card gets put on the player's discard pile.
    """
    for card in p.current_hand:

        # Found the card that we want to play
        if "action" in card.cardtype and card.name == card_name:
            try:
                globals()[card.action](p, s, cd)
                p.actions_left -= 1
                p.current_hand.remove(card)
                p.discardpile.append(card)
                p.show_hand_cards()
                break
            except:
                print("Action failed!!!")


def magic_spell(p: Player, s: dict, cd: dict) -> None:
    p.draw_cards(2)

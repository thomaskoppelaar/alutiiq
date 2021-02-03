# Action cards probably deserve their own little file
from data import Player, Card
from utils import clear_screen, load_card
from routines import store

def routine(p: Player, s: dict, cd: dict) -> None:
    """
    Action routine. Allows player to play action cards.
    """
    clear_screen()
    if p.actions_left <= 0:
        print("You don't have any actions left.")
        return
    action_cards: [Card] = [card for card in p.current_hand if "action" in card.cardtype]
    if len(action_cards) == 0:
        print("You don't have any action cards to play.")
        return

    print("Which action do you want to play?")
    i: int = 1
    for card in action_cards:
        print(" {0}.".format(i), card.name)
        print("  - {0}".format(card.description))
        i += 1
    
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
            if player_choice.isdigit():
                try:
                    index = int(player_choice) - 1
                    card_name = action_cards[index].name
                    perform_action(p, s, cd, card_name)
                    break
                except:
                    print("Invalid number choice!")

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
                action_performed: bool = globals()[card.action](p, s, cd)

                if action_performed:
                    p.actions_left -= 1

                    # Move card from hand onto discard pile
                    p.card_played(card)
                
                p.show_hand_cards()
               

                break
            except:
                print("Action failed!")


def magic_spell(p: Player, s: dict, cd: dict) -> bool:
    p.draw_cards(2)
    return True

def woodcutter(p: Player, s: dict, cd: dict) -> bool:
    p.add_money(2)
    p.add_purchases(1)
    return True

def smithy(p: Player, s: dict, cd: dict) -> bool:
    p.draw_cards(3)
    return True

def festival(p: Player, s: dict, cd: dict) -> bool:
    p.add_actions(2)
    p.add_purchases(1)
    p.add_money(2)
    return True

def mine(p: Player, s: dict, cd: dict) -> bool:
    money_cards = {}
    for card in p.current_hand:
        if "money" in card.cardtype:
            money_cards.update({card.name: card})
    
    if len(money_cards.keys()) == 0:
        print("No money cards to upgrade!")
        return False

    else:
        print("Which card do you want to upgrade?")
        i: int = 1
        for card_name in money_cards.keys():
            print(" {0}.".format(i), card_name)
            i += 1
    player_choice = ""
    while 1:
        player_choice = input("Your choice: (C to cancel) ")
        player_choice = player_choice.lower()

        if len(player_choice) == 0:
            print("Enter an option.")
            continue

        if player_choice == "c":
            print("Action cancelled.")
            return False
        else:
            try:
                index = -1
                card_name = ""
                if player_choice.isdigit():
                    index = int(player_choice) - 1
                    card_name = list(money_cards.keys())[index]
                else:
                    if money_cards.get(player_choice) is not None:
                        card_name = player_choice

                clear_screen()
                if card_name == "platinum coin":
                    print("Sorry, the fun stops here.")
                    return False
                elif card_name == "gold coin":
                    p.trash_hand_card(money_cards[card_name])
                    secret_card = load_card("platinum coin", cd)
                    print("That's some incredible value right there!")
                    p.add_hand_card(secret_card)
                    return True
                elif card_name == "silver coin":
                    p.trash_hand_card(money_cards[card_name])
                    store.gift_card(p, "gold coin", cd, s, pile="hand")
                    print("Upgraded a silver to a gold coin.")
                    return True
                elif card_name == "copper coin":
                    p.trash_hand_card(money_cards[card_name])
                    store.gift_card(p, "silver coin", cd, s, pile="hand")
                    print("Upgraded a copper to a silver coin.")
                    return True

                
            except:
                print("Invalid card choice!")
                continue

            


def bandit_sp(p: Player, s: dict, cd: dict) -> bool:
    store.gift_card(p, "gold coin", cd, s, pile="discard")
    return True

def village(p: Player, s: dict, cd: dict) -> bool:
    p.add_actions(2)
    p.draw_cards(1)
    return True
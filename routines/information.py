from utils import load_card, clear_screen
from data.player import Player

def routine(p: Player, s: dict, cd: dict) -> None:
    """
    Information routine. allows the player to get the description of any particular known card.
    """
    clear_screen()
    print("There are currently {0} cards known, {1} of which are in play.".format(len(cd), len(s)))
    print("Write down a card name that you would like more information about.")
    print("Show (S)tore cards, show (A)ll cards")

    
    while 1:
        player_choice = input("Your choice: (C to cancel) ")
        player_choice = player_choice.lower()

        if player_choice == "c": 
            clear_screen()
            break

        if len(player_choice) == 0:
            print("Please provide some input.")
            continue
        if player_choice == "s":
            clear_screen()
            print("Cards in store:")
            for card in s.keys():
                print(" -", card)
            continue
        if player_choice == "a":
            clear_screen()
            print("All cards in this game:")
            for card in cd.keys():
                print(" -", card)
            continue
        
        try:
            information_card = load_card(player_choice, cd)
            
            print("=== INFORMATION ABOUT CARD ===")
            print(information_card.description)
            continue
        except:
            print("That card does not exist.")



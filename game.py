import random
import json
from types import SimpleNamespace
import os


# System call to clear the console
def clear_screen():
    os.system('cls' if os.name=='nt' else 'clear')




store = {
    "silver coin": 5,
    "land": 3
}

# Card object
class Card:
    name: str = ""
    cost: int = 0
    cardtype: str = ""
    value: int = 0

    def __init__(self, d: dict): 
        self.__dict__.update(d) 

# Player object
class Player: 

    # List containing all cards.
    deck: [Card] = []

    # List containing current drawpile.
    drawpile: [Card] = []

    # List containing all cards in the discard pile.
    discardpile: [Card] = []

    # List containing all cards the player is currently holding.
    current_hand: [Card] = []

    purchases_left: int = 0
    actions_left: int = 0
    current_turn_balance: int = 0

# (Boilerplate) Load a json dict into an object
def load_card(card_name: str, card_data: [dict]) -> Card:
    """
    Makes a card object out of a json string.
    """

    card_string = json.dumps(card_data[card_name])
    card_obj = json.loads(card_string, object_hook=Card)
    return card_obj

def start_new_game(p: Player, cd) -> None:
    """
    Function that gets called at the start of a new game.

    p: The player object to start the game with.
    cd: The card data object.
    """

    # Add starter cards into deck
    p.deck = [load_card("copper coin", cd)] * 7
    p.deck += [load_card("land", cd)] * 3
    
    
    # Copy deck into drawpile
    p.drawpile = p.deck.copy()

    # shuffle draw pile
    random.shuffle(p.drawpile)

    # Draw 5 cards
    draw_cards(p, 5)


def discard_to_draw(p: Player) -> None:
    """
    Put the player's discard pile into their drawpile.
    Happens when a player gets to draw a card, but the draw pile is empty.
    """

    # Add every item from the discard pile into the draw pile
    while p.discardpile:
        p.drawpile.append(p.discardpile.pop())

    # Shuffle
    random.shuffle(p.drawpile)

def hand_to_discard(p: Player) -> None:
    while p.current_hand:
        p.discardpile.append(p.current_hand.pop())

def draw_cards(p: Player, number_of_cards: int) -> None:

    if (number_of_cards <= 0): return

    
    # Repeat n times
    for _ in range(number_of_cards):

        # If the draw pile is empty, and the discard pile is empty, we're can't do any more.
        if (len(p.drawpile) == 0 and len(p.discardpile) == 0):
            print("Nothing left to draw!")
            return

        # If the draw pile is empty, and the discard pile isn't, put everything into the draw pile.
        if (len(p.drawpile) == 0):
             discard_to_draw(p)
 
        # Pop a card from the draw pile, and add it onto the current hand
        p.current_hand.append(p.drawpile.pop())

def show_hand_cards(p: Player):
    """
    Prints the players' cards that are in his hands.
    """
    card_set = set(p.current_hand)
    print("Current cards in hand:")
    for card in card_set:
        print("  - {0} - (x{1})".format(card.name, p.current_hand.count(card)))

    print("Total hand value: {0}".format(get_hand_value(p)))

def get_hand_value(p: Player) -> int:
    res = 0

    for card in p.current_hand:
        res += card.value

    return res

def purchase_card(p: Player, card_name, cd, store) -> None:
    if card_name not in store:
        print("This card cannot be bought!")
    elif store[card_name] == 0:
        print("This card cannot be bought anymore!")
    else:

        # Load in the card
        card_bought = load_card(card_name, cd)
        if card_bought.cost > p.current_turn_balance:
            print("Insufficient funds!")
            return
        
        if p.purchases_left == 0:
            print("You can't buy any more cards this turn!")
            return
        
        # Confirm purchase
        p.purchases_left -= 1

        print("Bought card: {0}".format(card_name))

        # Add newly bought card to discard pile
        p.discardpile.append(card_bought)
        p.deck.append(card_bought)

        # Subtract cost from balance
        p.current_turn_balance -= card_bought.cost

        # Remove one card from the store list
        store[card_name] -= 1   

def end_turn(p: Player) -> None:
    clear_screen()
    print("Ended turn.")
    
    # Reset player balance
    p.current_turn_balance = 0
    
    # Put all remaining cards in hard onto the discard pile
    hand_to_discard(p)

    # Draw 5 cards
    draw_cards(p, 5)

def start_turn(p: Player) -> None:

    # Get balance
    p.current_turn_balance = get_hand_value(p)

    # Set actions and purchases left
    p.purchases_left = 1
    p.actions_left = 1

   



### Start of program

# Load card data
f = open("data/cards.json", "r")
card_data = json.load(f)
f.close()
# Create player
mainguy = Player()

# Start the game as this new dude
start_new_game(mainguy, card_data)

while 1:
    start_turn(mainguy)

    show_hand_cards(mainguy)

    player_choice = ""

    while 1:

        print("(E)nd turn, show (S)tore, show (H)and, (C)lear screen, (Q)uit game")
        player_choice = input("Your choice: ")
        player_choice = player_choice.upper()

        if player_choice not in ["E", "S", "H", "Q", "C"]:
            print("That's not valid input!")
    
        if (player_choice == "Q"):
            exit(0)
        elif (player_choice == "C"):
            clear_screen()

        elif (player_choice == "H"):
            show_hand_cards(mainguy)
        elif (player_choice == "E"):
            end_turn(mainguy)
            break
        elif (player_choice == "S"):
            print("store babey")
    

    
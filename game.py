import random


# Player object
class player: 

    # List containing all cards.
    deck = []

    # List containing current drawpile.
    drawpile = []

    # List containing all cards in the discard pile.
    discardpile = []

    # List containing all cards the player is currently holding.
    current_hand = []


def start_new_game(p: player):
    # Add starter cards into deck
    p.deck = ["copper coin"] * 7
    p.deck += ["land"] * 3
    
    # Copy deck into drawpile
    p.drawpile = p.deck.copy()

    # shuffle draw pile
    random.shuffle(p.drawpile)

    # take 5 cards from the drawpile and place them into the hand
    draw_cards(p, 5)


# Put the player's discard pile into their drawpile.
# Happens when a player gets to draw a card, but the draw pile is empty.
def discard_to_draw(p: player):

    # Add every item from the discard pile into the draw pile
    for _ in p.discardpile:
        p.drawpile.append(p.discardpile.pop())

    # Shuffle
    random.shuffle(p.drawpile)


def draw_cards(p: player, number_of_cards: int):

    if (number_of_cards <= 0): return

    
    # Repeat n times
    for _ in range(number_of_cards):

        # If the draw pile is empty, and the discard pile is empty, we're can't do any more.
        if (len(p.drawpile) == 0 and len(p.discardpile == 0)):
            print("Nothing left to draw!")
            return

        # If the draw pile is empty, and the discard pile isn't, put everything into the draw pile.
        if (len(p.drawpile) == 0):
             discard_to_draw(p)
 
        # Pop a card from the draw pile, and add it onto the current hand
        p.current_hand.append(p.drawpile.pop())




# Start of program

# Create player
mainguy = player()

# Start the game as this new dude
start_new_game(mainguy)

print(mainguy.current_hand)
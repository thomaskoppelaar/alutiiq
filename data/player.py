from data.card import Card
import random

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

    # Amount of money in hand through treasure.
    current_hand_balance: int = 0

    bonus_coins: int = 0

    amount_spent: int = 0

    def discard_to_draw(self) -> None:
        """
        Put the player's discard pile into their drawpile.
        Happens when a player gets to draw a card, but the draw pile is empty.
        """

        # Add every item from the discard pile into the draw pile
        while self.discardpile:
            self.drawpile.append(self.discardpile.pop())

        # Shuffle cards
        random.shuffle(self.drawpile)

    def hand_to_discard(self) -> None:
        """
        Adds all cards that the player is holding onto the discard pile.
        Happens at the end of the players turn.
        """
        # Whilst the player's hand has cards, put them onto the discard pile.
        while self.current_hand:
            self.discardpile.append(self.current_hand.pop())

    def draw_cards(self, n: int, verbose: bool = True) -> None:
        """
        Tries to take n cards from the player's drawpile, and places them into the player's hand.
        If the drawpile is empty, the discard pile will be added onto the drawpile and shuffled.
        """
        # What are you doin trying to draw negative cards
        if (n <= 0): 
            print("Uh, you tried to draw",n,"cards.")
            return

        print("Drawing", n, "cards...")
        # Repeat n times
        for _ in range(n):

            # If the draw pile is empty, and the discard pile is empty, we're can't do any more.
            if (len(self.drawpile) == 0 and len(self.discardpile) == 0):
                print("Nothing left to draw!")
                break

            # If the draw pile is empty, and the discard pile isn't, put everything into the draw pile.
            if (len(self.drawpile) == 0):
                self.discard_to_draw()
    
            # Pop a card from the draw pile, and add it onto the current hand
            card_drawn = self.drawpile.pop()
            if verbose: print("Drew card:", card_drawn.name)
            self.current_hand.append(card_drawn)
        
        # Update hand value
        self.current_hand_balance = self.get_hand_value()

    def show_hand_cards(self) -> None:
        """
        Prints the players' cards that are in his hands.
        Also prints the hand value.
        """
        card_set = {}
        print("Current cards in hand:")
        for card in self.current_hand:
            card_set[card.name] = card_set.get(card.name, 0) + 1

        for card in card_set:
            print("  - {0} - (x{1})".format(card, sum([1 for i in self.current_hand if i.name == card])))

        print("Total money in hand:", self.get_hand_value())
        print("Money gained through actions:", self.bonus_coins)

    def get_hand_value(self) -> int:
        """
        Gets the hand value (money) of the player.
        This is not equal to the value that the player has left to spend.
        """
        res = 0

        for card in self.current_hand:
            if "money" in card.cardtype:
                res += card.value

        return res

    def get_deck_score(self) -> int:
        """
        Gets the points of the player.
        This is used as the player's final score.
        """
        res = 0
        for card in self.deck:
            # Check if the card actually counts towards the final points
            if "point" in card.cardtype:
                res += card.value

   


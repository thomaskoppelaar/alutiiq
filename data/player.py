import random

from utils import load_card
from data import Card, session_objects
from screen import Screen

# Player object
class Player: 

    # List containing all cards.
    deck: [str] = []

    # List containing current drawpile.
    drawpile: [str] = []

    # List containing all cards in the discard pile.
    discardpile: [str] = []

    # List containing all cards the player is currently holding.
    current_hand: [str] = []

    # List containing all cards the player has played in a turn.
    cards_played: [str] = []

    purchases_left: int = 0
    actions_left: int = 0

    # Amount of money in hand through treasure.
    current_hand_balance: int = 0

    bonus_coins: int = 0

    amount_spent: int = 0

    def played_cards_to_discard(self) -> None:
        """
        Put the player's played cards into their discard pile.
        """
        while self.cards_played:
            self.discardpile.append(self.cards_played.pop())

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

    def draw_cards(self, n: int, scr: Screen, verbose: bool = True, ) -> None:
        """
        Tries to take n cards from the player's drawpile, and places them into the player's hand.
        If the drawpile is empty, the discard pile will be added onto the drawpile and shuffled.
        """
        # What are you doin trying to draw negative cards
        if (n <= 0): 
            scr.log("Uh, you tried to draw {0} cards.".format(n), 2)
            return

        scr.log("Drawing {0} cards...".format(n), 1)
        # Repeat n times
        for _ in range(n):

            # If the draw pile is empty, and the discard pile is empty, we're can't do any more.
            if (len(self.drawpile) == 0 and len(self.discardpile) == 0):
                scr.log("Nothing left to draw!")
                break

            # If the draw pile is empty, and the discard pile isn't, put everything into the draw pile.
            if (len(self.drawpile) == 0):
                self.discard_to_draw()
    
            # Pop a card from the draw pile, and add it onto the current hand
            card_drawn = load_card(self.drawpile.pop())
            if verbose: scr.log("Drew card: {0}".format(card_drawn.name))
            self.current_hand.append(card_drawn.name)
        
        # Update hand value
        self.current_hand_balance = self.get_hand_value()

    def add_hand_card(self, card: str) -> None:
        self.deck.append(card)
        self.current_hand.append(card)
        self.current_hand_balance = self.get_hand_value()
    
    def add_drawpile_card(self, card: str) -> None:
        self.deck.append(card)
        self.drawpile.append(card)

    def add_discardpile_card(self, card: str) -> None:
        self.deck.append(card)
        self.discardpile.append(card)

    def trash_hand_card(self, card: str, scr: Screen) -> None:
        """
        Remove a card from the player's hand and deck.
        """
        try:

            # Remove card from player
            self.current_hand.remove(card)
            self.deck.remove(card)

            # Add card into trashpile
            session_objects.s_trashpile.append(card)

            scr.log("Removed {0} from deck.".format(load_card(card).name))

        except ValueError:

            print("Can't remove this card!") 

    def get_hand_cards(self) -> [str]:
        """
        Gets a printable version of the player's hand cards.
        """

        # First, get a set of the player's cards, and count how many they have of each card.
        card_set = {}
        for card in self.current_hand:
            card_set[card] = card_set.get(card, 0) + 1

        # Then, format strings in a list in the way they should be displayed.
        res = []
        for card in card_set:
            
            # Card name, padded with strings to be 15 characters long
            string = "- {0}".format(card)
            string = string.ljust(15, " ")

            # Card count, padded with strings to be 3 characters long
            string += " x{0}".format(sum([1 for i in self.current_hand if i == card])).rjust(4, " ")
            res.append(string)

        return res

    def get_hand_value(self) -> int:
        """
        Gets the hand value (money) of the player.
        This is not equal to the value that the player has left to spend.
        """
        res = 0

        for i in self.current_hand:
            card = load_card(i)
            if "money" in card.cardtype:
                res += card.value

        return res

    def get_deck_score(self) -> int:
        """
        Gets the points of the player.
        This is used as the player's final score.
        """
        res = 0
        for i in self.deck:
            card = load_card(i)
            # Check if the card actually counts towards the final points
            if "point" in card.cardtype:
                res += card.value
        return res

    def add_actions(self, i: int, scr: Screen) -> None:
       """
       Should be called whenever the player gets bonus actions.
       """
       scr.log("Gained {0} bonus action(s)!".format(i), 1)
       self.actions_left += i

    def add_purchases(self, i: int, scr: Screen) -> None:
        """
        Should be called whenever the player gets bonus purchases.
        """
        scr.log("Gained {0} bonus purchase(s)!".format(i), 1)
        self.purchases_left += i
    
    def add_money(self, i: int, scr: Screen) -> None:
        """
        Should be called whenever the player gets bonus money.
        """
        scr.log("Gained {0} bonus money!".format(i), 1)
        
        self.bonus_coins += i
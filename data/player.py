from data import Card, session_objects
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

    # List containing all cards the player has played in a turn.
    cards_played: [Card] = []

    purchases_left: int = 0
    actions_left: int = 0

    # Amount of money in hand through treasure.
    current_hand_balance: int = 0

    bonus_coins: int = 0

    amount_spent: int = 0

    def card_played(self, card: Card) -> None:
        """
        Puts a card into a temporary pile, that gets cleared at the end of a player's turn.
        Ensures that the same card cannot be played twice within a turn.
        """
        self.current_hand.remove(card)
        self.cards_played.append(card)

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

    
    def add_hand_card(self, card: Card) -> None:
        self.deck.append(card)
        self.current_hand.append(card)
        self.current_hand_balance = self.get_hand_value()
    
    def add_drawpile_card(self, card: Card) -> None:
        self.deck.append(card)
        self.drawpile.append(card)

    def add_discardpile_card(self, card: Card) -> None:
        self.deck.append(card)
        self.discardpile.append(card)

    def trash_hand_card(self, card: Card) -> None:
        """
        Remove a card from the player's hand.
        """
        try:

            # Remove card from player
            self.current_hand.remove(card)
            self.deck.remove(card)

            # Add card into trashpile
            session_objects.Trashpile.append(card)

            print("Removed {0} from deck.".format(card.name))

        except ValueError:

            print("Can't remove this card!") 

    def get_hand_cards(self) -> [str]:
        """
        Gets a printable version of the player's hand cards.
        """

        # First, get a set of the player's cards, and count how many they have of each card.
        card_set = {}
        for card in self.current_hand:
            card_set[card.name] = card_set.get(card.name, 0) + 1

        # Then, format strings in a list in the way they should be displayed.
        res = []
        for card in card_set:
            
            # Card name, padded with strings to be 15 characters long
            string = "- {0}".format(card)
            string = string.ljust(15, " ")

            # Card count, padded with strings to be 3 characters long
            string += " x{0}".format(sum([1 for i in self.current_hand if i.name == card])).rjust(4, " ")
            res.append(string)

        return res

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

    def add_actions(self, i: int) -> None:
       """
       Should be called whenever the player gets bonus actions.
       """
       print("Gained {0} bonus action(s)! (Lasts only this turn.)".format(i))
       self.actions_left += i

    def add_purchases(self, i: int) -> None:
        """
        Should be called whenever the player gets bonus purchases.
        """
        print("Gained {0} bonus purchase(s)! (Lasts only this turn.)".format(i))
        self.purchases_left += i
    
    def add_money(self, i: int) -> None:
        """
        Should be called whenever the player gets bonus money.
        """
        print("Gained {0} bonus money! (Lasts only this turn.)".format(i))
        
        self.bonus_coins += i
[ ] = Open, [~] = being worked on, [X] = done, [?] = stuck [-] = discarded

- [X] Feature: Information option in turn
- [X] Enhancement - actions: Allow player to pick a number rather than having to type the full action card
- [X] Refactor: Figure out a way to shorten data.xyz to just become part of the data package
    - Example: to import the player object, you'd need to write `from data.player import Player`
     - Wanted result: `from data import Player`
- [X] Docs: Write out how the game works, what the rules are, and what a turn consists of
- [X] Feature - Turns: Keep track of which turn it is

=== Version 0.3 ===
- [X] Feature - Interface: Use curses.
    - [X] Mockup (see mockup.md)
    - [X] Get some window working
    - [X] Have different columns with different information
    - [X] Calibration routine
         - [X] Before player starts the game, check the window size.
            - [X] If the screen is big enough, start the game.
            - [X] Otherwise, go into a routine where the player can resize their screen until they see all of the corners
    - [X] User input
        - [X] Don't process incorrect input
            - [X] User can delete
            - [X] What happens when the player types in more than 17 characters?
                - They get limited by curses. Bless
        - [X] Quit command
        - [X] End turn command
    - [X] Turn counter
        - [X] Note what character space it has
        - [X] String formatting so it stays the correct size
        - [X] Method for updating the turn counter
    - [X] Show store
    - [X] Text scrolling
        - [X] Before sacrifices are made: try out pads
        - [X] Main content needs a way to be able to scroll using the up/down keys
            - [X] Keep track of upmost line
            - [X] Scrolling up / down functions
        - [X] I guess the most simple sacrifice to make would be to butcher the retrieve_user_input function
            - [X] Enter should return the full input
            - [X] Left_key goes back one place, Right_key one forward
            - [X] You can't go off of the 17 characters input place
            - [X] Backspace should delete the last character that was added
            - [X] Moving right shouldn't allow you to move all the way to the end of the input
                  rather, you should stick to the end of the word
        - [-] And make a function for going through the main content
            - [-] Which means keeping track of the main content
            - [-] And keeping track of which page is currently being displayed
            - [-] And displaying a new page whenever the `[` or `]` key is pressed.
    - [-] Test on Windows OS


- [X] Feature - History
    - [X] Screen should have a history region
    - [X] Screen should have a method for clearing history.
    - [X] The player's {...} should be shown in the history tab
        - [X] Gained bonuses
        - [X] Drawn cards
        - [X] Bought cards
        - [X] Played cards
    - [X] At the start of a turn, the history should be cleared.
    - [X] The history panel should automatically scroll once new items appear.
    - [-] Get feedback: How and when should history be cleared?
        - [X] Options are: on every turn,
        - [-] Never,
        - [-] Through a keybind (e.g. H),
        - [-] Or something else, namely: ...
    - [X] Add color options for logging
    - [X] Remove dependency of Player object in screen.py
- [X] Interface - more player-friendly.
    - [X] Show how many actions the player has left.
    - [X] Show card type in the information screen and the store.
    - [X] Show card description in the action screen.
    - [X] Documentation: Describe concepts of the game (e.g. discard pile, actions, etc)
        - [-] Make a new tutorial routine, which shows a bunch of cards on the screen talking about the different elements of the game.

- [X] Bug - Store: Add back store functionality
    - [X] When you have insufficient funds, you should still be able to purchase a card afterwards, rather than being kicked out of the store
- [X] Feature - Main screen: Show hand cards in the main panel (with description) when not in the store
- [X] Rework - Card storage: simply store the name of cards in a player's hand?
    - Issue: When selecting cards to discard from the player's hand, the list returned contains different objects than the ones in the player's hand.
    - Fix 1: Create a bunch of access methods for each card list the player has, and make them work on strings, cards, etc.
    - Fix 2: Store cards as names, load data only when necessary
    - [X] Implement Fix 2
- [X] Feature - Actions: Card selection should be possible
    - [X] Card selection should show in the main panel
    - [X] You should be able to ~~select~~ input a single card and confirm your choice
        - [X] Select a card
        - [-] Deselect the same card
        - [X] A confirm button (enter)
        - [X] A cancel button
        - [-] When selecting a different card, the previous selection should not be selected anymore
    - [X] Multiple cards
        - [-] Show the user how many cards they have to select
- [X] Refactor - utils: make package, merge utils.py and format_cards.py
- [X] Feature: Current turn overview
     - [X] Money in hand
     - [X] Actions left
     - [X] Purchases left
     - [X] Bonus money
     - [X] Money left
     - [X] When any value is 0, display as red, else green
- [X] Refactor - variables and function signatures:
    - [X] Be consistent in variable naming - convert everything to snake_case
- [X] Bug - bandit: Action fails due to passing screen
- [X] Rework - Mine: Show 1-2 messages when upgrading cards rather than 3
- [X] Enhance - Player getting cards: Color coding
    - [X] Buying a card is green
    - [-] Removing from deck should show up as red
    - [X] Removing from hand (into discard) is white
    - [X] Drawing card from drawpile is white
    - [X] Receiving a card from the store is green

=== Version 0.4 ===
- [~] Enhance - Windows 10: Compatibility
    - [ ] Update readme to include more detailed installation instructions
    - [ ] User input: Arrow keys are yet again different, as well as backspace
        - [ ] Create a list of ints that should be recognized as an (up/down/left/right) arrow key, and one for backspace
    - [ ] Test in CMD
        - [ ] Bug: When hitting enter on user input completion, UI for the rest of that line breaks
    - [ ] Test in Powershell  

- [X] Enhance - Interface: Show "C" as a cancel option
- [X] Rework - Interface: "Money left" should be top item on "Current turn overview"
- [ ] Enhance - Interface: Visually explain that scrolling is a thing
    - [ ] Display "Scroll down for more options" on the last line, if there is still content left to scroll to
    - [ ] Ensure last line isn't covered by scroll text
- [ ] Enhance - Store: Highlight which cards can be bought using green, and show insufficient funds / out of stock cards using red
    - [ ] Current issue: format_cards doesn't know about the user's balance
    - [ ] Furthermore, is this only relevant to the store, or would other actions benefit from this as well?
    - [ ] (e.g.) an action card like mine showing how many cards are left of the next upgrade
- [X] Bug - User input: Player was unable to use the backspace key on input
    - [X] Issue: I have roughly 0 clue ~~how the input is handled~~ what keycodes refer can refer to a backspace
    - [X] Fix: it might be the ASCII backspace (\x08 or \b) that I was missing
- [ ] Enhance - Bug catching: Save some sort of transaction log
- [ ] Bug - Interface: Interface crashes on resize of main game
    - [ ] Fix: go back to initial resize routine if the size changes to be below the minimum
- [X] Bug - User input: If the input space is full, and the user presses delete, a "?" will remain on screen.
- [ ] Bug - Interface: background sometimes not properly displayed
- [ ] Bug - Gameplay: During playtesting, player ended up with 6 cards in their hand when they won the games
- [ ] Feature - Card: Farming village card
- [X] Bug - Chapel: Player is able to trash more than 4 cards
    - [X] Fix: set correct limit
- [X] Feature - Cards: new cards
    - [X] Chapel
        - [X] Requires working trashpile
        - [X] Requires trashing method
        - [X] Card data
        - [X] Function
    - [X] Mine
        - [X] Trash a money card, gain one quality higher
        - [X] Allow player to input a card name
    - [X] Gold
        - [X] Worth 3 coin
    - [X] Bandit
        -  [X] Gain 1 gold card
    - [X] Village
        -  [X] +2 actions, +1 card
- [X] Bug: Add a temporary discard pile so that turns cannot be infinite
    - [X] Whenever an action card gets played, it should be put on a temporary pile, rather than the discard pile
    - [X] Otherwise, drawing your entire deck and looping through festival + mine + smithy + village is infinite
- [X] Feature: Add emphasis and/or color to text.
- [X] Enhancement - actions: When an action is played, show how much actions/cards/money has been gained.
- [X] Enhancement - actions/information: Have the description of a card shown when it is played.
    - [X] When viewing the information of a card, show the name and the description.
    - [-] Perhaps pick a random adjective as well, for fun? E.g. "A humble/simple/cruddy/shoddy building."
    - [X] When playing an action, the new description (stating what it does) gets printed
- [ ] Feature - Gamemodes:
    - [ ] Racing mode: Try and buy a castle in as little turns as is possible
        - [X] Keep track of turns
        - [X] Prototype
        - [ ] Documentation
        - [ ] Start screen
        - [ ] A "restart" option
    - [ ] Countdown mode: Get as much points as possible in X amount of turns
    - [ ] Score more: Get to 30 points in as little turns and with the lowest amount of cards possible.
- [X] Refactor - Interface: Have a generic method for choosing cards out of a list
    - [X] Method takes in a list of choices, and outputs a string
    - [X] Options for displaying certain information:
        - [X] Description
        - [X] Card type
        - [X] Cost
    - [X] Minimum and maximum amount of choices
        - [ ] For multiple choices, check for duplicate cards.

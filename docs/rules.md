# Introduction

Welcome to Alutiiq! This is a puzzle deckbuilder that's played entirely in the command line. The game is heavily inspired by Dominion, and currently draws all of its cards/mechanics from it.

## Goal

In this game, your goal is to acquire a castle card as fast as possible. To do this, you will need to purchase new cards and try to find a suitable strategy of getting the money you need. Try and see which combination of cards suits your playstyle.


## Card types

There are three main types of cards available for you to get during your game. The types are:

- Money: These cards will provide you with money in order to purchase new cards.
- Actions: These are the main source of variety in the game, as each card will have a different effect when played.
- Points: These cards count towards a final player "score", which may be used in some of the later game modes.

## Player deck

At the start of a new game, the player starts out with 10 cards: 7 copper coins, and 3 lands. The copper coins are the base currency, and can be used to buy the first couple of upgrades to your deck.

Any cards that you put into your deck (by e.g. buying one) will be seen in later turns. This means that you have full control over what gets placed into your deck, and which cards you draw frequently.

A player's deck is at any given moment split up into three main piles:

- A draw pile.
- A discard pile.
- A player's hand (pile).

## Player turn

Each turn, the player draws 5 cards from their draw pile, and places them in their hand. These are the cards that they have available to them for this turn.

Each turn, the player can purchase one card and play one action card. A player's buying power is determined by the value of the cards in their hand. For example, the player has the following hand:

- 3 Copper coin
- 1 Silver coin
- 1 land

Their hand value is 5. This is determined by the value of 3 copper coins (each worth 1 coin), and one silver coin (each worth 2 coins). The land card does not hold monetary value, and therefore is worth 0 coins.

At the end of a player's turn, their entire hand is discarded, and placed onto the discard pile.

If there are no more cards on a player's drawpile, the discard pile gets reshuffled and placed onto the drawpile.

## Buying a card

Each turn, a player can purchase one card. Each card purchased will be placed on top of the player's discard pile.

## Playing a card

A player can play one action card per turn. After playing the card, it gets removed from the player's hand. At the end of the turn, it gets placed on top of the discard pile.
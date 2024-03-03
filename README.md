# Top Trumps

> Top Trumps is a card game first published in 1978.[1][2] Each card contains a list of numerical data, and the aim of the game is to compare these values to try to trump and win an opponent's card. A wide variety of different packs of Top Trumps has been published.

(c) [Wikipedia](https://en.wikipedia.org/wiki/Top_Trumps)

I first encountered Top Trumps in a McDonald's Happy Meal, and it has become one of the most tedious "table games" I've played. The rules of the game, as described on [wikiHow](https://www.wikihow.com/Play-Top-Trumps), are quite simple. However, due to the lack of variability or elements of randomness, unless one is deliberately trying to lose, the game feels endless.

Wikipedia states that the playing time is 3-10 minutes. But is it, though?

## So, what is the real playtime?

The playtime for the decks from McDonald's should be quite predictable, even for the very first game, since their stats are always between 1 and 10, averaging about `35 minutes`.

The classic decks are a bit more tricky as stats values may vary significantly - year, height, price, etc. I need to gather some examples before sharing any number here.

What if each player selects a stat at random during their turn? The playtime still averages `26-30 minutes`.

So, maybe the 3-10 minutes is just how much patience the average adult has to play the game with their children?

## Test conditions

* Games emulated - `10,000`
  * With this number, the average game duration deviates within ~2%.
* Number of players - `3`
  * The average playtime decreases as more players join.
* Average number of seconds per exchange - `8`
  * Based on tests conducted with the 7 years old.
* Max exchanges - `450`
  * The assumption here is that after an hour, hardly anyone would want to continue playing the game.

Tests were run with the decks from `decks`.

## Other observations

### Are the stats identical between decks?

It appears that all the decks have unique cards in terms of stats, even the ones from McDonald's Happy Meals.

### Identical cards

Some decks contain cards that are identical in terms of stats, for example:
* McDonald's Minions: Rise of Gru - `Jean-Clawed` and `Svengeance`

# Top Trumps

> Top Trumps is a card game first published in 1978.[1][2] Each card contains a list of numerical data, and the aim of the game is to compare these values to try to trump and win an opponent's card. A wide variety of different packs of Top Trumps has been published.

(c) [Wikipedia](https://en.wikipedia.org/wiki/Top_Trumps)

I first encountered Top Trumps in a McDonald's Happy Meal, and it has become one of the most tedious "table games" I've played. The rules of the game, as described on [wikiHow](https://www.wikihow.com/Play-Top-Trumps), are quite simple. However, due to the lack of variability or elements of randomness, unless one is deliberately trying to lose, the game feels endless.

Wikipedia states that the playing time is 3-10 minutes. But is it, though?

## So, what is the real playtime?

The playtime for the packs from McDonald's should be quite predictable, even for the very first game, since their stats are always between 1 and 10. Based on emulations, the average playtime is about [`35 minutes`](https://github.com/aelmekeev/top-trumps/actions/workflows/packs.yaml).

The classic packs are a bit more complex, as the values of their stats can vary significantly — including year, height, price, etc. It may take a few games to determine what should be considered a "high" value for each stat, but otherwise, the gameplay doesn't differ much. Nonetheless, the classic packs show more variability in terms of playtime, ranging from [`34 to 56 minutes`](https://github.com/aelmekeev/top-trumps/actions/workflows/packs.yaml). In the first few games, where players might choose stats nearly at random, [the duration of the game can be reduced by up to 20%](https://github.com/aelmekeev/top-trumps/actions/workflows/strategies.yaml).

As evident, none of these durations come close to the 3-10 minutes mentioned on Wikipedia.

## Test conditions

* Games emulated - `10,000`
  * With this number, [the average game duration deviates within ~2%](https://github.com/aelmekeev/top-trumps/actions/workflows/emulations.yaml).
* Number of players - `3`
  * The average playtime [decreases as more players join](https://github.com/aelmekeev/top-trumps/actions/workflows/players.yaml).
* Average number of seconds per exchange - `8`
  * Based on tests conducted with the 7 years old.
* Max exchanges - `450`
  * The assumption here is that after an hour, hardly anyone would want to continue playing the game.

Tests were run with the packs from `packs`.

## Other observations

### Are the stats identical between packs?

It appears that all the packs have unique cards in terms of stats, even the ones from McDonald's Happy Meals.

### Identical cards

Some packs contain cards that are identical in terms of stats, for example:
* McDonald's Minions: Rise of Gru - `Jean-Clawed` and `Svengeance`
* Carta Mundi's Aircraft - `Panavia Tornado ECR` and `Panavia Tornado IDS`

### Unusual stats

* [Seattle 30 Top Things to See](https://ultimate-top-trumps.co.uk/usa/winning_moves/winning_moves/seattle_30_things_to_see.html) has some stats with `n/a` 

## Resources

* [Ultimate Top Trumps](https://ultimate-top-trumps.co.uk/) - great online collection of Top Trump packs
* [APStats/Top-Trumps-data](https://github.com/APStats/Top-Trumps-data/tree/master) - some packs in CSV format